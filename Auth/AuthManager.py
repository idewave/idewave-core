import asyncio
from asyncio.streams import StreamReader, StreamWriter
from concurrent.futures import TimeoutError
from os import urandom
from hashlib import sha1
from base64 import b64decode
from io import BytesIO
from struct import pack, unpack

from Auth.Constants.AuthStep import AuthStep
from Auth.Handlers.LoginChallenge import LoginChallenge
from Auth.Handlers.LoginProof import LoginProof
from Auth.Handlers.Realmlist import Realmlist
from Auth.Constants.LoginOpCode import LoginOpCode
from Auth.Crypto.SRP import SRP
from World.WorldPacket.WorldPacketManager import WorldPacketManager
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Auth.Constants.WorldServerAuthResponseCodes import ResponseCodes
from Account.AccountManager import AccountManager
from Auth.Crypto.HeaderCrypt import HeaderCrypt
from Utils.Debug.Logger import Logger


class AuthManager(object):

    AUTH_HANDLERS = {
        LoginOpCode.LOGIN_CHALL: LoginChallenge,
        LoginOpCode.LOGIN_PROOF: LoginProof,
        LoginOpCode.RECON_CHALL: 'ReconChallenge',
        LoginOpCode.RECON_PROOF: 'ReconProof',
        LoginOpCode.REALMLIST: Realmlist
    }

    def __init__(self, reader: StreamReader, writer: StreamWriter, **kwargs):
        self.reader = reader
        self.writer = writer
        # uses on first step
        self.srp = SRP()

        # uses on second step
        self.world_packet_manager = kwargs.pop('world_packet_manager', None)
        self.session_keys = kwargs.pop('session_keys', None)
        self.data = bytes()
        self.build = 0
        self.unk = 0
        self.account_name = None
        self.client_seed = 0
        self.auth_seed = bytes()
        self.client_hash = bytes()
        self.session_key = bytes()
        self.server_hash = bytes()

        # uses in both cases
        self.temp_ref = kwargs.pop('temp_ref', None)

    async def process(self, step: AuthStep):
        if step == AuthStep.FIRST:
            await self.authenticate_on_login_server()
        elif step == AuthStep.SECOND:
            await self.authenticate_on_world_server()
        else:
            return None

    async def authenticate_on_login_server(self):
        while True:
            try:
                request = await asyncio.wait_for(self.reader.read(1024), timeout=0.01)
                if request:
                    opcode, packet = request[0], request[1:]
                    try:
                        handler = AuthManager.AUTH_HANDLERS[LoginOpCode(opcode)]
                    except ValueError:
                        Logger.error('[AuthManager]: Incorrect request, check the opcode')
                        pass
                    else:
                        response = await handler(packet=packet, srp=self.srp, temp_ref=self.temp_ref).process()

                        if response:
                            self.writer.write(response)
            except TimeoutError:
                pass
            finally:
                await asyncio.sleep(0.01)

    async def authenticate_on_world_server(self):
        self.send_auth_challenge()
        try:
            await self._parse_data()
            self._check_session_key()
            self._generate_server_hash()
            # after this step next packets will be encrypted
            self._setup_encryption()

            if self.server_hash != self.client_hash:
                raise Exception('[Auth Manager]: Server hash is differs from client hash')
            else:
                self._send_addon_info()
                self._send_auth_response()

        except TimeoutError:
            Logger.error('[Auth Manager]: Timeout on step2')
            pass
        finally:
            await asyncio.sleep(0.01)

    def send_auth_challenge(self):
        # auth seed need to generate header_crypt
        Logger.info('[Auth Manager]: sending auth challenge')
        self.auth_seed = int.from_bytes(urandom(4), 'little')
        auth_seed_bytes = pack('<I', self.auth_seed)
        # TODO: make it like standard request handler
        response = WorldPacketManager.generate_packet(WorldOpCode.SMSG_AUTH_CHALLENGE, auth_seed_bytes)
        self.writer.write(response)

    async def _parse_data(self):
        data = await asyncio.wait_for(self.reader.read(1024), timeout=0.01)
        # omit first 6 bytes, cause 01-02 = packet size, 03-04 = opcode (0x1ED), 05-06 - unknown null-bytes
        tmp_buf = BytesIO(data[6:])
        self.build = unpack('<H', tmp_buf.read(2))[0]
        # remove next 6 unknown null-bytes (\x00)
        tmp_buf.read(6)
        self.account_name = self._parse_account_name(tmp_buf)

        # set account for using in world packet handlers
        with AccountManager() as account_mgr:
            self.temp_ref.account = account_mgr.get(name=self.account_name).account

        self.client_seed = tmp_buf.read(4)
        self.client_hash = tmp_buf.read(20)

    def _parse_account_name(self, buffer: BytesIO):
        Logger.info('[Auth Session Manager]: parsing account name')
        result = bytes()

        while True:
            char = buffer.read(1)
            if char and char != b'\x00':
                result += char
            else:
                break

        try:
            result = result.decode('utf-8')
        except UnicodeDecodeError:
            Logger.error('[Auth Session Manager]: decode error, wrong name = {}'.format(result))
        else:
            return result

    def _check_session_key(self):
        Logger.info('[Auth Session Manager]: checking session key')
        key = '#{}-session-key'.format(self.account_name)
        session_key = self.session_keys[key]

        if not session_key:
            raise Exception('[AuthMgr]: Session key does not exists')

        del self.session_keys[key]

        self.session_key = b64decode(session_key)

    def _generate_server_hash(self):
        Logger.info('[Auth Session Manager]: generating server hash for account "{}"'.format(self.account_name))

        to_hash = (
            self.account_name.encode('ascii') +
            bytes(4) +
            self.client_seed +
            int.to_bytes(self.auth_seed, 4, 'little') +
            self.session_key
        )

        self.server_hash = sha1(to_hash).digest()

    def _setup_encryption(self):
        Logger.info('[Auth Manager]: setup encryption')
        try:
            header_crypt = HeaderCrypt(self.session_key)
        except Exception as e:
            raise Exception('[Auth Manager]: error on setup encryption = {}'.format(e))
        else:
            self.world_packet_manager.set_header_crypt(header_crypt)

    def _send_auth_response(self):
        # updating session request
        response = pack('<BIBIB',
                        ResponseCodes.AUTH_OK.value,
                        0x00,   # BillingTimeRemaining
                        0x00,   # BillingPlanFlags
                        0x00,   # BillingTimeRested
                        0x01    # Expansion, 0 - normal, 1 - TBC, must be set manually for each account
                        )

        response = WorldPacketManager.generate_packet(
            opcode=WorldOpCode.SMSG_AUTH_RESPONSE,
            data=response,
            header_crypt=self.world_packet_manager.header_crypt
        )
        self.writer.write(response)

    def _send_addon_info(self):
        # TODO parse actual addon list from CMSG_AUTH_SESSION and check
        response = b'\x02\x01\x00\x00\x00\x00\x00\x00' * 16
        response = WorldPacketManager.generate_packet(
            opcode=WorldOpCode.SMSG_ADDON_INFO,
            data=response,
            header_crypt=self.world_packet_manager.header_crypt
        )
        # send this packet to show 'addons' button on Characters screen
        self.writer.write(response)
