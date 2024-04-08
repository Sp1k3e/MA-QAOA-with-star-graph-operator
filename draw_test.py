import matplotlib.pyplot as plt

# 数据
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 6]

# 创建折线图
plt.plot(x, y)

# 添加标题和标签
plt.title('Simple Line Plot')
plt.xlabel('X轴')
plt.ylabel('Y轴')

# 显示图形
plt.show()
