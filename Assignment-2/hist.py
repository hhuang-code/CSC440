"""
Used in ex 3.11-(a)
In terminal, type "python hist.py"
"""

import matplotlib.pyplot as plt
import numpy as np

data = np.array([13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33, 35, 35, 35, 35, 36, 40, 45, 46, 52, 70]);
binwidth = 10
plt.hist(data, bins = range(10, 70 + binwidth, binwidth), ls='dotted', lw = 3, alpha = 0.5)
plt.xticks(np.arange(10, 70 + 1, 5))
plt.yticks(np.arange(0, 12, 1))
plt.grid()
plt.title('Histogram with width = 10')
plt.show()
