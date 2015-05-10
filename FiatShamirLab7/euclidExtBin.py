#coding: utf-8

import random
import bigNumDLL
import sys

int0 = bigNumDLL.bigNum("0")
int1 = bigNumDLL.bigNum("1")
int2 = bigNumDLL.bigNum("2")
int256 = bigNumDLL.bigNum("256")

def algorithm(expoPret, fi):
    g = int1
    a = fi
    b = expoPret
    while(a % int2 == int0 and b % int2 == int0):
        a /= int2
        b /= int2
        g *= int2

    u = a
    v = b
    A = int1
    B = int0
    C = int0
    D = int1

    while u != int0:
        while u % int2 == int0:
            u /= int2
            if (A % int2 == int0 and B % int2 == int0):
                A /= int2
                B /= int2
            else:
                A = (A + b) / int2
                B = (B - a) / int2

        while v % int2 == int0:
            v /= int2
            if (C % int2 == int0 and D % int2 == int0):
                C /= int2
                D /= int2
            else:
                C = (C + b) / int2
                D = (D - a) / int2

        if u >= v:
            u -= v
            A -= C
            B -= D
        else:
            v -= u
            C -= A
            D -= B

    gcd = g * v
    return gcd, C, D % fi

def euclideExtend(fi, bitsLen):
    oFlag = True

    while oFlag:
        flag = False
        oFlag = False
        while not flag:
            bitsNum = random.randint(0, bitsLen)
            expoPret = bigNumDLL.bigNum()
            expoPret.getRandBigNum(bitsNum)
            if expoPret < fi:
                flag = True

        simpleEA = False
        while not simpleEA:
            gcd, C, D = algorithm(expoPret, fi)

            if ((gcd != int1) or (((expoPret * D) % fi) != int1)):
                expoPret += int1
                if expoPret >= fi:
                    oFlag = True
                    break
            else:
                simpleEA = True
                x = C
                y = D % fi

    return expoPret, y
