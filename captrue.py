import pyshark

def packet_callback(packet):
    print(packet)

# 抓取 enp0s31f6 网卡的网络包并保存为 pcap 文件，只过滤端口 11322 的包
capture = pyshark.LiveCapture(interface='any', output_file='capture.pcap', bpf_filter='port 11322')
capture.apply_on_packets(packet_callback)