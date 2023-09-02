import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler 
import joblib  # 用于加载模型
import os  # 导入os库用于获取当前文件所在文件夹路径
from sklearn.preprocessing import LabelEncoder
from collections import Counter

#不信传不了
# 获取当前文件所在文件夹的路径
current_directory = os.path.dirname(os.path.abspath(__file__))

# 构建模型文件的相对路径
model_filename = 'model2.0.pkl'
model_path = os.path.join(current_directory, model_filename)

test_data = pd.read_csv(r'D:\desktop\NSL-KDD-Dataset-9d544d0eb9b87d7e2f43ff65733bdb644631d12f\KDDTest+.csv', header=None)
# test_data = pd.read_csv(r'D:\desktop\test.csv', header=None)

#预处理数据
# 创建LabelEncoder对象
label_encoder = LabelEncoder()

# 对train_data中的标签进行编码
test_data[1] = label_encoder.fit_transform(test_data[1])
test_data[2] = label_encoder.fit_transform(test_data[2])
test_data[3] = label_encoder.fit_transform(test_data[3])
test_data[41] = label_encoder.fit_transform(test_data[41])


# 划分特征和标签
X_test = test_data.drop([41], axis=1)
y_test = test_data[41]


# 加载已训练的模型
clf = joblib.load(model_path)


# 使用模型进行分类预测
predicted_labels = clf.predict(test_data)

# 标签映射
label_mapping = {
    0: "denign",
    1: "dos",
    2: "u2r",
    3: "r2l",
    4: "probe"
}

# 将数字标签映射为可读标签
predicted_labels_readable = [label_mapping[label] for label in predicted_labels]

# 计算每个可读标签的出现次数
label_counts = Counter(predicted_labels_readable)

# 打印计数结果
print("标签计数结果:")
for label, count in label_counts.items():
    print(f"{label}: 出现次数：{count}")

# 将结果发送到数据库的HTTP接口
database_url = "http://your-database-url.com/api"
data_to_send = {
    "results": label_counts
}

response = requests.post(database_url, json=data_to_send)

# 检查HTTP请求是否成功
if response.status_code == 200:
    print("结果已成功存储到数据库")
else:
    print("存储到数据库时出现错误")
