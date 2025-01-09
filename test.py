import os
from dotenv import load_dotenv
load_dotenv()


# 1. 업비트 차트 데이터 가져오기(30일봉)
import pyupbit
df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")
# print(df.tail())

# 2. 로그인
access = os.getenv("UPBIT_ACCESS_KEY")
secret = os.getenv("UPBIT_SECRET_KEY")
upbit = pyupbit.Upbit(access,secret)

# 자산조회
print("내 원화 조회 : ")  
print(upbit.get_balance("KRW"))  

# 3. 자동매매


