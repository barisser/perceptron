import requests
import json
import math
import matplotlib.pyplot as plt

data=[]

price=[]  #weighted price per day, reverse order
volume=[]  #volume USD per day

onedaychange=[]

Xmovingaverage=[]
Xinterval=15

Ymovingaverage=[]
Yinterval=50

Xdifference=[] # PERCENTAGE DIFFERENCE between X moving average and todays price
Ydifference=[]



def get_data():
    f='http://www.quandl.com/api/v1/datasets/BITCOIN/BITSTAMPUSD'
    a=requests.get(f)
    if a.status_code==200:
        b=a.content
    global c
    c=json.loads(b)
    print c['column_names']
    #return c['data']
    global data
    datas=c['data']

    data=[]
    for x in datas:
        if x[7]>10000000:
            g=0
        else:
            data.append(x)



def prep():
    global volume, price, onedaychange,Xmovingaverage, Ymovingaverage
    global Xdifference, Ydifference

    for x in data:
        volume.append(x[6])
        price.append(x[7])


    price=price[::-1]
    volume=volume[::-1]

    a=0
    onedaychange.append(1)
    while a<len(price)-1:
        onedaychange.append(price[a+1]/price[a]-1)
        a=a+1

    for i in range(0,Xinterval):
        Xmovingaverage.append(0)
    for i in range(0,Yinterval):
        Ymovingaverage.append(0)

    a=0
    while a<len(price)-Xinterval:
        b=0
        r=0
        while b<Xinterval:
            r=r+float(price[a+b])/float(Xinterval)
            b=b+1
        Xmovingaverage.append(r)
        a=a+1

    a=0
    while a<len(price)-Yinterval:
        c=0
        r=0
        while c<Yinterval:
            r=r+float(price[a+c])/float(Yinterval)
            c=c+1
        Ymovingaverage.append(r)
        a=a+1

    for i in range(0,Xinterval):
        Xdifference.append(1)
    for i in range(0,Yinterval):
        Ydifference.append(1)

    g=Xinterval
    while g<len(Xmovingaverage):
        Xdifference.append(price[g]/Xmovingaverage[g]-1)

        g=g+1
    g=Yinterval
    while g<len(Ymovingaverage):
        Ydifference.append(price[g]/Ymovingaverage[g]-1)
        g=g+1


def average(x):
    b=0
    n=0
    for a in x:
        if a<999999999 and a>0:
            b=b+a
            n=n+1.0

    b=b/n
    return b


def standard_deviation(x):
    b=0
    g=average(x)
    for y in x:
        b=b+math.pow((y-g),2)

    b=b/len(x)
    b=math.pow(b,0.5)
    return b


def correlation(x,y):
    a=0
    b=0
    ax=average(x)
    ay=average(y)
    while a<len(x):
        c=x[a]-ax
        d=y[a]-ay
        g=c*d
        b=b+g
        a=a+1

    b=b/(standard_deviation(x)*standard_deviation(y))
    b=b/len(x)
    return b


def init():
    get_data()
    prep()


