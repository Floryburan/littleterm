import scapy.all as scapy
from threading import Thread

# 全局变量用于标志是否停止抓包
stop_sniffing = False

# 计数器用于统计抓到的总包数、加密包数和非加密包数
total_packets = 0
encrypted_packets = 0
unencrypted_packets = 0

def start_sniffing(interface):
    global stop_sniffing
    global total_packets
    global encrypted_packets
    global unencrypted_packets

    # 使用多线程运行抓包功能
    def sniff_packets(interface):
        global stop_sniffing
        global total_packets
        global encrypted_packets
        global unencrypted_packets

        while not stop_sniffing:
            try:
                packet = scapy.sniff(iface=interface, count=1)[0]
                total_packets += 1

                # 在这里添加检测加密流量的逻辑
                # 示例中假设加密流量的判断条件是是否有SSL/TLS协议层
                if packet.haslayer(scapy.TLS):

                    encrypted_packets += 1
                else:
                    unencrypted_packets += 1

            except Exception as e:
                pass

    # 启动抓包线程
    sniff_thread = Thread(target=sniff_packets, args=(interface,))
    sniff_thread.start()

def stop_sniffing_packets():
    global stop_sniffing
    stop_sniffing = True

def main():
    interface = "WLAN"  # 替换为你的网络接口，例如"eth0"

    start_sniffing(interface)
    input("按下回车键停止抓包...")
    stop_sniffing_packets()

    print(f"抓包总数: {total_packets}")
    print(f"加密流量包数: {encrypted_packets}")
    print(f"非加密流量包数: {unencrypted_packets}")

if __name__ == "__main__":
    main()
