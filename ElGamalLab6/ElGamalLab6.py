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
    if (paramsNum != 4):                #введены верно
        print "There is wrong number of parameters. Main string was entered incorrectly."
        return False

    return True

def PrintStart():
    print "This programme encrypts or decrypts the source file according\
        to El-Gamal cryptographic scheme "
    print "Main string should be in a such way: "
    print "[python file name] [source file name] [midResult file name][result file name]"
    print "	python file name - name of file with a program"
    print "	source file name - file with the plain text"
    print "     midResult file name - file with a result of encryption"
    print "     result file name - file with a result of decryption"

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
    p.Write("p.txt")
    x = bigNumDLL.bigNum()
    g = bigNumDLL.bigNum()
    xFlag = True
    gFlag = True
    while gFlag:
        g.getRandBigNum(bitsLen)
        if(g < p):
            gFlag = False

    while xFlag:
        x.getRandBigNum(bitsLen)
        if(x < p):
            xFlag = False

    y = powmod(g, x, p)
    return y, g, p, x

def encrypt(message, g, y, p, bitsLen): #функция шифрования в схеме Эль-Гамаля
    if message >= p:
        print "Message is too large!"
    
    k, revK = euclidExtBin.euclideExtend(p - int1, bitsLen)

    a = powmod(g, k, p)
    b = powmod(y, k, p)
    b = b * message % p

    return a, b

def decrypt(b, a, x, p): #функция дешифрования в схеме
                                                #Эль-Гамаля
    a = powmod(a, x, p)
    gcd, C, revA = euclidExtBin.algorithm(a, p)
    if (gcd != int1):
        print "Error!"

    message = b * revA % p
    return message

def main():
    int1 = bigNumDLL.bigNum("1")

    paramsNum = len(sys.argv)
    if not checkParam(paramsNum, sys.argv):
        sys.exit(-1)

    sourceFileName = sys.argv[1]
    destinFileName = sys.argv[2]
    resFileName = sys.argv[3]

    PrintStart()
    bitsLen = 128

    print "Open and close keys are generated..."

    y, g, p, x = keyGen(bitsLen)

    print "Open and close keys are successfully calculated!"
    
    message = bigNumDLL.bigNum()
    message.Read(sourceFileName, 1000000000)

    print "Source message is encrypted..."

    a, b = encrypt(message, g, y, p, bitsLen)

    print "Source message is encrypted successfully"

    a.Write(destinFileName)
    b.Write("add.txt")

    print "Ciphered message is decrypted..."

    message = decrypt(b, a, x, p)

    print "Ciphered message is decrypted successfully"

    message.Write(resFileName)

    print "Cryptographic El-Gamal's algorithm  has been performed successfully!"
        
if __name__ == "__main__":
    main()
