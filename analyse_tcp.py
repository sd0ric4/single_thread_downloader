# analyze_tcp.py
from scapy.all import *
import matplotlib.pyplot as plt
from scapy.layers.inet import TCP
from scapy.utils import rdpcap

def analyze_pcap(filename):
    # 读取pcap文件
    packets = rdpcap(filename)
    
    # 提取TCP连接建立的包
    syn_packet = None
    syn_ack_packet = None
    ack_packet = None
    
    for packet in packets:
        if TCP in packet:
            if packet[TCP].flags & 0x02:  # SYN
                syn_packet = packet
            elif packet[TCP].flags & 0x12:  # SYN-ACK
                syn_ack_packet = packet
            elif packet[TCP].flags & 0x10:  # ACK
                if syn_ack_packet:  # 确保这是连接建立的ACK
                    ack_packet = packet
                    break

    # 绘制TCP三次握手图
    plt.figure(figsize=(10, 6))
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    times = []
    if syn_packet:
        times.append(syn_packet.time)
    if syn_ack_packet:
        times.append(syn_ack_packet.time)
    if ack_packet:
        times.append(ack_packet.time)
    
    base_time = min(times)
    
    # 画图
    client_y = 1
    server_y = 0
    
    plt.plot([0, 10], [client_y, client_y], 'b-', label='客户端')
    plt.plot([0, 10], [server_y, server_y], 'r-', label='服务器')
    
    # 绘制箭头
    if syn_packet and syn_ack_packet and ack_packet:
        plt.arrow(2, client_y, 0, -0.8, head_width=0.1, head_length=0.1, fc='k', ec='k')
        plt.text(1.5, 0.6, 'SYN', fontsize=10)
        
        plt.arrow(4, server_y, 0, 0.8, head_width=0.1, head_length=0.1, fc='k', ec='k')
        plt.text(3.5, 0.6, 'SYN+ACK', fontsize=10)
        
        plt.arrow(6, client_y, 0, -0.8, head_width=0.1, head_length=0.1, fc='k', ec='k')
        plt.text(5.5, 0.6, 'ACK', fontsize=10)
    
    plt.title('TCP三次握手过程')
    plt.legend()
    plt.axis('off')
    plt.savefig('tcp_handshake.png')
    plt.show()

if __name__ == '__main__':
    analyze_pcap('capture.pcapng')