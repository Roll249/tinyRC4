#!/usr/bin/env python3
w,e,r=range,len,str.encode
class R:
    def __init__(self,k):
        l,t = r(k),0
        b = [i for i in w(0,256)]
        for i in w(0,e(b)):
            t=t+b[i]+l[i%e(l)]
            t %= 256
            b[t],b[i]=b[i],b[t]
        self.b=b

    def gk(self,x):
        s,p,q,b=[],0,0,self.b
        while not e(s)>=e(x):
            p=(p+1)%256
            q=(q+b[p])%256
            b[p],b[q]=b[q],b[p]
            j=(b[p]+b[q])%256
            s.append(b[j])
        self.s=s

    def c(self,x):
        y,o=r(x),[]
        for i in w(0,e(y)):
            o.append(self.s[i]^y[i])
        return ''.join([chr(z) for z in o])

