#-*-coding:utf-8 -*-

import pandas as pd
import scapy.all as scapy
import time
import subprocess
import os
from os import popen

# 启动脚本，下面写一个能传参数进来的，要有bat的bin的目录、pcap目录以及csv目录
def get_csv(str_bin, str_pcap, str_csv):
    str_bin2 = replace_(str_bin)
    str_csv2 = replace_(str_csv)
    str_pcap2 = replace_(str_pcap)
    # print(str_bin2)
    os.chdir(str_bin2)
    os.system("cfm.bat "+str_pcap2+" "+str_csv2)


# 一般路径都是\，要替换成/
def replace_(word):
    word2 = word.replace('\\','/')
    return str(word2)

# 抓包持续时间（秒） 默认5s
capture_duration = 5

# 获取当前时间作为文件名前缀
timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
file_prefix = f"capture_{timestamp}"

# 存储抓包数据的列表
captured_packets = []

# 抓包回调函数
def packet_callback(packet):
    if packet.haslayer(scapy.TCP):
        captured_packets.append(packet)

# 启动抓包
print("开始抓包...")
scapy.sniff(prn=packet_callback, timeout=capture_duration)

# 停止抓包
print("停止抓包...")

# 过滤出TCP数据包到PCAP文件,存入：feature_extraction/user_capture
file_name = f"C:/Users/yxy/littleterm/feature_extraction/user_capture/{file_prefix}.pcap"
scapy.wrpcap(file_name, captured_packets) #抓包日志
scapy.wrpcap("C:/Users/yxy/littleterm/feature_extraction/user_packet.pcap", captured_packets) #固定文件，存储每次抓包的数据，覆盖写入

print(f"数据包已保存到 {file_name}")
print(f"总共抓取了 {len(captured_packets)} 个数据包")
print(f"抓包持续时间: {capture_duration} 秒")

# 提取特征
str1 = r"D:\Users\yxy\Microsoft Edge\cicflowmeter-4\CICFlowMeter-4.0\bin" #脚本目录
str2 = r"C:\Users\yxy\littleterm\feature_extraction\user_packet.pcap" #固定存包
str3 = r"C:\Users\yxy\littleterm\feature_extraction\trans_csv"  #特征csv存入目录
get_csv(str1,str2,str3)

# 处理csv
#读取特征csv文件
df = pd.read_csv("C:/Users/yxy/littleterm/feature_extraction/trans_csv/user_packet.pcap_Flow.csv",encoding='gb2312') #默认user_packet.csv

# print(df)

# 删去无用特征
df=df.iloc[:, 4:] #删除前4列

df=df.drop(['Timestamp','Label'],axis=1) # 删去时间戳

#保存最终可用的csv文件
outputpath = 'C:/Users/yxy/littleterm/feature_extraction/data_new.csv'
df.to_csv(outputpath, index=False, mode='w')
