#coding: utf-8

import random
import bigNumDLL
import sys

int0 = bigNumDLL.bigNum("0")
int1 = bigNumDLL.bigNum("1")
int2 = bigNumDLL.bigNum("2")
int256 = bigNumDLL.bigNum("256")

def powmod(basis, degree, modul):
    result = int1

    while degree != int0:
        if degree % int2 == int0:
            basis *= basis
            basis %= modul
            degree /= int2
        else:
            degree -= int1
            result *= basis
            result %= modul

    return result

def checkLittleNums(simplePret):  #проверка делимости на простые числа
    flagsArr = []                   #от 0 до 256
    for i in range(256):
        flagsArr.append(False)

    for i in range(2):          #решетом Эратосфена протыкаем массив
        flagsArr[i] = True
    for i in range(2, 256):
        if not flagsArr[i]:
            j = i
            while (j + i) < 256:
                if not flagsArr[j + i]:
                    flagsArr[j + i] = True
                j = j + i

    for i in range(256):        #проверяем на делимость
        if not flagsArr[i]:
            divider = bigNumDLL.bigNum(str(i))
            if simplePret <= divider:
                break
            if (simplePret % divider) == int0:
                return False

    return True

def rabinMiller(simplePret, roundsNum):     #тест Рабина-Миллера на простоту
    algoNum = simplePret - int1             #числа
    deg = 0
    while (algoNum % int2) == int0:
        deg += 1
        algoNum /= int2

    for i in range(roundsNum):
        numForCheck = int0
        while((numForCheck > (simplePret - int2)) or (numForCheck < int2)):
            bitsNum = random.randint(2, roundsNum - 1)
            numForCheckArr = random.getrandbits(bitsNum)
            numForCheck = bigNumDLL.bigNum(str(numForCheckArr))

        flag = False

        checkVal = powmod(numForCheck, algoNum, simplePret)
        if not (checkVal == int1 or checkVal == (simplePret - int1)):
            for i in range(deg - 1):
                checkVal = (checkVal ^ int2) % simplePret
                if checkVal == int1:
                    return False
                elif checkVal == (simplePret - int1):
                    flag = True
                    break
            if not flag:
                return False

    return True

def checkSimple(simplePret, roundsNum):
    if checkLittleNums(simplePret) and rabinMiller(simplePret, roundsNum):
        return True
    return False

def simpleBigNumGenerate(bitsLen):
    simplePret = bigNumDLL.bigNum()
    simplePret.getRandBigNum(bitsLen)
    isSimple = False
    while not isSimple:
        isSimple = checkSimple(simplePret, bitsLen)
        if not isSimple:
            simplePret = simplePret + int1

    return simplePret
