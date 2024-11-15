import socket
import struct

def start_server(host='0.0.0.0', port=11322):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"服务器启动在 {host}:{port}")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"客户端连接: {address}")
        
        try:
            # 读取图片
            with open('downloaded.jpg', 'rb') as f:
                image_data = f.read()
            
            # 发送文件大小
            size = len(image_data)
            client_socket.send(struct.pack('!I', size))
            
            # 分块发送文件
            chunk_size = 1024
            for i in range(0, size, chunk_size):
                chunk = image_data[i:i + chunk_size]
                client_socket.send(chunk)
                
        except Exception as e:
            print(f"错误: {e}")
        finally:
            client_socket.close()