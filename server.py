from Socket import Socket
import socket
from indexer import Indexer
from utility import *
import time


class Server(Socket):
    def __init__(self, path_dir):
        super(Server, self).__init__()
        self.indexer = Indexer()
        self.dir_path = path_dir
        self.path = Path(self.dir_path)
        self.pattern = generate_pattern()
        self.paths = generate_paths(self.path, self.pattern)
        self.timings = []
        self.process_list = [1, 1, 1, 2, 3, 4, 1]

        self.users = []
        self.index_dict = dict()

    def set_up(self):
        self.socket.bind(('127.0.0.1', 21000))
        self.socket.listen(5)
        self.socket.setblocking(False)
        for count in self.process_list:
            start = time.time()
            self.index_dict = self.indexer.create_index(self.path, self.paths, count)
            end = time.time() - start
            self.timings.append(end)

        write_index_to_json(self.index_dict)
        print(f"Files indexed successfully!\nCreated index.json\nProcess count list: {self.process_list}\nCorresponding "
              f"timestamps: {self.timings}")
        draw_results(self.process_list, self.timings)
        print("Check <Graphs> folder for chart info!\n")
        print("Server is Listening...\n")

    async def send_data(self, user, data=None):

        await self.main_loop.sock_sendall(user, data)

    async def listen_socket(self, listened_socket=None):
        if not listened_socket:
            return

        await self.send_data(listened_socket, "Enter search query:\n".encode("utf-8"))
        print("Log:msg been sent")
        while True:
            data = await self.main_loop.sock_recv(listened_socket, 1024)
            if not len(data):
                self.users.pop()
                print(f"User <{listened_socket.getpeername()}> disconnected!")
                listened_socket.shutdown(socket.SHUT_RDWR)
                listened_socket.close()
                break

            print(f"User sent {data.decode('utf-8')}")
            response = str(self.index_dict.get(data.decode("utf-8"), "Sorry, given key not found\n"))
            await self.send_data(listened_socket, response.encode("utf-8"))

    async def accept_sockets(self):
        while True:
            user_socket, _ = await self.main_loop.sock_accept(self.socket)
            print(f"User <{user_socket.getpeername()}> connected!")

            self.users.append(user_socket)
            self.main_loop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())


if __name__ == '__main__':
    path = '/home/demon/Desktop/course_work_parallel_computing/datasets/aclImdb'
    server = Server(path)
    server.set_up()

    server.start()
