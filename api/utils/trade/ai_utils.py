import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import deque
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import datetime
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
import tushare as ts
from tensorflow.keras.models import load_model

pro = ts.pro_api('3cb9379a9a4f25f917b9f7cf73030848f2922944e98a52e3b5686b90')


class StockPrediction(object):
    def __init__(self, ts_code, pre_days=10, men_his_days=5, test_day=100):
        self.test_day = test_day
        self.men_his_days = 5
        self.pre_days = 10
        path = './media/ai_code/1/mycode1/'
        self.filepath = path + 'model/train_params.h5'

        self.checkpoint = ModelCheckpoint(
            filepath=self.filepath,
            save_weights_only=False,
            monitor='val_mape',
            mode='min',
            save_best_only=True
        )
        # 模型路径
        # 获取基础数据
        self.stock = self.get_dataset(ts_code, pre_days)
        # 数据标准化
        self.standard = self.Stock_Price_LSTM_Data_Precesing(men_his_days, pre_days)
        # X:预测，y:结果，X_lately:剩余的
        self.X, self.y, self.X_lately = self.standard
        # 划分
        # self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.1)
        self.X_train = self.X[:-self.test_day]
        self.X_test = self.X[-self.test_day:]
        self.y_train = self.y[:-self.test_day]
        self.y_test = self.y[-self.test_day:]
        #
        self.df_time = self.stock.index[-len(self.y_test):]
        # 加载最好模型
        self.best_model = None
        self.pre = None
        try:
            self.best_model = load_model(self.filepath)
            # 预测测试
            self.pre = self.best_model.predict(self.X_test)
        except Exception:
            self.train()
        # 设置保存方式

    def get_dataset(self, ts_code, pre_days):
        df = pro.daily(ts_code=ts_code, fields=["trade_date", "open", "high", "low", "close", "vol", "amount"])
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df['trade_date'] = df['trade_date'].dt.strftime('%Y-%m-%d')
        df = df.set_index('trade_date')
        df = df.sort_index(ascending=True)
        # label: 10天后的价格
        df['label'] = df['close'].shift(-pre_days)
        return df

    # 进行数据标准化
    def Stock_Price_LSTM_Data_Precesing(self, men_his_days, pre_days):
        scaler = StandardScaler()
        sca_X = scaler.fit_transform(self.stock.iloc[:, :-1])
        deq = deque(maxlen=men_his_days)
        X = []
        for i in sca_X:
            deq.append(list(i))
            if len(deq) == men_his_days:
                X.append(list(deq))
        X_lately = X[-pre_days:]
        #
        X = X[:-pre_days]

        y = self.stock['label'].values[men_his_days - 1:-pre_days]
        X = np.array(X)
        y = np.array(y)
        return X, y, X_lately

    def train(self, units=32):
        model = Sequential()
        model.add(LSTM(units, input_shape=self.X.shape[1:], activation='relu', return_sequences=True))
        model.add(Dropout(0.1))
        #
        model.add(LSTM(units, activation='relu', return_sequences=True))
        model.add(Dropout(0.1))
        #
        model.add(LSTM(units, activation='relu'))
        model.add(Dropout(0.1))
        #
        model.add(Dense(units, activation='relu'))
        model.add(Dropout(0.1))
        #
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse', metrics=['mape'])
        #
        model.fit(self.X_train, self.y_train, batch_size=32, epochs=1, validation_data=(self.X_test, self.y_test),
                  callbacks=[self.checkpoint])

        self.best_model = load_model(self.filepath)
        # 预测测试
        self.pre = self.best_model.predict(self.X_test)

    def test(self):
        pass

    def forecast(self):
        pass

    def draw_picture(self):
        plt.plot(self.df_time, self.y_test, color='red', label='price')
        plt.plot(self.df_time, self.pre, color='green', label='predict')
        plt.show()

    def return_predict(self):
        return {
            'time': self.df_time.tolist(),
            'y_test': self.y_test.tolist(),
            'predict': self.pre.T.tolist()[0]
        }

    def lately_day(self):
        X_l = self.best_model.predict(self.X_lately)
        X_z = self.stock.iloc[-self.pre_days:]
        plt.figure()
        plt.plot(self.df_time, X_l, color='red', label='price')
        plt.plot(self.df_time, X_z, color='green', label='predict')
        plt.show()
        pass

    def get_summary(self):
        return self.best_model.summary()
        pass


sp = StockPrediction('000001.SZ')
res1 = sp.return_predict()
res2 = sp.get_summary()
