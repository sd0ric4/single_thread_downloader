import gradio as gr
from utils.receiver import download_file
import socket
import struct


def test_connection(host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, int(port)))
        
        # 发送命令
        command = 'get_file_list'
        client_socket.send(command.encode('utf-8'))
        
        # 接收文件列表大小
        size_data = client_socket.recv(4)
        size = struct.unpack('!I', size_data)[0]
        
        # 接收文件列表
        file_list_bytes = client_socket.recv(size)
        file_list_str = file_list_bytes.decode('utf-8')
        file_list = file_list_str.split('\n')
        print(f"文件列表: {file_list}")
        client_socket.close()
        file_list = [f for f in file_list if f]
        return f"<div style='color: green;'>连接成功</div>", gr.update(choices=file_list)
    except Exception as e:
        return f"<div style='color: red;'>连接失败: {e}</div>", gr.update(choices=[])

def download_and_show(file_name, host, port):
    print(f"Downloading {file_name} from {host}:{port}")
    try:
        file_path = download_file(file_name=file_name, host=host, port=int(port))
        return "下载成功", file_path
    except Exception as e:
        return f"下载失败: {e}", None


with gr.Blocks() as demo:
    gr.Markdown("# 文件下载器")
    host = gr.Textbox(label="主机")
    port = gr.Number(label="端口")
    connect_output = gr.HTML(label="连接状态")
    connect_btn = gr.Button("测试连接")
    file_list_dropdown = gr.Dropdown(label="文件名", choices=['暂时没有文件'],interactive=True)
    connect_btn.click(test_connection, inputs=[host, port], outputs=[connect_output,file_list_dropdown])
    
    download_btn = gr.Button("下载文件")
    download_output = gr.Textbox(label="下载状态")
    image_preview = gr.Image(label="下载的文件")
    download_btn.click(download_and_show, inputs=[file_list_dropdown, host, port], outputs=[download_output, image_preview])

if __name__ == '__main__':
    demo.launch(server_name="0.0.0.0")