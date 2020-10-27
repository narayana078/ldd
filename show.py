#Descripition : list 2.4 Ghz and 5 Ghz channels and frequiencies
#Name : Lakshmi Narayana
import subprocess
import platform

def scan(interface):
    cmd = ["iwlist", interface, "channel"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ch= proc.stdout.read().decode('ascii',errors="backslashreplace")
    ch=ch.replace("\r","")
    ls= ch.split("\n")
    ls=ls[1:]
    return ls
#2.4ghz
def twon():
    ch=scan("wlp3s0")
    lis=[]
    i=0
    for item in ch:
        ch1=()
        if item.find('2.4')>0:
            item=str(item)
            channel=item[10:-12]
            ch1=ch1+(channel,)
            freq=item[23:]
            ch1=ch1+(freq,)
            lis.append(ch1)
            del ch1
        if item.find("Current Frequency:2.4")>0:
            lis=lis[:-1]
    return lis
#5ghz
def fiven():
    ch=scan("wlp3s0")
    lis=[]
    i=0
    for item in ch:
        ch1=()
        if item.find('5.')>0:
            item=str(item)
            channel=item[10:-10]
            ch1=ch1+(channel,)
            freq=item[23:]
            ch1=ch1+(freq,)
            lis.append(ch1)
            del ch1
        if item.find("Current Frequency:5.")>0:
            lis=lis[:-1]
    return lis

#2.4 frequency
def twoc():
    ch=scan("wlp3s0")
    ch1=()
    lis=[]
    i=0
    for item in ch:
            if item.find("Current Frequency:2.4")>0:
                item=str(item)
                item=item[28:]
                ch1=ch1+(item,)
                ch1=ch1+(platform.node(),)
                lis.append(ch1)
    return lis
#5 frequency
def fivec():
    ch=scan("wlp3s0")
    ch1=()
    lis=[]
    i=0
    for item in ch:
            if item.find("Current Frequency:5.")>0:
                item=str(item)
                item=item[28:]
                ch1=ch1+(item,)
                ch1=ch1+(platform.node(),)
                lis.append(ch1)
    return lis

if __name__=="__main__":
    num=twon()
    print("\n2.4 Ghz channels\n")
    print(num)
    print("\n5 Ghz channels\n")
    num=fiven()
    print(num)
    print("\n")
    ls=twoc()
    print(ls)
    print("\n")
    ls=fivec()
    print(ls)

