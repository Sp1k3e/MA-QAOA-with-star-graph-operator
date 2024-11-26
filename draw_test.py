import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 示例数据
data = {
    'Group': ['A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B'],
    'Values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 创建图形和轴
plt.figure()

# 使用seaborn的boxplot方法绘制箱线图
sns.boxplot(x='Group', y='Values', data=df)

# 设置标题和标签
plt.title('Multiple Box Plots with Seaborn')
plt.ylabel('Value')

# 显示图形
plt.show()