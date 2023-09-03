import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from tkinter import font
from ..getPackage import get_label_counts


# 初始化Tkinter窗口
root = tk.Tk()
root.title("加密恶意流量检测系统")
root.geometry("800x600")
custom_font = font.Font(family="SimSun", size=12)  # 使用"SimSun"字体，字号为12

# 加载背景图片
bg_image = Image.open(r"D:\desktop\tryit.png")  # 请将图片文件名替换为实际的图片文件
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# 创建一个标签来显示标题
title_label = tk.Label(root, text="加密恶意流量检测系统", font=("Times New Roman", 40, "bold"), fg="white", bg="black")
title_label.pack(pady=20)

# 创建一个框架来容纳按钮和图表
frame = tk.Frame(root, bg="black")
frame.pack()

# 定义一个函数来处理上传文件
def upload_file():
    file_path = filedialog.askopenfilename(title="选择要上传的文件")
    if file_path:
        # 在此处添加处理文件的代码
        messagebox.showinfo("上传成功", "文件已成功上传")

# 创建上传按钮
upload_button = tk.Button(frame, text="上传pcap", command=upload_file, padx=10, pady=5, bg="#045104", fg="white")
upload_button.grid(row=0, column=0, padx=10)

# 创建开始抓包按钮
start_button = tk.Button(frame, text="开始抓包", padx=10, pady=5, bg="#045104", fg="white")
start_button.grid(row=0, column=1, padx=10)

# 创建停止抓包按钮
stop_button = tk.Button(frame, text="停止抓包", padx=10, pady=5, bg="#045104", fg="white")
stop_button.grid(row=0, column=2, padx=10)

# 创建一个空的图表区域
chart_frame = tk.Frame(root, bg="black")
chart_frame.pack(expand=True, fill="both")

# 在图表区域添加Matplotlib图表
def update_pie_chart(data):
    labels = data.keys()
    values = data.values()
    
    plt.figure(figsize=(6, 4))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=["#669fef", "#f3cf2b", "#e6eaf0", "#fe8839", "#5470c6"])
    plt.title("恶意行为分类统计图", fontsize=16)
    
    canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_frame)
    canvas.get_tk_widget().pack(expand=True, fill="both")
    canvas.draw()


# 模拟后端数据
backend_data = {
    'benign': 10,
    'dos': 10,
    'u2r': 10,
    'r2l': 10,
    'probe': 10
}

backend_data=get_label_counts()

# 更新图表
update_pie_chart(backend_data)

# 运行Tkinter主循环
root.mainloop()
