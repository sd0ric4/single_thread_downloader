from scapy.all import *
import matplotlib.pyplot as plt

pcap_path = "capture.pcap"  # 数据包路径
packets = rdpcap(pcap_path)  # 读取数据包

plt.figure(figsize=(10, 8))  # 设置figure大小
# 隐藏边框
plt.gca().spines["top"].set_alpha(.0)
plt.gca().spines["bottom"].set_alpha(.0)
plt.gca().spines["right"].set_alpha(.0)
plt.gca().spines["left"].set_alpha(.0)
plt.title("TCP connection", fontsize=18)  # 添加标题
plt.axis([0, 10, 0, 10])  # 横纵坐标范围
plt.xticks([1, 9], [packets[0]["IP"].src, packets[0]["IP"].dst])  # 添加横坐标标签
plt.yticks([])  # 隐藏纵坐标标签
# 两条竖线
plt.vlines(x=1, ymin=0, ymax=10, linestyles='dotted')
plt.vlines(x=9, ymin=0, ymax=10, linestyles='dotted')
# 添加文字
plt.text(1, 10, 'Client', horizontalalignment='center', fontsize=15)
plt.text(9, 10, 'Server', horizontalalignment='center', fontsize=15)

client_ip = packets[0]["IP"].src
for i in range(len(packets)):  # 对每一个数据包的数据进行处理
    if packets[i]["IP"].src == client_ip:  # 如果是从客户端发往服务器
        p1 = [1, 9 - 2 * i]
        p2 = [9, 9 - 2 * i - 1]
    else:  # 如果是从服务器发往客户端
        p1 = [9, 9 - 2 * i]
        p2 = [1, 9 - 2 * i - 1]
    # 画一条带箭头的线
    plt.arrow(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1],
              length_includes_head=True,  # 长度包含箭头部分
              head_width=0.1, head_length=0.2, color='black')  # 箭头的长宽和颜色
    # 添加数据信息
    message = 'sport=' + str(packets[i]["TCP"].sport) + ',' + 'dport=' + str(packets[i]["TCP"].dport) + ',' + 'seq=' + str(packets[i]["TCP"].seq) + ',' + 'ack=' + str(packets[i]["TCP"].ack) + ',' + 'flags=' + str(packets[i]["TCP"].flags)
    plt.text(5, p1[1], message, horizontalalignment='center', fontsize=10)

plt.savefig("TCP_connection.png")  # 保存图片