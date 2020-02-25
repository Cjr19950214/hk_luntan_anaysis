import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib.dates import AutoDateLocator, DateFormatter  

gd_data = pd.read_csv('basic_info.csv')
fig = plt.figure(figsize=(10, 6))
ax1 = plt.subplot(111)

ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))  #设置时间显示格式
ax1.xaxis.set_major_locator(AutoDateLocator(maxticks=13)) #设置时间间隔  12个月的数据会有13个点

#设置标题
ax1.set_title('Scatter Plot')
#设置X轴标签
ax1.set_xlabel('time', fontsize=18,fontfamily = 'sans-serif',fontstyle='italic')
#设置Y轴标签
ax1.set_ylabel('comment_num', fontsize=18,fontfamily = 'sans-serif',fontstyle='italic')
ax1.grid(True) ##增加格点
#画散点图
ax1.scatter(pd.to_datetime(gd_data['launch_time']),gd_data["comment_num"],c = 'r',marker = '.')

#设置图标
for label in ax1.get_xticklabels():
    label.set_rotation(60)
    label.set_horizontalalignment('right')
# ax1.legend('post')
ax1.set_xlim(pd.to_datetime('2019-01-01'),pd.to_datetime('2020-01-01'))
plt.yticks(range(0,10000,500)) #设置y轴刻度密度，范围
ax1.set_ylim(ymin=0) #将y轴坐标的起点设置为0点，为了跟x轴原点重合
#显示所画的图
plt.show()
