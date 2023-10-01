import numpy as np
import numba 
from numba import jit

# 传入jit，numba装饰器中的一种
@jit(nopython=True) 
def go_fast(a): # 首次调用时，函数被编译为机器代码
    trace = 0.0
    # 假设输入变量是numpy数组
    for i in range(a.shape[0]):   # Numba 擅长处理循环
        trace += np.tanh(a[i, i])  # numba喜欢numpy函数
    return a + trace # numba喜欢numpy广播

# 因为函数要求传入的参数是nunpy数组
x = np.arange(100).reshape(10, 10) 
# 执行函数
go_fast(x)
