import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import joblib 

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus']=False
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 读取训练集和测试集数据
train_data = pd.read_csv(r"D:\desktop\NSL-KDD-Dataset-9d544d0eb9b87d7e2f43ff65733bdb644631d12f\KDDTrain+.TXT", header=None)
test_data = pd.read_csv(r"D:\desktop\NSL-KDD-Dataset-9d544d0eb9b87d7e2f43ff65733bdb644631d12f\KDDTest+.TXT", header=None)
train_data.head()

aim_type={
    'benign':['normal'],
    'dos':['apache2','back','land','mailbomb','neptune','pod','processtable','smurf','teardrop','udpstorm','snmpgetattack'],
    'u2r':['buffer_overflow','httptunnel','loadmodule','perl','ps','rootkit','sqlattack','xterm'],
    'r2l':['ftp_write','guess_passwd','imap','multihop','named','phf','sendmail','snmpgetattack','snmpguess','spy','warezclient','warezmaster','worm','xlock','xsnoop'],
    'probe':['ipsweep','mscan','nmap','portsweep','saint','satan','worm']
}

# 将数据集中的攻击类型进行分类
def attack_type(x):
    if x in aim_type['benign']:
        return 'benign'
    elif x in aim_type['dos']:
        return 'dos'
    elif x in aim_type['u2r']:
        return 'u2r'
    elif x in aim_type['r2l']:
        return 'r2l'
    elif x in aim_type['probe']:
        return 'probe'
    else:
        return 'unknown'

# 将数据集中的攻击类型进行分类
train_data[41] = train_data[41].apply(attack_type)
test_data[41] = test_data[41].apply(attack_type)

train_data.head()

# 示例预处理代码：
from sklearn.preprocessing import LabelEncoder

# 创建LabelEncoder对象
label_encoder = LabelEncoder()

# 对train_data中的标签进行编码
train_data[1] = label_encoder.fit_transform(train_data[1])
train_data[2] = label_encoder.fit_transform(train_data[2])
train_data[3] = label_encoder.fit_transform(train_data[3])
train_data[41] = label_encoder.fit_transform(train_data[41])

# 对test_data中的标签进行编码
test_data[1] = label_encoder.fit_transform(test_data[1])
test_data[2] = label_encoder.fit_transform(test_data[2])
test_data[3] = label_encoder.fit_transform(test_data[3])
test_data[41] = label_encoder.fit_transform(test_data[41])


# 划分特征和标签
X_train = train_data.drop([41], axis=1)
y_train = train_data[41]

X_test = test_data.drop([41], axis=1)
y_test = test_data[41]

# # 输出训练集和测试集的标签的分布
# print('训练集中各类标签的分布：')
# print(y_train.value_counts())
# print('测试集中各类标签的分布：')
# print(y_test.value_counts())

from sklearn.preprocessing import MinMaxScaler 

# 缩放处理，归一化
scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# XGBoost
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error,f1_score,roc_auc_score
from sklearn import metrics
from math import sqrt
# 混淆矩阵
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# XGBoost建模
# 设置参数
param = {'n_estimators':range(10,101,50),
        'max_depth':range(4,6,1),
        'min_child_weight':range(4,6,1) ,
        'gamma':[i / 10.0 for i in range(0,3)]
}
# XGBoost训练建模
reg = XGBClassifier(n_estimators=100,learning_rate=0.1,random_state=42)
# 网格搜索最佳参数，交叉验证设为5折
clf = GridSearchCV(reg, param, cv = 5)
# 开始训练
clf.fit(X_train_scaled, y_train) 

# 最佳效果进行预测
y_pred = clf.predict(X_test_scaled)


# 输出算法效果指标，最佳参数
print("Best parameters: {}".format(clf.best_params_)) 
print("Accuracy on training set: {:.3f}".format(clf.score(X_train_scaled, y_train))) 
print("Accuracy on test set: {:.3f}".format(clf.score(X_test_scaled, y_test)))
print("RMSE score : {:.3f}".format(sqrt(mean_squared_error(y_test, y_pred))))
print("R2 score : {:.3f}".format(r2_score(y_test, y_pred)))
print("MAE score : {:.3f}".format(mean_absolute_error(y_test, y_pred)))

print("Confusion matrix: \n",confusion_matrix(y_pred,y_test))
print("Classification report: \n",classification_report(y_pred,y_test))

joblib.dump(clf,r'D:\desktop\model2.0')