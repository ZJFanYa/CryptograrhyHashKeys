# -*- coding:cp1251 -*-

import sys
import math

def checkParam(paramsNum, arguments): #проверка того, что параметры командной строки
    if (paramsNum != 3):                #введены верно
        print "There is wrong number of parameters. Main string was entered incorrectly."
        return False
    
    return True
	
def PrintStart():
    print "This programme encodes the source file according\
        to MD5 hash algorithm "
    print "Main string should be in a such way: "
    print "[python file name] [source file name] [result file name]"
    print "	python file name - name of file with a program"
    print "	source file name - file with the plain text"
    print "     result file name - file with a hash sum of source file"

def intTo8Hex(value):       #функция представления длины потока в 64-х битах 
    value = value * 8       #получаем длину потока в битах
    resArr = []
    for i in range(8):
        resArr.append([])   #готовим массив для длины потока
    for j in range(2):  
        for i in range(4):
            resArr[i + 4 * j] = value % 0x100   #сначала идет младшее слово
            value = value / 0x100

    return resArr       #массив с представленной в нем длиной текста в битах

def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (~z | x)

def T(value):
    return int(4294967296 * abs(math.sin(value)))

def cicleShift(value, shift):
    mainPart = (value << shift) % 0x100000000   #сдвинули влево слово на 32 - shift позиций
    secPart = value >> (32 - shift)             #сдвинутые первые shift бит засунули в конец
    return mainPart + secPart

def firRoundMagicFun(A, B, C, D, k, shift, i):
    result =  (B + cicleShift((A + F(B, C, D) + k + T(i)) % 0x100000000, shift)) %\
             0x100000000
    return result

def secRoundMagicFun(A, B, C, D, k, shift, i):
    result =  (B + cicleShift((A + G(B, C, D) + k + T(i)) % 0x100000000, shift)) %\
             0x100000000
    return result

def thirRoundMagicFun(A, B, C, D, k, shift, i):
    result =  (B + cicleShift((A + H(B, C, D) + k + T(i)) % 0x100000000, shift)) %\
             0x100000000
    return result

def fourRoundMagicFun(A, B, C, D, k, shift, i):
    result =  (B + cicleShift((A + I(B, C, D) + k + T(i)) % 0x100000000, shift)) %\
             0x100000000
    return result

def md5Hashing(plainText):
    plainTextLen = len(plainText)
    plainText = plainText + chr(0x80)  #добавляем байт 0х80 в конец файла

    while (len(plainText) % 0x40) != 0x38:
        plainText = plainText + chr(0x00) #добавляем байты 0x00, пока длина потока не станет 
                                            #сравнима с 448 по модулю 512
    lenArr = intTo8Hex(plainTextLen)        #найти 64-х битное рпедставление длины файла

    for i in range(8):
        plainText = plainText + chr(lenArr[i]) #добавляем представление длины в конец потока

    plainTextLen = len(plainText)

    sourceArr = []
    for i in range(plainTextLen / 4):
        value = 0
        for j in range(4):
            value = value + (ord(plainText[i * 4 + j]) << (j * 8))  #обращаем порядок байт в каждом слове
        sourceArr.append(value)
        
    wordsArr = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
    
    codArr = []             #массив для хранения текущего потока из 16 слов
    for i in range(16):
        codArr.append([])

    copyArr = []            # массив с временной копией слов искомого хэша
    for i in range(4):
        copyArr.append([])
        
    for i in range(len(sourceArr) / 16):
        for j in range(16):
            codArr[j] = sourceArr[i * 16 + j]
            
        for j in range(4):
            copyArr[j] = wordsArr[j]
            
        for j in range(4):
            for k in range(4):
                wordsArr[(4 - k) % 4] = firRoundMagicFun(wordsArr[(4 - k) % 4], wordsArr[(5 - k) % 4],
                                           wordsArr[(6 - k) % 4], wordsArr[(7 - k) % 4],
                                           codArr[j * 4 + k], (k + 1) * 5 + 2, j * 4 + k + 1)

        for j in range(4):
            for k in range(4):
                wordsArr[(4 - k) % 4] = secRoundMagicFun(wordsArr[(4 - k) % 4], wordsArr[(5 - k) % 4],
                                           wordsArr[(6 - k) % 4], wordsArr[(7 - k) % 4],
                                           codArr[((4 * j) + (k * 5 + 1)) % 16],
                                               int(0.5 * k * k + 3.5 * k + 5), 16 + j * 4 + k + 1)

        for j in range(4):
            for k in range(4):
                wordsArr[(4 - k) % 4] = thirRoundMagicFun(wordsArr[(4 - k) % 4], wordsArr[(5 - k) % 4],
                                           wordsArr[(6 - k) % 4], wordsArr[(7 - k) % 4],
                                           codArr[((4 * (5 - j)) + (k * 3 + 1)) % 16],
                                               2 * ((k % 2) + int(k / 2)) + 5 * k + 4,
                                                32 + j * 4 + k + 1)

        for j in range(4):                
            for k in range(4):
                wordsArr[(4 - k) % 4] = fourRoundMagicFun(wordsArr[(4 - k) % 4], wordsArr[(5 - k) % 4],
                                           wordsArr[(6 - k) % 4], wordsArr[(7 - k) % 4],
                                           codArr[((4 * (4 - j)) + k * 7) % 16],
                                               int(0.5 * k * k + 3.5 * k + 6),
                                                48 + j * 4 + k + 1)

        for j in range(4):
            wordsArr[j] = (wordsArr[j] + copyArr[j]) % 0x100000000

    for i in range(4):
        firstByte = (wordsArr[i] & 0x000000ff) << 24  #обращаем порядок байт в словах выходного буфера
        secByte = (wordsArr[i] & 0x0000ff00) << 8
        thirByte = (wordsArr[i] & 0x00ff0000) >> 8
        fourByte = (wordsArr[i] & 0xff000000) >> 24
        wordsArr[i] = firstByte + secByte + thirByte + fourByte

    resStr = ""
    for i in range(4):
        stringToFile = hex(wordsArr[i])[2:-1]
        addString = '0' * (8 - len(stringToFile))
        resStr = resStr + addString + stringToFile
        
    return resStr

def main():
    paramsNum = len(sys.argv)
    if not checkParam(paramsNum, sys.argv):
        sys.exit(-1)
		
    sourceFileName = sys.argv[1]
    destinFileName = sys.argv[2]

    PrintStart()

    with open(sourceFileName, 'rb') as sourceFile:
        plainText = sourceFile.read()
		
    plainTextLen = len(plainText)

    if not plainText:
        print "The plain text file is empty. Error!"
        sys.exit(-1)

    md5Sum = md5Hashing(plaintext)

    with open(destinFileName, 'wb') as resFile:
        resFile.write(resStr)

    print "Hash algorithm md5 has been calculated successfully!"
        
if __name__ == "__main__":
    main()
