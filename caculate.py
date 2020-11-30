import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import csv

isfirst = True
temp_a = []
temp_b = []
temp_c = []
temp_d = []
f = os.walk('./train_subject/')
if not os.path.exists('./line'):
      os.mkdir('./line')

index = 1
for file in f:
      for files in file[2]:
            index += 1
            tof = open('./line/' + str(files), 'w')
            # 通过read_csv来读取我们的目的数据集
            new_adv_data = pd.read_csv('./train_subject/' + files)
            # 清洗不需要的数据
            # new_adv_data = adv_data.iloc[:, 1:]
            # 得到我们所需要的数据集且查看其前几列以及数据形状
            print('head:', new_adv_data.head(), '\nShape:', new_adv_data.shape)

            # 数据描述
            print(new_adv_data.describe())
            # 缺失值检验
            print(new_adv_data[new_adv_data.isnull() == True].count())

            #new_adv_data.boxplot()
            # plt.savefig("boxplot.jpg")
            # plt.show()
            ##相关系数矩阵 r(相关系数) = x和y的协方差/(x的标准差*y的标准差) == cov（x,y）/σx*σy
            # 相关系数0~0.3弱相关0.3~0.6中等程度相关0.6~1强相关
            print(new_adv_data.corr())

            # 建立散点图来查看数据集里的数据分布
            # seaborn的pairplot函数绘制X的每一维度和对应Y的散点图。通过设置size和aspect参数来调节显示的大小和比例。
            # 可以从图中看出，TV特征和销量是有比较强的线性关系的，而Radio和Sales线性关系弱一些，Newspaper和Sales线性关系更弱。
            # 通过加入一个参数kind='reg'，seaborn可以添加一条最佳拟合直线和95%的置信带。
            #sns.pairplot(new_adv_data, x_vars=['vmaf'], y_vars='score', height=7, aspect=0.8, kind='reg')
            # plt.savefig("pairplot.jpg")
            # plt.show()

            # 利用sklearn里面的包来对数据集进行划分，以此来创建训练集和测试集
            # train_size表示训练集所占总数据集的比例
            X_train, X_test, Y_train, Y_test = train_test_split(new_adv_data.iloc[:, :3], new_adv_data.score.iloc[:],
                                                                train_size=.999)

            real_X_train = []
            real_Y_train = []
            for i in new_adv_data.iloc[0:120, :3]:
                real_X_train.append(i[ :3])
                real_Y_train.append(i[-1])
            print("原始数据特征:", new_adv_data.iloc[:, :3].shape,
                  ",训练数据特征:", X_train.shape,
                  ",测试数据特征:", X_test.shape)

            print("原始数据标签:", new_adv_data.score.shape,
                  ",训练数据标签:", Y_train.shape,
                  ",测试数据标签:", Y_test.shape)

            model = LinearRegression()

            model.fit(X_train, Y_train)

            a = model.intercept_  # 截距

            temp_d.append(a)

            b = model.coef_  # 回归系数

            print("最佳拟合线:截距", a, ",回归系数：", b)
            headers = ['a', 'b', 'c', 'd']
            f_csv = csv.DictWriter(tof, headers)
            rows = []
            rows.append({'a': b[0], 'b': b[1], 'c': b[2], 'd' : a})
            temp_a.append(b[0])
            temp_b.append(b[1])
            temp_c.append(b[2])
            f_csv.writeheader()
            f_csv.writerows(rows)
            tof.close()
            # y=2.668+0.0448∗TV+0.187∗Radio-0.00242∗Newspaper

            # R方检测
            # 决定系数r平方
            # 对于评估模型的精确度
            # y误差平方和 = Σ(y实际值 - y预测值)^2
            # y的总波动 = Σ(y实际值 - y平均值)^2
            # 有多少百分比的y波动没有被回归拟合线所描述 = SSE/总波动
            # 有多少百分比的y波动被回归线描述 = 1 - SSE/总波动 = 决定系数R平方
            # 对于决定系数R平方来说1） 回归线拟合程度：有多少百分比的y波动刻印有回归线来描述(x的波动变化)
            # 2）值大小：R平方越高，回归模型越精确(取值范围0~1)，1无误差，0无法完成拟合
            score = model.score(X_test, Y_test)


            print(score)

            # 对线性回归进行预测

            Y_pred = model.predict(X_test)

            print(Y_pred)

            plt.plot(range(len(Y_pred)), Y_pred, 'b', label="predict")

            # 显示图像
            #plt.savefig("predict.jpg")
            #plt.show()

            #plt.figure()
            #plt.plot(range(len(Y_pred)), Y_pred, 'b', label="predict")
            #plt.plot(range(len(Y_pred)), Y_test, 'r', label="test")
            #plt.legend(loc="upper right")  # 显示图中的标签
            #plt.xlabel("the number of score")
            #plt.ylabel('value of score')
            #plt.savefig("ROC.jpg")
            #plt.show()
#plt.plot(range(len(temp_d)), temp_d, 'b', label="a")
#plt.show()
#plt.plot(range(len(temp_b)), temp_b, 'b', label="b")
#plt.show()
#plt.plot(range(len(temp_c)), temp_c, 'b', label="c")
#plt.show()     # 显示图像
