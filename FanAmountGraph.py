import matplotlib.pyplot as plt
import csv
from datetime import datetime

filename='D:\PyCharmFiles\TikTokAnalysis\data\人民日报3月粉丝增长数据.csv'
origin = 122747343
with open(filename,encoding='utf-8-sig') as f: #打开这个文件，并将结果文件对象存储在f中
    reader=csv.reader(f)  #创建一个阅读器reader
    header_row=next(reader) #返回文件中的下一行
    dates,newfans=[],[]      #声明存储日期，新增粉丝的列表
    for row in reader:
        current_date= datetime.strptime(row[0],'%Y-%m-%d')  #将日期数据转换为datetime对象
        dates.append(current_date)    #存储日期
        newfan=int(row[1]) #将字符串转换为数字
        newfan = newfan + origin
        newfans.append(newfan)   #存储粉丝

#根据数据绘制图形
fig=plt.figure(dpi=128,figsize=(10,6))
plt.plot(dates,newfans,c='red',alpha = 0.6)#实参alpha指定颜色的透明度，0表示完全透明，1（默认值）完全不透明
plt.fill_between(dates,newfans,facecolor='blue',alpha = 0.8) #给图表区域填充颜色
plt.title('Fan Amount',fontsize=24)
plt.xlabel('Date',fontsize=16)
plt.ylabel('Amount',fontsize=16)
plt.tick_params(axis='both',which='major',labelsize=16)#刻度设置
fig.autofmt_xdate()  #绘制斜的日期标签
plt.show()