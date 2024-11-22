import socket
import struct

def download_file(file_name, host='localhost', port=11322):
    """下载文件"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    try:
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
        
        # 保存文件
        with open(file_name, 'wb') as f:
            f.write(received_data)
            
        print("文件下载完成")
        return(file_name)
    finally:
        client_socket.close()