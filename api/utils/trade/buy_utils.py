from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time

m = PyMouse()
k = PyKeyboard()

def clear_ts_code():
    # 双击代码
    m.click(58, 194, 1, 1)
    m.click(159, 195, 1, 2)
    time.sleep(2)
    for i in range(8):
        k.press_key('delete')
    time.sleep(2)


def click_buy(ts_code, count):
    clear_ts_code()
    # 点击买入
    m.click(66, 132, 1, 1)
    # 点击代码
    time.sleep(1)
    m.click(85, 196, 1, 1)
    time.sleep(1)
    k.type_string(ts_code[0:7])
    # 点击数量
    m.click(78, 303, 1, 1)
    time.sleep(1)
    k.type_string(str(count))
    # 确定买入
    time.sleep(1)
    m.click(112, 348, 1, 1)
    time.sleep(1)
    m.click(364, 593, 1, 1)
    m.click(323, 564, 1, 1)

def click_sell(ts_code, count):
    clear_ts_code()
    # 点击买入
    m.click(145, 131, 1, 1)
    # 点击代码
    time.sleep(1)
    m.click(85, 196, 1, 1)
    time.sleep(1)
    k.type_string(ts_code[0:7])
    # 点击数量
    m.click(78, 303, 1, 1)
    time.sleep(1)
    k.type_string(str(count))
    # 确定买入
    time.sleep(1)
    m.click(112, 348, 1, 1)
    time.sleep(1)
    m.click(364, 593, 1, 1)
    m.click(323, 564, 1, 1)
