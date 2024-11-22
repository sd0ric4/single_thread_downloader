import os
import socket
import struct

def download_file(file_name,file_path='./Downloads', host='localhost', port=11322):
    """下载文件"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        command = f'download_file:{file_name}'
        client_socket.send(command.encode('utf-8'))
        # 接收文件大小
        size_data = client_socket.recv(4)   
        size = struct.unpack('!I', size_data)[0]
        
        # 接收文件数据
        received_data = b''
        # 为什么要判断len(received_data) < size？因为recv()方法不保证一次性接收完所有数据
        while len(received_data) < size:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            received_data += chunk
        full_file_path = os.path.join(file_path, file_name)
        # 保存文件
        with open(full_file_path, 'wb') as f:
            f.write(received_data)
            
        print("文件下载完成")
        return(full_file_path)
    finally:
        client_socket.close()