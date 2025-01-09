import pyupbit
import talib
import os
from dotenv import load_dotenv
import pyupbit.websocket_api as wsck
load_dotenv()

access = os.getenv("UPBIT_ACCESS_KEY")
secret = os.getenv("UPBIT_SECRET_KEY")

BTC = "KRW-BTC"
ETH = "KRW-ETH"
XRP = "KRW-XRP"
STX = "KRW-STX"

coin = STX
min = "minute5"

# 업비트 로그인 #
# access = os.getenv("UPBIT_ACCESS_KEY")
# secret = os.getenv("UPBIT_SECRET_KEY")
# upbit = pyupbit.Upbit(access,secret)

# RSI지표 함수 #
def RSI(coin, min ,period=14) : 
    rdf = pyupbit.get_ohlcv(coin, min, 100)
    rdf['rsi'] = talib.RSI(rdf.close)
    numlist = []

    for i in range(len(rdf)):
        numlist.append(i)
    numlist.reverse()
    rdf['num'] = numlist

    return rdf

if __name__ == "__main__" :
    # while True:
    try :
        wm = wsck.WebSocketManager("ticker", ["KRW-STX" , ]) # 통신연결
        for i in range(5):
            data = wm.get()
            print(i, data['trade_price']) # 실시간 시세
            # 로직 
            # 1. RSI 지표 조회
            df = RSI(coin, min)
            print(df)
            rsiNum = df['rsi'].loc[(df.rsi<=30) & (df.num == 0)].values
            if len(rsiNum) > 0 :
                print("RSI 지표 : " , rsiNum[0])
                # 매수
                upbit = pyupbit.Upbit(access,secret)
                myKRW = upbit.get_balance("KRW") # 잔고조회
                print("잔고 : " , myKRW)

                # 수량 구하기 (분할매수시 10만원 단위)
                if data['trade_price'] != None:
                    ea = float(float(100000.0 / float(data['trade_price'])))
                    ea = round(ea,8)
                    print("수량 : ", ea)
                    if float(data['trade_price'])*ea > 5000 :
                        print(upbit.buy_limit_order(coin , float(data['trade_price']), ea ))
                        print("buy!! ")
                    else :
                        print("5000원 미만!! ")
        
        wm.terminate() # 통신종료

    except Exception as e:
        print(e)
        wm.terminate() # 통신종료
    

    '''
    # 5분봉 조회
    minute5 = pyupbit.get_ohlcv(coin, "minute5", 200)

    rsiDf = RSI(minute5)
    print(rsiDf)
    # if result['decision'] == 'buy':
    lastRSI = rsiDf['rsi'].loc[(rsiDf.rsi<=30) & (rsiDf.num == 0)].values # rsi 20 이하 구하기
    lastClose = rsiDf['close'].loc[(rsiDf.rsi<=30) & (rsiDf.num == 0)].values # rsi 20 이하인 종가

    print("lastRSI = " , lastRSI)
    print("lastClose = " , lastClose)

    # 매수 로직
    if len(lastRSI) == 0 :
        print('패스')
    else :
        print('매수!!!')
        myKRW = upbit.get_balance("KRW") # 자산조회
        cnt = 2
        if float(lastClose)*cnt > 5000 :
            print(upbit.buy_limit_order(coin , float(lastClose), cnt ))
            print("buy!! ")
            print("원화 : ", upbit.get_balance("KRW"))
        else :
            print("5000원 미만!! ")
    '''