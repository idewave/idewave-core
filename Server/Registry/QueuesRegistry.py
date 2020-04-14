from asyncio import Queue

from Typings.Abstract.AbstractRegistry import AbstractRegistry


class QueuesRegistry(AbstractRegistry):

    session_keys_queue = Queue()

    players_queue = Queue()

    remove_player_queue = Queue()

    connections_queue = Queue()

    disconnect_queue = Queue()

    packets_queue = Queue()

    broadcast_packets_queue = Queue()
