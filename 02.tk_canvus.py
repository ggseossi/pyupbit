from tkinter import *
from tkinter import messagebox

import re
from urllib import request

# hynix 000660 naver 035420 LG디스플레이 034220 
# 삼성전자 005930 삼성전자(우) 005935 바디텍매드 206640 크래프톤 259960
company_codes = ["000660" , "035420", "034220"]

stkcode = "005935"
samsung_buyamt = 10101000
bodymad_buyamt = 744435 # 호털s 주식
samsungwo_buyamt = 7774700 # 용덕s 주식


#bs_obj 를 받아서 candle_chart 리턴하도록
def get_candle_chart_data(company_code):
    url = "https://finance.naver.com/item/main.nhn?code="+company_code  # url 입력
    html = request.urlopen(url).read().decode("cp949")

    # dl class 뽑기
    pattern1 = r"(\<dl class=\"blind\"\>)([\s\S]+?)(\</dl\>)"
    result = re.findall(pattern1, html)  # <dl class="blind"> </dl> 읽어오기 list type
    result = result[0][1].strip()  # html 헤더정보는 제외하고 중간의 원하는 정보만 뽑아와서 str으로 변환한다.

    # dd 정보들 뽑기
    pattern2 = r"(\<dd\>)([\s\S]+?)(\</dd\>)"
    detail_results = re.findall(pattern2, result)  # 변환된 list 중 필요한 정보는 전부 <dd> </dd>로 쌓여 있으니, 이 정보만 list로 뽑아온다

    # 다듬기 및 출력
    for detail_result in detail_results[1:]:  # 각각의 tuple을  뽑아내서 string으로 출력하기
        # tuple 들 중 0번 index는 버린다 (장마감 시간)
        ret = detail_result[1].split(" ")
        # if ( ret.find("현재가") > 0) :
        #     return ret
        if ("현재가" in ret) : return ret
        # print(detail_result[1].split(" "))  # [0]과 [2]는 각각 <dd>와 </dd> 이기 때문에 버리고 [1]의 실제 데이터만 사용한다
        # return detail_result[1].split(" ")
        # [1]의 데이터도 띄어쓰기를 구분하여 보면 더 분석이 용이하니 split 한다


def clickButton() :
    # messagebox.showinfo('현재시세', get_candle_chart_data("005930"))
    today = get_candle_chart_data(stkcode)
    label1 = Label(window, text=today, anchor="w", font=('굴림', 12))
    # canvas.create_text([400, 200], text=today, font=('굴림', 12))
    label1.pack()
    
    # 그래프 표시
    if ("하락" in today):
        canvas.create_line(0, 0, 250, 170, fill="blue", width=3)
    else:
        canvas.create_line(0, 170, 250, 20, fill="red", width=3)

    samsung_sum = 176 * float(today[1].replace(',',''))
    def1 = samsung_buyamt - samsung_sum

    body_sum = 45 * float(today[1].replace(',',''))
    def2 = bodymad_buyamt - body_sum

    samsungwu_sum = 142 * float(today[1].replace(',',''))
    def3 = samsungwo_buyamt - samsungwu_sum


    if stkcode == "005930" :
        if samsung_buyamt < samsung_sum :
            def1 = def1 * -1
            label2 = Label(window, text="매입단가 : 57,392 (176주) / + "+str(def1), foreground='red', anchor="w", font=('bold', 12))
        else:
            label2 = Label(window, text="매입단가 : 57,392 (176주) / - "+str(def1), foreground='blue',anchor="w", font=('bold', 12))
    elif stkcode == "206640" : # 호털's 주식
        if bodymad_buyamt < body_sum :
            def2 = def2*-1
            label2 = Label(window, text="매입단가 : 16,543 (45주) / + "+str(def2), foreground='red', anchor="w", font=('bold', 12))
        else:
            label2 = Label(window, text="매입단가 : 16,543 (45주) / - "+str(def2), foreground='blue',anchor="w", font=('bold', 12))
    elif stkcode == "005935" : # 용덕's 주식
        if samsungwo_buyamt < samsungwu_sum :
            def3 = def3*-1
            label2 = Label(window, text="매입단가 : 54,751 (142주) / + "+str(def3), foreground='red', anchor="w", font=('bold', 12))
        else:
            label2 = Label(window, text="매입단가 : 54,751 (142주) / - "+str(def3), foreground='blue',anchor="w", font=('bold', 12))

    label2.pack()
    window.mainloop()

window = Tk()

canvas = Canvas(window, height=300, width=500) # 캔버스를 윈도 창에 부착
window.title("실시간시세")
canvas.pack()

# Button의 스타일과 버튼 클릭 시 실행되는 함수(clickButton)를 지정하였다.
button1 = Button(window, text="수익률측정", fg="red", bg="yellow", command=clickButton)
button1.pack(expand=1)

window.mainloop()






# print(get_candle_chart_data("000660"))
# print(get_candle_chart_data("035420"))