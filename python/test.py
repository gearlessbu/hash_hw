import matplotlib.pyplot as plt
import numpy as np

# 数据：表格的内容
data = [
    ['UnivMultShift'],
    ['Indpd2MultShift'],
    ['Indpd5MersennePrime'],
    ['SimpleTabulation'],
    ['Indpd5TZTable'],
]

meantimes = np.loadtxt("./tmp/mean_hash_time.txt")
for i in range(5):
    data[i].append(meantimes[i])

# 列标签
columns = ['hashing scheme', 'update time (nanoseconds)']

# 创建一个新的图形
fig, ax = plt.subplots()

# 隐藏轴
ax.axis('off')

# 创建表格并添加到图形中
table = ax.table(cellText=data, colLabels=columns, loc='center')

for (i, j), cell in table.get_celld().items():
    if i > 0:  # 从第一行（数据行）开始
        if j == 0:  # 如果是第一列，去除顶部边框
            cell.set_edgecolor('none')
        else:  # 其他列去除底部边框
            if i != len(data):  # 不影响最后一行
                cell.set_edgecolor('none')

# 显示图形
plt.show()
