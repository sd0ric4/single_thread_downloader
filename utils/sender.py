import socket
import struct
import os

def get_file_list(file_path='images'):
    file_list = os.listdir(file_path)
    return file_list

def start_server(host='0.0.0.0', port=11322):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"服务器启动在 {host}:{port}")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"客户端连接: {address}")
        
        try:
            # 接收命令
            command = client_socket.recv(1024).decode('utf-8')
            
            if command == 'get_file_list':
                # 发送文件列表
                file_list = get_file_list()
                file_list_str = '\n'.join(file_list)
                file_list_bytes = file_list_str.encode('utf-8')
                
                # 发送文件列表大小
                size = len(file_list_bytes)
                client_socket.send(struct.pack('!I', size))
                
                # 发送文件列表
                client_socket.send(file_list_bytes)
            elif command.startswith('download_file:'):
                # 处理下载文件命令
                file_name = command.split(':')[1]
                file_path = os.path.join('images', file_name)
                
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    
                    # 发送文件大小
                    size = len(file_data)
                    client_socket.send(struct.pack('!I', size))
                    
                    # 分块发送文件
                    chunk_size = 1024
                    for i in range(0, size, chunk_size):
                        chunk = file_data[i:i + chunk_size]
                        client_socket.send(chunk)
                else:
                    # 文件不存在
                    client_socket.send(struct.pack('!I', 0))
                
        except Exception as e:
            print(f"错误: {e}")
        finally:
            client_socket.close()