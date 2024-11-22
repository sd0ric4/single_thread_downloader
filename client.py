import gradio as gr
from utils.receiver import download_file
import socket

def test_connection(host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, int(port)))
        client_socket.close()
        return "<div style='color: green;'>连接成功</div>"
    except Exception as e:
        return f"<div style='color: red;'>连接失败: {e}</div>"

def download_and_show(file_name, host, port):
    download_file(file_name, host, int(port))
    return file_name

with gr.Blocks() as demo:
    gr.Markdown("# 文件下载器")
    host = gr.Textbox(label="主机")
    port = gr.Number(label="端口")
    connect_output = gr.HTML(label="连接状态")
    connect_btn = gr.Button("测试连接")
    connect_btn.click(test_connection, inputs=[host, port], outputs=connect_output)
    
    file_name = gr.Textbox(label="文件名")
    
    download_btn = gr.Button("下载文件")
    download_output = gr.Textbox(label="下载状态")
    download_btn.click(download_and_show, inputs=[file_name, host, port], outputs=download_output)

if __name__ == '__main__':
    demo.launch()