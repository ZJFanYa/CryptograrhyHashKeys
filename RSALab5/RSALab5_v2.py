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
        to RSA cryptographic algorithm "
    print "Main string should be in a such way: "
    print "[python file name] [source file name] [result file name]"
    print "	python file name - name of file with a program"
    print "	source file name - file with the plain text"
    print "     result file name - file with a result of encryption or decryption"

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

def shiftRight(arr, size): #добавить новую ячейку массива
    if not size:            #и сдвинуть все ячейки массива вправо на
        arr.append(int0)       #один шаг
        size = 1
        return arr, size

    arr.append(int0)
    size += 1
    for i in range(size - 1):
        arr[size - 1 - i] = arr[size - 2 - i]

    arr[0] = int0

    return arr, size

def getArr(message, modulo):    #получение из текстовой строки массива
    symArr = []                 #больших чисел
    symArrSize = 0

    elCount = 0
    count = 0
    while len(message) > elCount:
        degree = int1
        symArr, symArrSize = shiftRight(symArr, symArrSize)
        while ((symArr[0] < modulo) and (len(message) > elCount)):
            elemNow = ord(message[len(message) - 1 - elCount])
            elemBigNum = bigNumDLL.bigNum(str(elemNow))
            symArr[0] += (elemBigNum * degree)
            degree *= int256
            elCount += 1
        if symArr[0] >= modulo:
            degree /= int256
            symArr[0] -= (elemBigNum * degree)
            elCount -= 1
        while ord(message[len(message) - elCount]) == 0:
            elCount -= 1
        count += 1

    return symArr, count

def getArrDec(message, modulo, lenArr):    #получение из текстовой строки массива
    symArr = []                 #больших чисел
    symArrSize = 0

    elCount = 0
    for i in range(len(lenArr)):
        tmpCount = 0
        degree = int1
        symArr, symArrSize = shiftRight(symArr, symArrSize)
        while (tmpCount < lenArr[i]):
            elemNow = ord(message[len(message) - 1 - elCount])
            elemBigNum = bigNumDLL.bigNum(str(elemNow))
            symArr[0] += (elemBigNum * degree)
            degree *= int256
            elCount += 1
            tmpCount += 1

    return symArr, len(lenArr)

def getText(arr, size): #получить текстовое сообщение из массива
    mesLen = 0          #больших чисел
    message = ""
    lenArr = []
    for i in range(size):
        tempMes = ""
        while arr[size - 1 - i] != int0:
            elemNow = arr[size - 1 - i] % int256
            value = elemNow.getInt()
            tempMes = chr(value) + tempMes
            arr[size - 1 - i] /= int256
        message = tempMes + message
        lenArr.append(len(tempMes))

    return message, lenArr

def encrypt(message, openKey, modulo): #функция шифрования алгоритмом RSA
    sourceArr, size = getArr(message, modulo)
    cipherArr = []
    for i in range(size):
        cipherArr.append([])

    for i in range(size):
        cipherArr[i] = powmod(sourceArr[i], openKey, modulo)

    encrText, lenArr = getText(cipherArr, size)
    return encrText, lenArr

def decrypt(message, closeKey, modulo, lenArr): #функция дешифрования алгоритмом RSA
    cipherArr, size = getArrDec(message, modulo, lenArr)
    sourceArr = []
    for i in range(size):
        sourceArr.append([])

    for i in range(size):
        sourceArr[i] = powmod(cipherArr[i], closeKey, modulo)

    plaintext, oneArr = getText(sourceArr, size)
    return plaintext
	
def rsa(plaintext):
    print "Big simple numbers are generated..."
	
    firstFact = simpleGen.simpleBigNumGenerate()
    secFact = simpleGen.simpleBigNumGenerate()

    print "Simple number are generated successfully!"
	
    modulo = firstFact * secFact
    fi = (lambda x, y: (x - int1)*(y - int1))(firstFact, secFact)

    openKey, closeKey = euclidExtBin.euclideExtend(fi)

    print "Open and close keys are successfully calculated!"    

    print "Source message is encrypted..."

    cipher, lenArr = encrypt(plaintext, openKey, modulo)

    print "Source message is encrypted successfully"

    print "Ciphered message is decrypted..."

    source = decrypt(cipher, closeKey, modulo, lenArr)

    print "Ciphered message is decrypted successfully"
	
    return source

def main():
    int1 = bigNumDLL.bigNum("1")

    paramsNum = len(sys.argv)
    if not checkParam(paramsNum, sys.argv):
        sys.exit(-1)

    sourceFileName = sys.argv[1]
    destinFileName = sys.argv[2]
    resFileName = sys.argv[3]

    PrintStart()
	
    with open(sourceFileName, 'rb') as sourceFile:
        plainText = sourceFile.read()
	
    source = rsa(plainText)

    with open(resFileName, 'wb') as resFile:
        resFile.write(source)

    print "Cryptographic algorithm RSA has been performed successfully!"
        
if __name__ == "__main__":
    main()
