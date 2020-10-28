#Descripition : list 2.4 Ghz and 5 Ghz channels and frequiencies and current signal strength
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
def scan_ch(interface):
    cmd = ["iwlist", interface, "scan"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ch= proc.stdout.read().decode('ascii',errors="backslashreplace")
    ch=ch.replace("\r","")
    ls= ch.split("\n")
    ls=ls[1:]
    return ls
#2.4ghz
def twonum():
    ch=scan("wlp3s0")
    sig=scan_ch("wlp3s0")
    lis=[]
    i=0
    chan=""
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
            item=str(item)
            chan=item[28:-13]
    for it in sig:
        if it.find("level")>0:
            cha=str(it)
            signal=cha[48:-1]
    i=0
    for item in lis:
        tup=item
        if(tup[1]==chan):
            tup=tup+(signal,)
            lis.remove(item)
            lis.insert(i,tup)
        i=i+1
    return lis
#5ghz
def fivenum():
    ch=scan("wlp3s0")
    sig=scan_ch("wlp3s0")
    lis=[]
    i=0
    chan=""
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
            item=str(item)
            chan=item[28:-13]
    for it in sig:
        if it.find("level")>0:
            cha=str(it)
            signal=cha[48:-1]
    i=0
    for item in lis:
        tup=item
        if(tup[1]==chan):
            tup=tup+(signal,)
            lis.remove(item)
            lis.insert(i,tup)
        i=i+1
    return lis


if  __name__=="__main__":
    num=twonum()
    print("\n2.4 Ghz channels\n")
    print(num)
    print("\n5 Ghz channels\n")
    num=fivenum()
    print(num)


