import asyncio
from Server.Queue.MultiProcessQueue import MultiProcessQueue


web_data_queue = MultiProcessQueue.get_instance()
players_queue = asyncio.Queue()
connections_queue = asyncio.Queue()
update_packets_queue = asyncio.Queue()
