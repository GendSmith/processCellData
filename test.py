import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# 生成两组离散点
x1 = (0,1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9)
y1 = np.array([3, 4, 5, 6, 5, 8, 10, 15, 7, 5])

x2 = (0.1,2.4,4.1,6.0,8.6)
y2 = np.array([1, 2, 1, 1, 2])

# 绘制两个折线图
plt.plot(x1, y1, label='y1')
plt.plot(x2, y2, label='y2')

# 对第二个折线图进行插值
f = interp1d(x2, y2, kind='linear')

# 将 x1 的值限制在 x2 的范围内
x1_clipped = np.clip(x1, np.min(x2), np.max(x2))

# 计算插值值
y2_interp = f(x1_clipped)

print('y1',y1)
print('y2_interp:',y2_interp)

plt.plot(x1_clipped, y2_interp, label='y2_interp')

# 计算两个折线图的差值
y_diff = y1 - y2_interp

# 绘制新的折线图
plt.plot(x1, y_diff, label='y1 - y2')

# 显示图例和图形
plt.legend()
plt.show()