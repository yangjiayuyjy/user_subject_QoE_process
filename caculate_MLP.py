import os
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import csv

isfirst = True
temp_a = []
temp_b = []
temp_c = []
temp_d = []
f = os.walk('./new_seven_input/')
if not os.path.exists('./MLP'):
      os.mkdir('./MLP')



from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import numpy as np  

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true-y_pred)**2))


index = 1
loss = 0
ave_loss = 0
models = []
X_Y = []

test = []
for file in f:
      for files in file[2]:
            # 通过read_csv来读取我们的目的数据集
            new_adv_data = pd.read_csv('./new_seven_input/' + files)
            #排除最后一个数据集
            if files == 'subject66.csv':
                X_train = new_adv_data.iloc[:, :7]
                Y_train = new_adv_data.score
                ave_model = make_pipeline(StandardScaler(),
                                      MLPRegressor(hidden_layer_sizes=(5,6,5),
                                                   tol=1e-10, max_iter=10000, random_state=0))
                ave_model.fit(X_train, Y_train)
                models.append(ave_model)
                temp = models[0].predict(test[0])
                loss = rmse(Y_train, models[0].predict(X_train))
                print(loss / (index - 1))
                loss = rmse(Y_train, models[-1].predict(X_train))

                temp_Y = models[-1].predict(X_train)
                print(temp_Y)
                print(loss / (index - 1))
                continue
            index += 1

            if files == 'subject2.csv':
                X_train = new_adv_data.iloc[:, :7]
                Y_train = new_adv_data.score
                ave_model = make_pipeline(StandardScaler(),
                                      MLPRegressor(hidden_layer_sizes=(5,6,5),
                                                   tol=1e-10, max_iter=10000, random_state=0))
                ave_model.fit(X_train, Y_train)
                models.append(ave_model)
                temp = models[0].predict(test[0])
                loss = rmse(Y_train, models[0].predict(X_train))
                print(loss / (index - 1))
                loss = rmse(Y_train, models[-1].predict(X_train))

                temp_Y = models[-1].predict(X_train)
                print(temp_Y)
                print(loss / (index - 1))
                continue
            index += 1
            # 清洗不需要的数据
            # new_adv_data = adv_data.iloc[:, 1:]
            # 得到我们所需要的数据集且查看其前几列以及数据形状


            # 建立散点图来查看数据集里的数据分布
            # seaborn的pairplot函数绘制X的每一维度和对应Y的散点图。通过设置size和aspect参数来调节显示的大小和比例。
            # 可以从图中看出，TV特征和销量是有比较强的线性关系的，而Radio和Sales线性关系弱一些，Newspaper和Sales线性关系更弱。
            # 通过加入一个参数kind='reg'，seaborn可以添加一条最佳拟合直线和95%的置信带。
            #sns.pairplot(new_adv_data, x_vars=['vmaf'], y_vars='score', height=7, aspect=0.8, kind='reg')
            # plt.savefig("pairplot.jpg")
            # plt.show()

            # 利用sklearn里面的包来对数据集进行划分，以此来创建训练集和测试集
            # train_size表示训练集所占总数据集的比例
            X_train, X_test, Y_train, Y_test = train_test_split(new_adv_data.iloc[:, :7], new_adv_data.score,
                                                                train_size=.999)
            test.append(X_test)
            test.append(Y_test)

            #MLP的方法
            model = make_pipeline(StandardScaler(),
                                 MLPRegressor(hidden_layer_sizes=(6,6,4),
                                             tol=1e-10, max_iter=10000, random_state=0))
            #linear 
            # model = LinearRegression()

            model.fit(X_train, Y_train)
            tran_data = [X_train, Y_train]
            X_Y.append(tran_data)
            models.append(model)


loss = rmse(test[1], models[0].predict(test[0]))
ave_loss = rmse(test[1], models[-1].predict(test[0]))

temp_Y = models[-1].predict(test[0])

print(temp_Y)

processed_data = pd.DataFrame({'predict': models[0].predict(X_Y[0][0]),
                               'ave_predict': models[-1].predict(test[0]),
                               'real': test[1]})
rr = processed_data.corr('spearman')
predicts = list(rr.get('predict'))
ave_predict = list(rr.get('ave_predict'))

print(rr)

print(loss / (index-1))
print(ave_loss / (index-1))







