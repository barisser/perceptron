import random
import math
import hashlib
import datetime
import time
import numpy as np
import btcanalysis as btc

layers=[4, 10, 3]

layern=len(layers)

randn=0

def rand():
    a=time.time()
    global randn

    b=hashlib.sha256(str(a)+str(randn)).hexdigest()

    c=int(b, 16)
    randn=randn+math.pow(c, 0.5)
    d=float(c%1000000)
    return d/1000000

def rand_array(n):
    r=[]
    for i in range(n):
        r.append(rand())
    return r

def logistics(sumin):
    r=1/(1+math.pow(math.e, -1*sumin))
    return r

def score(outputset, onedaychangedata):
    m=1
    a=0
    while a<len(outputset)-1:

        if outputset[a]==0: #SELL
            m=m/(1+onedaychangedata[a+1])
        elif outputset[a]==2: #BUY on margin
            m=m*(1+onedaychangedata[a+1])

        a=a+1
    return m




class unit:


    def __init__(self):     
        self.neurons=[]
        self.axons=[]
        for x in layers:
            r=[]
            for i in range(0, x):
                r.append(0)
            self.neurons.append(r)
        for i in range(0, layern-1):
            #self.axons.append(rand_array(layers[i]*layers[i+1]))
            g=[0]*layers[i]*layers[i+1]
            self.axons.append(g)


    def reset(self):
        self.neurons=[]
        for x in layers:
            r=[]
            for i in range(0, x):
                r.append(0)
            self.neurons.append(r)


    def run(self, inputs):
        global outs
        self.reset()

        b=0
        while b<len(self.neurons[0]):
            self.neurons[0][b]=inputs[b]
            b=b+1

        a=0
        while a<layern-1:
            outs=[]

            for x in self.neurons[a]:
                t=logistics(x)
                outs.append(t)

            nn=0
            while nn<len(self.neurons[a]):
                #for each neuron in layer
                #scan all subsequent axons
                aa=0
                while aa<len(self.neurons[a+1]): #length of next layer
                    axonid=nn*len(self.neurons[a+1])+aa
                    axonweight=self.axons[a][axonid]
                    self.neurons[a+1][aa]=axonweight*outs[nn]

                    aa=aa+1


                nn=nn+1
            a=a+1

        f=self.neurons[layern-1]
        g=0
        best=-1
        bestn=-1
        while g<len(f):
            if f[g]>best:
                best=f[g]
                bestn=g
            g=g+1
        return bestn


    def cycle(self, inputset):
        #RUNS MANY TIMES
        #inputset should be 2D array
        g=0
        outputs=[]
        while g<len(inputset):
            outputs.append(self.run(inputset[g]))
            g=g+1

        return outputs




class system:

    def __init__(self, unit_n):
        self.units=[unit() for i in range(unit_n)]
        self.bestscore=0
        self.bestaxons=[]


    def compete(self, inputs):
        r=[]
        scores=[]
        probability=[]

        for x in self.units:
            outs=x.cycle(inputs)
            s=score(outs, btc.onedaychange)
            if s>self.bestscore:
                self.bestscore=s
                self.bestaxons=x.axons
                print s

            probability.append(math.pow(s, 2))

        a=sum(probability)
        if a==0:
            a=1
        p=[]
        n=0
        for x in probability:
            p.append([float(x)/float(a), n])
            n=n+1

        p.sort()


        return p

    def choosesurvivors(self, probability):
        n=len(self.units)
        survivors=[]

        while len(survivors)<n:
            a=rand()
            b=0
            f=-1
            while b<len(probability):
                if a<=probability[b][0]:
                    f=probability[b][1]
                    b=len(probability)
                elif a>probability[b][0]:
                    a=a-probability[b][0]
                b=b+1
            if not f==-1:
                survivors.append(f)
        return survivors

    def recombine(self, a, b):
        r=[]
        c=0
        while c<len(self.units[a].axons):
            g=[]
            d=0
            while d<len(self.units[a].axons[c]):
                g.append(self.units[a].axons[c][d]/2+self.units[b].axons[c][d]/2)
                d=d+1
            r.append(g)

            c=c+1
        return r

    def permutate(self, factor):
        a=0
        while a<len(self.units):
            b=0
            while b<len(self.units[a].axons):
                c=0
                while c<len(self.units[a].axons[b]):

                    y=rand()*factor-0.5*factor
                    self.units[a].axons[b][c]=self.units[a].axons[b][c]+y
                    c=c+1
                b=b+1



            a=a+1

    def breednew(self, survivors):
        #FULL recombination
        a=0
        while a<len(survivors):

            r=random.randint(0, len(survivors)-1)
            g=self.recombine(a, r)
            self.units[a].axons=g

            a=a+1

    def evolveonce(self, inputs):
        p=self.compete(inputs)
        survivors=self.choosesurvivors(p)
        self.permutate(0.1)
        self.breednew(survivors)

    def evolve(self, inputs, generation_n):
        a=0
        while a<generation_n:
            self.evolveonce(inputs)
            a=a+1
            print "generation "+str(a)



a=system(20)

inputset=[]

def init():
    global inputset
    btc.init()
    a=0
    while a<len(btc.price):
        r=[]
        r.append(btc.price[a])
        r.append(btc.volume[a])
        r.append(btc.onedaychange[a])
        r.append(btc.Xdifference[a])
        r.append(btc.Ydifference[a])
        inputset.append(r)

        a=a+1




init()
