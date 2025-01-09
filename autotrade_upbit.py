import pyupbit
import talib
import os
import time
import numpy
from dotenv import load_dotenv
import pyupbit.websocket_api as wsck
load_dotenv()

access = os.getenv("UPBIT_ACCESS_KEY")
secret = os.getenv("UPBIT_SECRET_KEY")

################### 변수 설정 ####################
BTC = "KRW-BTC"
ETH = "KRW-ETH"
XRP = "KRW-XRP"
STX = "KRW-STX"

setCoin     = XRP      # 코인설정
setCoinCd   = "XRP"    # 코인설정
setRSI      = 40       # 매수 RSI 값 설정
setSellRate = 2.0      # 매도 퍼센트 
setBuyAmt   = 100000.0 # 분할매수 가격설정 

min = "minute5"        # 분봉설정
prevRSI = 0.0          # 매수했던 RSI 지표
buyCnt  = 0            # 매수횟수
coinCnt = 0.0          # 코인 수량
coinAvg = 0.0          # 코인 평단가

# 업비트 로그인 #
# access = os.getenv("UPBIT_ACCESS_KEY")
# secret = os.getenv("UPBIT_SECRET_KEY")
# upbit = pyupbit.Upbit(access,secret)

################### RSI지표 함수 ####################
def RSI(coin, min ,period=14) : 
    rdf = pyupbit.get_ohlcv(coin, min, 70)
    rdf['rsi'] = talib.RSI(rdf.close)
    numlist = []

    for i in range(len(rdf)):
        numlist.append(i)
    numlist.reverse()
    rdf['num'] = numlist

    return rdf

####################### MAIN ########################
if __name__ == "__main__" :
    while True:
        # time.sleep(10)
        try :
            # 통신연결
            wm = wsck.WebSocketManager("ticker", [setCoin , ]) # 통신연결
            for i in range(100):
                data = wm.get()
                print(i, data['trade_price']) # 실시간 시세
                # 로직 
                # 1번째 RSI 지표 조회
                df = RSI(setCoin, min)
                print(df)

                # setRSI 값 설정 30 이하일때 매수하도록 설정
                rsiNum = df['rsi'].loc[(df.rsi<=setRSI) & (df.num == 0)].values
                print("rsiNum = " , rsiNum)

                # # 업비트 로그인 #
                upbit = pyupbit.Upbit(access,secret)
                myBalnce = upbit.get_balances() # 잔고조회
                print("잔고 : " , myBalnce)
                if myBalnce != None:
                    for i in range(len(myBalnce)):
                        if str(myBalnce[i]['currency']) == "KRW" :
                            print("KRW : " , myBalnce[i]['balance'])

                        if str(myBalnce[i]['currency']) == setCoinCd :
                            print("보유코인 : "         , myBalnce[i]['currency'])
                            print("보유코인 수량 : "     , myBalnce[i]['balance'])
                            print("보유코인 평균단가 : " , myBalnce[i]['avg_buy_price'])                                       
                            coinCnt = float(myBalnce[i]['balance'])
                            coinAvg = float(myBalnce[i]['avg_buy_price'])
                            print(float(data['trade_price']))
                            print(float(coinAvg))

                ########## 매도 로직 ########## 
                tempPlusRate = 0.0
                if coinCnt > 0.0 : #매수한 코인 있을때
                ##### 2% 수익시 ##### 
                    tempPlusRate = round(((float(data['trade_price']) - float(coinAvg)) 
                                           / float(coinAvg)) * 100 , 2) #현 수익률계산
                    print("tempPlusRate : " , tempPlusRate) 
                    if tempPlusRate >= setSellRate:
                        if float(data['trade_price']) * coinCnt > 5000.0 :
                            sellResult = upbit.sell_limit_order(setCoin , float(data['trade_price']), coinCnt )
                            print(sellResult)
                            print(" ############ 2% 수익!!!!!! 매도 완료 ")
                        else :
                            print("5000원 미만!! 매도불가! ")
                ##### 급락올떄 풀매도 #####
                else :
                    print("매수코인 없음 ") 

                ########## 최초 매수 ########## 
                if buyCnt == 0: 
                    if len(rsiNum) > 0 :
                        print("최초 매수하기")
                        print("RSI 지표 : " , rsiNum[0])
                        
                        # 수량 구하기 (분할매수시 10만원 단위)
                        if data['trade_price'] != None:
                            ea = float(float(setBuyAmt / float(data['trade_price'])))
                            ea = round(ea,8)
                            print("수량 ::>> ", ea)
                            if float(data['trade_price'])*ea > 5000.0 :
                                buyResult = upbit.buy_limit_order(setCoin , float(data['trade_price']), ea )
                                print(buyResult)
                                buyCnt = buyCnt + 1 # 매수횟수증가
                                prevRSI = float(rsiNum[0]) # 현재 RSI 지표
                            else :
                                print("5000원 미만!!  매수불가! ")
                ########## 추가 매수 ##########                          
                else : # 최초 매수 아닌 추가매수 
                    if prevRSI - 5 > float(rsiNum[0]) : #기존 매수 RSI지수보다 5작을때
                        print("추가 매수!! ")
                        ea = float(float(setBuyAmt / float(data['trade_price'])))
                        ea = round(ea,8)
                        print("수량 : ", ea)
                        if float(data['trade_price'])*ea > 5000.0 :
                            buyResult = upbit.buy_limit_order(setCoin , float(data['trade_price']), ea )
                            print(buyResult)
                            buyCnt = buyCnt + 1
                            prevRSI = float(rsiNum[0]) # 현재 RSI 지표
                        else :
                            print("5000원 미만!! 매수불가! ")

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