#coding: utf-8

import random
import bigNumDLL
import sys
import euclidExtBin
import simpleGen

int0 = bigNumDLL.bigNum("0")
int1 = bigNumDLL.bigNum("1")
int2 = bigNumDLL.bigNum("2")
int256 = bigNumDLL.bigNum("256")

def checkParam(paramsNum, arguments): #проверка того, что параметры командной строки
    if (paramsNum != 1):                #введены верно
        print "There is wrong number of parameters. Main string was entered incorrectly."
        return False

    return True

def PrintStart():
    print "This programme encrypts or decrypts the source file according\
        to El-Gamal cryptographic scheme "
    print "Main string should be in a such way: "
    print "[python file name]"

def powmod(basis, degree, modul): #быстрое возведение в степень по модулю
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

def keyGen(bitsLen):
    p = simpleGen.simpleBigNumGenerate(bitsLen)
    q = simpleGen.simpleBigNumGenerate(bitsLen)
    modul = p * q
    secret = bigNumDLL.bigNum()

    sFlag = True
    while sFlag:
        secret.getRandBigNum(bitsLen)
        if(secret < modul):
            sFlag = False

    secret.Write("secret.txt")

    openKey = (secret ^ int2) % modul
    return modul, openKey

def proove(modul, openKey, pretender, bitsLen):
    random.seed()
    checker = bigNumDLL.bigNum()

    for i in range(40):
        rFlag = True
        while rFlag:
            checker.getRandBigNum(bitsLen)
            if checker < modul:
                rFlag = False

        mail = (checker ^ int2) % modul
        randBitNow = random.randint(0, 1)
        randBit = bigNumDLL.bigNum(str(randBitNow))
        if randBit == int1:
            print "I'm 1"
        elif randBit == int0:
            print "I'm 0"

        reply = (checker * (pretender ^ randBit)) % modul

        if reply == int0:
            return False

        leftPart = (reply ^ int2) % modul
        rightPart = (mail * (openKey ^ randBit)) % modul
        if randBit == int1:
            leftPart.Write("lp.txt")
            rightPart.Write("rp.txt")
        if leftPart != rightPart:
            print "Doshel!"
            return False

    return True

def main():
    int1 = bigNumDLL.bigNum("1")

    paramsNum = len(sys.argv)
    if not checkParam(paramsNum, sys.argv):
        sys.exit(-1)

    PrintStart()
    bitsLen = 128

    print "Open key is generated..."

    modul, openKey = keyGen(bitsLen)

    print "Open key is successfully calculated!"

    print "Please, enter the secret key: "
    pret = raw_input()
    pretender = bigNumDLL.bigNum(pret)
    
    isRealOwner = proove(modul, openKey, pretender, bitsLen)

    if isRealOwner:
        print "Owner confirmed, he knows the secret!"
    else:
        print "Owner couldn't confirm, he knows the secret!"

    print "Cryptographic Fiat-Shamir's protocol  has been performed successfully!"
        
if __name__ == "__main__":
    main()
