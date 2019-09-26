from os import urandom
from hashlib import sha1


class SRP(object):

    MODULUS = 0x894B645E89E1535BBDAD5B8B290650530801B18EBFBF5E8FAB3C82872A3E9BB7
    GENERATOR = 7
    MULTIPLIER = 3

    def __init__(self, **kwargs):
        self._generate_priv_ephemeral()
        self.session_key = kwargs.pop('session_key', bytes())
        self.client_proof = kwargs.pop('client_proof', bytes())
        self.server_proof = kwargs.pop('server_proof', bytes())
        self.serv_ephemeral = kwargs.pop('serv_ephemeral', None)

    def _generate_priv_ephemeral(self):
        random_19_bytes = urandom(19)
        big_random_int = int.from_bytes(random_19_bytes, 'little')
        priv_ephemeral = big_random_int % SRP.MODULUS
        self.priv_ephemeral = priv_ephemeral

    def generate_server_ephemeral(self, verifier):
        big_integer = pow(SRP.GENERATOR, self.priv_ephemeral, SRP.MODULUS)
        ephemeral = (SRP.MULTIPLIER * int(verifier) + big_integer) % SRP.MODULUS
        self.serv_ephemeral = ephemeral

    @staticmethod
    def _scramble_a_b(big_int_a, big_int_b):
        a_bytes = int.to_bytes(big_int_a, 32, 'little')
        b_bytes = int.to_bytes(big_int_b, 32, 'little')
        scramble_hash = sha1(a_bytes + b_bytes).digest()
        scramble = int.from_bytes(scramble_hash, 'little')
        return scramble

    def generate_session_key(self, client_eph, verifier):
        assert self.serv_ephemeral
        scramble = SRP._scramble_a_b(client_eph, self.serv_ephemeral)
        pow_verifier = pow(int(verifier), scramble, SRP.MODULUS)
        pow_verifier *= client_eph
        to_interleave = pow(pow_verifier, self.priv_ephemeral, SRP.MODULUS)
        self.session_key = self._sha1_interleave(to_interleave)

    def generate_client_proof(self, client_ephemeral, account):
        assert self.serv_ephemeral
        assert self.session_key
        
        modulus_bytes = int.to_bytes(SRP.MODULUS, 32, 'little').rstrip(b'\x00')
        modulus_hash = sha1(modulus_bytes).digest()
        gen_bytes = int.to_bytes(SRP.GENERATOR, 32, 'little').rstrip(b'\x00')
        gen_hash = sha1(gen_bytes).digest()
        xor_hash = bytes()

        for m_byte, g_byte in zip(modulus_hash, gen_hash):
            xor_hash += int.to_bytes(m_byte^g_byte, 1, 'little')
        
        client_eph = int.to_bytes(client_ephemeral, 32, 'little')
        server_eph = int.to_bytes(self.serv_ephemeral, 32, 'little')

        to_hash = ( xor_hash + sha1(account.name.upper().encode('ascii')).digest() +
                account.salt + client_eph + server_eph + self.session_key)

        self.client_proof = sha1(to_hash).digest()

    def generate_server_proof(self, client_ephemeral):
        assert self.session_key
        assert self.client_proof
        client_eph = int.to_bytes(client_ephemeral, 32, 'little')
        to_hash = client_eph + self.client_proof + self.session_key
        self.server_proof = sha1(to_hash).digest()

    @staticmethod
    def generate_verifier(ident, password, salt):
        login_data = '{}:{}'.format(ident, password) # ident + ':' + password
        login_hash = sha1(login_data.encode('ascii')).digest()
        salted_hash = salt + login_hash
        salted_hash_bytes = sha1(salted_hash).digest()
        salted_hash_int = int.from_bytes(salted_hash_bytes, 'little')

        verifier = pow(SRP.GENERATOR, salted_hash_int, SRP.MODULUS)
        return verifier

    def _sha1_interleave(self, big_int):
        big_array = int.to_bytes(big_int, 128, 'little').rstrip(b'\x00')

        if len(big_array) % 2 == 1:
            big_array = big_array[1:]

        part1 = bytes()
        part2 = bytes()

        for i in range(len(big_array)):
            if i % 2 == 0:
                part1 += big_array[i:i+1]
            else:
                part2 += big_array[i:i+1]

        hash1 = sha1(part1).digest()
        hash2 = sha1(part2).digest()

        interleaved = bytes()

        for i in range(20):
            interleaved += hash1[i:i+1] + hash2[i:i+1]

        return interleaved
