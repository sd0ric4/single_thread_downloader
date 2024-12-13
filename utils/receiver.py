import os
import struct
import gradio as gr
from self_class.mysocket import MySocket
import tempfile
from tqdm import tqdm

def download_file(file_name : str, file_path='./Downloads', host='localhost', port=11322):
    """下载文件"""
    client_socket = MySocket()
    client_socket.connect((host, port))

    try:
        command = f'download_file:{file_name}'
        client_socket.mysend(command.encode('utf-8'))
        # 接收文件大小
        size_data = client_socket.recv_all(4)
        size = struct.unpack('!I', size_data)[0]
        print(f"文件大小: {size} bytes")

        # 创建进度条
        progress_bar = tqdm(total=size, unit='B', unit_scale=True, desc=file_name)
        
        # 创建临时文件，在目标目录下
        temp_file = tempfile.NamedTemporaryFile(delete=False, dir=file_path)
        temp_file_name = temp_file.name
        print(f"正在下载文件到临时文件: {temp_file_name}")
        
        # 接收并写入文件
        received_size = 0
        while received_size < size:
            chunk_size = min(1024, size - received_size)
            chunk = client_socket.recv_all(chunk_size)
            if not chunk:
                break
            temp_file.write(chunk)
            received_size += len(chunk)
            progress_bar.update(len(chunk))
        
        temp_file.close()
        progress_bar.close()
        
        # 将临时文件移动到目标路径
        full_file_path = os.path.join(file_path, file_name)
        os.makedirs(file_path, exist_ok=True)
        os.replace(temp_file_name, full_file_path)
        print("文件下载完成")
        return full_file_path
    finally:
        client_socket.close()

def test_connection(host: str, port: int):
    client_socket = MySocket()
    try:
        client_socket.connect((host, port))
        
        # 发送命令
        command = 'get_file_list'
        client_socket.mysend(command.encode('utf-8'))
        
        # 接收文件列表
        file_list_bytes = client_socket.myreceive()
        file_list_str = file_list_bytes.decode('utf-8')
        file_list = file_list_str.split('\n')
        print(f"文件列表: {file_list}")
        file_list = [f for f in file_list if f]
        return f"<div style='color: green;'>连接成功</div>", gr.update(choices=file_list)
    except Exception as e:
        return f"<div style='color: red;'>连接失败: {e}</div>", gr.update(choices=[])
    finally:
        client_socket.close()