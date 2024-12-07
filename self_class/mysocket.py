import socket
import struct
from typing import Optional
class MySocket(socket.socket):
    def __init__(self, sock: Optional[socket.socket] = None):
        if sock is None:
            super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        else:
            # 修正初始化方式
            fd = sock.detach()  # 首先分离文件描述符
            super().__init__(fileno=fd)  # 使用 fileno 参数而不是 _sock
            self.settimeout(sock.gettimeout())

    def mysend(self, msg):
        try:
            msg = struct.pack('!I', len(msg)) + msg  # 前缀加上消息长度
            totalsent = 0
            while totalsent < len(msg):
                sent = self.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent += sent
        except Exception as e:
            print(f"Error in mysend: {e}")

    def myreceive(self):
        try:
            # 首先接收消息长度
            raw_msglen = self.recv_all(4)
            if not raw_msglen:
                return None
            msglen = struct.unpack('!I', raw_msglen)[0]
            # 然后接收消息数据
            return self.recv_all(msglen)
        except Exception as e:
            print(f"Error in myreceive: {e}")
            return None

    def recv_all(self, n):
        data = b''
        try:
            while len(data) < n:
                packet = self.recv(n - len(data))
                if not packet:
                    raise EOFError('socket closed {} bytes into a {}-byte message'.format(len(data), n))
                data += packet
        except Exception as e:
            print(f"Error in recv_all: {e}")
        return data