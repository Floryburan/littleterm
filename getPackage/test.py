import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler 
import joblib  # 用于加载模型
import os  # 导入os库用于获取当前文件所在文件夹路径
from sklearn.preprocessing import LabelEncoder
#不信传不了
# 获取当前文件所在文件夹的路径
current_directory = os.path.dirname(os.path.abspath(__file__))

# 构建模型文件的相对路径
model_filename = 'model2.0.pkl'
model_path = os.path.join(current_directory, model_filename)

test_data = pd.read_csv(r'D:\desktop\test.csv', header=None)

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


# 假设你已经有了一个训练好的模型 clf 和相应的特征提取代码

# 创建一个DataFrame来存储现实抓到的数据包的特征
# 特征列的顺序和格式需要与训练数据集相匹配
# real_data = pd.DataFrame({
#     'Feature1': [0,'tcp','private','REJ',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,229,10,0.00,0.00,1.00,1.00,0.04,0.06,0.00,255,10,0.04,0.06,0.00,0.00,0.00,0.00,1.00,1.00,'neptune',21],  # 依次填充你的特征值
#     'Feature2': [0,'tcp','private','REJ',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,136,1,0.00,0.00,1.00,1.00,0.01,0.06,0.00,255,1,0.00,0.06,0.00,0.00,0.00,0.00,1.00,1.00,'neptune',21],
#     # 添加更多特征列
# })



# 使用模型进行分类预测
predicted_labels = clf.predict(test_data)

# 打印分类结果
print("分类结果:")
for label in predicted_labels:
    print(label)

