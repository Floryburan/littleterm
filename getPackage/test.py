import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler 
import joblib  # 用于加载模型
import os  # 导入os库用于获取当前文件所在文件夹路径
from sklearn.preprocessing import LabelEncoder
from collections import Counter
# import requests
from collections import Counter

#不信传不了
# 获取当前文件所在文件夹的路径
current_directory = os.path.dirname(os.path.abspath(__file__))

# 构建模型文件的相对路径
model_filename = 'model4.0.pkl'
model_path = os.path.join(current_directory, model_filename)

# # 构建测试数据文件的相对路径
# test_filename = 'test.csv'
# test_path = os.path.join(current_directory, test_filename)

# # 读取测试数据文件
# test_data = pd.read_csv(test_path, header=None)
# 读取测试数据文件
test_data_new = pd.read_csv(r"E:\系统默认\文档\WeChat Files\wxid_ibj2zc64e7ug32\FileStorage\File\2023-09\data_new(2).csv", header=None,skiprows=1)

# test_data = test_data_new.iloc[1:]
# 替代清洗策略示例
test_data_new_cleaned = test_data_new.replace([np.inf, -np.inf], np.nan).fillna(9999999)

# 缩放处理，归一化
scaler = MinMaxScaler()
scaler.fit(test_data_new_cleaned)
X_test_new_scaled = scaler.transform(test_data_new_cleaned)


# 加载已训练的模型
clf = joblib.load(model_path)

# 使用已经训练好的模型对测试数据进行预测
y_pred_new = clf.predict(X_test_new_scaled)

# # 输出测试结果
# print('测试结果：')
# print(y_pred_new)

# 创建LabelEncoder对象
label_encoder = LabelEncoder()


# 标签映射
label_mapping = {
    0: "Benign",
    1: "Dos",
    2: "Ddos",
    3: "Bot",
    4: "Bruteforce",
    5: "Infilteration",
    6: "unknow"
}

# 将数字标签映射为可读标签
predicted_labels_readable = [label_mapping[label] for label in y_pred_new]

# 计算每个可读标签的出现次数
label_counts = Counter(predicted_labels_readable)

# 打印计数结果
print("标签计数结果:")
for label, count in label_counts.items():
    print(f"{label}: 出现次数：{count}")

# # 将结果发送到数据库的HTTP接口
# database_url = "http://192.168.211.1:5000//calculate"
# data_to_send = {
#     "results": label_counts
# }

# response = requests.post(database_url, json=data_to_send)

# # 检查HTTP请求是否成功
# if response.status_code == 200:
#     print("结果已成功存储到数据库")
# else:
#     print("存储到数据库时出现错误")
