#-*- coding:utf-8 -*-
import random
import numpy as np
# 生成32位元组，，，，先默认输入的是32位二进制
inputarray=[]
inputarray2=[]
output=[]
for i in xrange(32):
    inputarray.append(random.randint(0,1))
    inputarray2.append(random.randint(0,1))
# inputarray=[1, 0, 0, 1,0, 1, 0, 1,0, 1, 1, 0,1, 0, 0, 0,0, 0, 1, 1, 0, 1, 1, 1,  1, 1, 1, 1,  0, 1, 0, 1]
# inputarray2=[0, 1, 1, 0,1, 1, 0, 1,1, 1, 1, 0,1, 0, 0, 1, 1, 0, 0, 1,  0, 1, 0, 1,1, 0, 0, 0,0, 0, 0, 0]

#########################
# 10进制与2进制列表转化  #
#########################
def bittonum(inputarray):
    l=len(inputarray)
    k=len(inputarray)/4
    num=[]
    sum=0
    for i in range(l-1,0,-4):
        num.append(inputarray[i]*1+inputarray[i-1]*2+inputarray[i-2]*4+inputarray[i-3]*8)
        i=i-4
    for i in range(k):
        sum+=(num[i]*(16**i))
    return sum

def numtobit_1(num):
    la=[]
    if num<0:
        return '-'+numtobit(abs(num))
    while True:
        num,remainder=divmod(num,2)
        la.append(str(remainder))
        if num==0:
            return ''.join(la[::-1])

def numtobit(num):
    k=numtobit_1(num)
    k = map(int, k)
    if len(k)<32:
        k.reverse()
        for i in range(32-len(k)):
            k.append(0)
        k.reverse()
    return k




#######################
#      轮函数操作      #
########################
# length=(len(inputarray)/2)
# L_array=inputarray[0:length-1]
# R_array=inputarray[length:2*length-1]
#左移一位函数,,,传入左移的数组需要a=L_array[0:length-1]给a，否则原array会发生移位。
def L_go(L_array):#左移
    a=L_array
    b=a.pop(0)
    a.append(b)
    return a
##a=L_array[0:length-1]
#simon 轮函数
def simon(inputarray):#simon轮函数
    length=(len(inputarray)/2)
    L_array=inputarray[0:length]
    R_array=inputarray[length:length*2]
    #左移操作
    L_1 = L_array[0:length]
    L_1=L_go(L_1)
    L_3=L_array[0:length]
    for i in xrange(3):
        L_3=L_go(L_3)
    L_7=L_3
    for i in xrange(4):
        L_7=L_go(L_7)
    array_1=np.array(L_1)
    array_3 = np.array(L_3)
    array_7=np.array(L_7)
    out=((array_1&array_7)^R_array)^array_3
    newL_array=out.tolist()
    L=newL_array[0:length]
    newR_array=L_array
    L.extend(newR_array)
    return L

######################
#      n轮加密       #
######################
def simon_n(n,inputarray):
    for i in range(0,n):
        inputarray=simon(inputarray)
    return inputarray
print simon_n(1,inputarray)




#加密测试
# for i in xrange(10):
#     inputarray=simon(inputarray)
# print inputarray


##################
#  求轮函数次数   #
##################
#一阶差分
def chafen(i,inputarray,n):
    y=len(inputarray)
    x=inputarray[0:y]
    x = bittonum(inputarray)
    miwen=x^i
    miwen=numtobit(miwen)
    newx=simon_n(n,miwen)#############

    return newx   #??????????差分加密出来是个 列表 数组   怎么求和  怎么比较
#迭代序列，非线性差分基底
def jiahexulie(d):
    x=[]
    i=2**(d-1)
    while i<2**d:
    x.append(i)
        i+=1
    return x
#高阶差分（n）
def gaojie(inputarray,jiahe,n):
    temp=[]
    for i in jiahe:
        temp.append(bittonum(chafen(i,inputarray,n)))
    return temp
###########################
#    次数验证函数         #
###########################
def yanzheng(d,n,max):#d次数，test测试字符串，基于
    counter=0
    tmp=[]
    xulie=[]
    for i in range(1,d):
        xulie.extend(jiahexulie(i))
    while(counter<max):
        test=[]
        for i in range(n):#####32bit
            test.append(random.randint(0, 1))
        tmp=gaojie(test, xulie, n)
        if counter==0:
            sum=tmp
            counter=counter+1
        else:
            if tmp!=sum:
                return 0
            counter=counter+1
    return 1
#########################
# 计算n轮加密的布尔次数  #
#########################

def cishu(inputarray,inputarray2,n):
    Y_1=[]
    Y_2=[]
    xulie=[0]
    for i in range(1,33):
        d=i
        print d
        xulie=jiahexulie(d)
        Y_1.extend(gaojie(inputarray,xulie,n))
        Y_2.extend(gaojie(inputarray2,xulie,n))
        Y_1_set=set(Y_1)
        Y_2_set=set(Y_2)
        if (list(Y_1_set-Y_2_set)):
            continue
        else:
            # if yanzheng(d,n,n)==1:
            #     return d
            # else:
            #     continue
            return d
    return d

#main
#
# for i in range(11,13):
#      print ("正在计算第%d轮次数" %(i))
#      output.append(cishu(inputarray,inputarray2,i))
# print output

print cishu(inputarray,inputarray2,16)
