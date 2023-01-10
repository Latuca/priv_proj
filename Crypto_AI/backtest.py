import pyupbit
import numpy as np
#ohlcv는 당일 open시가,high고가,low저가,close종가,volume 거래량을 의미한다.
df = pyupbit.get_ohlcv("KRW-BTC",count=7)
#변동폭 *k계산,(고가-저가)*k값
df['range'] = (df['high'] - df['low']) * 0.5
#target(매수가),range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005 
#ror(수익률),np.where(조건문,참일떄 값, 거짓일 때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
#누적곱 계산(cumprod) =>누적수익률
df['hpr'] = df['ror'].cumprod()
#Draw Down 계산 (누적 최대 값과 현재 hpr 차이/ 누적  최대값 *100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
#MDD계산
print("MDD(%): ", df['dd'].max())
#엑셀파일로
df.to_excel("dd.xlsx")