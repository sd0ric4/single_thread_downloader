import struct
import os
from typing import List, Tuple
from self_class.mysocket import MySocket

def get_file_list(file_path: str = 'images') -> List[str]:
    file_list = os.listdir(file_path)
    return file_list

def send_file_list(client_socket: MySocket) -> None:
    file_list = get_file_list()
    file_list_str = '\n'.join(file_list)
    file_list_bytes = file_list_str.encode('utf-8')
    client_socket.mysend(file_list_bytes)

def send_file(client_socket: MySocket, file_name: str) -> None:
    file_path = os.path.join('images', file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        size = len(file_data)
        client_socket.send(struct.pack('!I', size))
        
        chunk_size = 1024
        for i in range(0, size, chunk_size):
            chunk = file_data[i:i + chunk_size]
            client_socket.send(chunk)
    else:
        client_socket.send(struct.pack('!I', 0))
        
def handle_client(client_socket: MySocket) -> None:
    try:
        command = client_socket.myreceive().decode('utf-8')
        
        if command == 'get_file_list':
            send_file_list(client_socket)
        elif command.startswith('download_file:'):
            file_name = command.split(':')[1]
            send_file(client_socket, file_name)
    except Exception as e:
        print(f"错误: {e}")
    finally:
        if client_socket:
            try:
                client_socket.close()
            except Exception as e:
                print(f"关闭 socket 时出错: {e}")

def start_server(host: str = '0.0.0.0', port: int = 11322) -> None:
    with MySocket() as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        
        print(f"服务器启动在 {host}:{port}")
        
        while True:
            client_socket, address = server_socket.accept()
            print(f"客户端连接: {address}")
            with MySocket(sock=client_socket) as client_sock:
                handle_client(client_sock)