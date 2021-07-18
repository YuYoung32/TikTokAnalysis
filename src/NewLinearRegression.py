# -*-coding:utf-8-*-
import numpy as np
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime

#######################################
#开始预处理处理数据
#读取粉丝增长量
filename= '/data/人民日报3月粉丝增长数据.csv'
with open(filename,encoding='utf-8-sig') as f: #打开这个文件，并将结果文件对象存储在f中
    reader=csv.reader(f)  #创建一个阅读器reader
    header_row=next(reader) #返回文件中的下一行
    newfans=[]      #声明新增粉丝的列表
    for row in reader:
        newfan=int(row[1])    #将字符串转换为数字
        newfans.append(newfan)   #存储新增粉丝
#读取分享，评论，转发数据
filename= '/data/人民日报3月份视频数据.csv'
with open(filename,encoding='utf-8-sig') as f: #打开这个文件，并将结果文件对象存储在f中
    reader=csv.reader(f)  #创建一个阅读器reader
    header_row=next(reader) #返回文件中的下一行
    dates,likes,comments,shares=[], [] ,[] ,[]    #声明存储日期，新增粉丝的列表
    for row in reader:
        current_date = datetime.strptime(row[3], '%Y/%m/%d %H:%M')  # 将日期数据转换为datetime对象
        current_date = current_date.strftime('%Y/%m/%d')  # 截取到天
        dates.append(current_date)  # 日期
        like = int(row[0])
        likes.append(like)  #点赞
        comment = int(row[1])
        comments.append(comment)    #评论
        share = int(row[2])
        shares.append(share)    #转发

#处理数据（按天）
cnts = []
distinct_dates = list(set(dates))
distinct_dates.sort(reverse = True)
for date in distinct_dates:
    cnt = 0
    for temp_date in dates:
        if temp_date == date:
            cnt = cnt + 1
    cnts.append(cnt)
sum_likes, sum_comments, sum_shares = [],[],[]
'''test module
print(likes)
print(len(shares))
print(cnts)
print(dates)
test all OK'''
#处理同一天的点赞
flag = 0
for cnt in cnts:
    count = 0
    sum_like = 0
    while count < cnt:  #对同一天的数量进行相加
        count = count + 1
        sum_like += likes[flag]
        flag = flag + 1;
    sum_likes.append(sum_like)
#处理同一天的评论
flag = 0
for cnt in cnts:
    count = 0
    sum_comment = 0
    while count < cnt:  #对同一天的数量进行相加
        count = count + 1
        sum_comment += comments[flag]
        flag = flag + 1;
    sum_comments.append(sum_comment)
#处理同一天的转发
flag = 0
for cnt in cnts:
    count = 0
    sum_share = 0
    while count < cnt:  #对同一天的数量进行相加
        count = count + 1
        sum_share += shares[flag]
        flag = flag + 1;
    sum_shares.append(sum_share)
#导出数据
with open('../ProcessedData.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['likes', 'comments', 'shares', 'date'])
    temp_list = []
    cnt = 0
    while cnt < 31:
        cnt = cnt + 1
        temp_list.append([likes[cnt], comments[cnt], shares[cnt], dates[cnt]])
    writer.writerows(temp_list)
#归一化
max_likes = max(sum_likes)
max_comments = max(sum_comments)
max_shares = max(sum_shares)
max_newfans = max(newfans)
cnt = 0
while cnt < 31:
    sum_likes[cnt] = sum_likes[cnt]/max_likes
    sum_comments[cnt] = sum_comments[cnt]/max_comments
    sum_shares[cnt] = sum_shares[cnt]/max_shares
    newfans[cnt] = newfans[cnt]/max_newfans
    cnt = cnt + 1
#预处理数据完成
#得到每天的点赞 sum_likes
#得到每天的评论 sum_comments
#得到每天的转发 sum_shares
'''test module
print(sum_likes)
print(len(sum_likes))
print(len(sum_comments))
print(len(sum_shares))
长度都为31
test all OK'''

#######################################
#开始多线性拟合

print(distinct_dates)
y = newfans
x = np.column_stack((sum_likes, sum_comments, sum_shares))
x_n = sm.add_constant(x)  # statsmodels进行回归
model = sm.OLS(y, x_n)  # model是回归分析模型
results = model.fit()  # results是回归分析后的结果
# 输出结果
print(results.summary())
print('Parameters: ', results.params)
print('R2: ', results.rsquared)
#绘图
fig=plt.figure(figsize=(16, 9))
plt.title("LinearRegression")
plt.xlabel("Date")
plt.ylabel("Amount")

y_fitted = results.fittedvalues
y_fitted_max = max(y_fitted)
for index in range(len(y_fitted)):
    y_fitted[index] = y_fitted[index]/y_fitted_max
l1, = plt.plot(distinct_dates, sum_likes, marker="o",color="red",alpha = 0.5,label = 'likes')  #散点图
l2, = plt.plot(distinct_dates, sum_comments, marker="o",color="green",alpha = 0.5)
l3, = plt.plot(distinct_dates, sum_shares, marker="o",color="blue",alpha = 0.5)
l4, = plt.plot(distinct_dates, newfans, marker="o",color="pink",alpha = 0.5)
l5, = plt.plot(distinct_dates, y_fitted, marker="o",color="black")
plt.legend([l1,l2,l3,l4,l5],['Likes','Comments','Shares','Newfans', 'FittedNewFans'],loc='upper right')
fig.autofmt_xdate()
plt.show()

