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
        to ripemd-160 hash algorithm "
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

def magicFun(counter, x, y, z):
    if counter < 16:
        return x ^ y ^ z
    elif (counter >= 16 and counter < 32):
        return ((x & y) | (~x & z))
    elif (counter >= 32 and counter < 48):
        return ((x | ~y) ^ z)
    elif (counter >= 48 and counter < 64):
        return ((x & z) | (y & ~z))
    else:
        return (x ^ (y | ~z))

def cicleShift(value, shift):
    mainPart = (value << shift) % 0x100000000   #сдвинули влево слово на 32 - shift позиций
    secPart = value >> (32 - shift)             #сдвинутые первые shift бит засунули в конец
    return mainPart + secPart

def ripeMdHashing(sourceArr):
    wordsArr = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]
    
    codArr = []             #массив для хранения текущего потока из 16 слов
    for i in range(16):
        codArr.append([])

    copyArr = []            # массив с временной копией слов искомого хэша
    for i in range(5):
        copyArr.append([])
    hidCopyArr = []
    for i in range(5):
        hidCopyArr.append([])
    constArr = [0x00000000, 0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xa953fd4e]
    hidConstArr = [0x50a28be6, 0x5c4dd124, 0x6d703ef3, 0x7a6d76e9, 0x00000000]
    mixArr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
              7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
              3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
              1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
              4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]
    hidMixArr = [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
                 6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
                 15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
                 8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
                 12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]
    shiftLeftArr = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
                    7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
                    11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
                    11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
                    9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
    hidShiftLeftArr = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
                       9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
                       9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
                       15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
                       8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
    
    for i in range(len(sourceArr) / 16):
        for j in range(16):
            codArr[j] = sourceArr[i * 16 + j]
            
        for j in range(5):
            copyArr[j] = wordsArr[j]
            hidCopyArr[j] = wordsArr[j]

        for j in range(80):
            temp = (cicleShift(((copyArr[0] +\
                               magicFun(j, copyArr[1], copyArr[2], copyArr[3]) +\
                               codArr[mixArr[j]] + constArr[int(j / 16)]) & 0xffffffff),
                               shiftLeftArr[j]) + copyArr[4]) & 0xffffffff
            copyArr[0] = copyArr[4]
            copyArr[4] = copyArr[3]
            copyArr[3] = cicleShift(copyArr[2], 10)
            copyArr[2] = copyArr[1]
            copyArr[1] = temp

            temp = (cicleShift(((hidCopyArr[0] +\
                               magicFun(79 - j, hidCopyArr[1], hidCopyArr[2],
                                        hidCopyArr[3]) +\
                                 codArr[hidMixArr[j]] + hidConstArr[int(j / 16)]) &\
                                0xffffffff),
                               hidShiftLeftArr[j]) + hidCopyArr[4]) & 0xffffffff
            hidCopyArr[0] = hidCopyArr[4]
            hidCopyArr[4] = hidCopyArr[3]
            hidCopyArr[3] = cicleShift(hidCopyArr[2], 10)
            hidCopyArr[2] = hidCopyArr[1]
            hidCopyArr[1] = temp
            
        temp = (wordsArr[1] + copyArr[2] + hidCopyArr[3]) & 0xffffffff
        for i in range(4):
            wordsArr[i + 1] = (wordsArr[(i + 2) % 5] + copyArr[(i + 3) % 5] +\
                              hidCopyArr[(i + 4) % 5]) & 0xffffffff
        wordsArr[0] = temp
        
    return wordsArr

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
		
    plainText = plainText + chr(0x80)  #добавляем байт 0х80 в конец файла

    while (len(plainText) % 0x40) != 0x38:
        plainText = plainText + chr(0x00) #добавляем байты 0x00, пока длина потока не станет 
                                            #сравнима с 448 по модулю 512
    lenArr = intTo8Hex(plainTextLen)        #найти 64-х битное рпедставление длины файла

    for i in range(8):
        plainText = plainText + chr(lenArr[i]) #добавляем представление длины в конец потока

    plainTextLen = len(plainText)

    ripeMdArr = []
    for i in range(plainTextLen / 4):
        value = 0
        for j in range(4):
            value = value + (ord(plainText[i * 4 + j]) << (j * 8))  #обращаем порядок байт в каждом слове
        ripeMdArr.append(value)

    for i in range(5):
        firstByte = (ripeMdSum[i] & 0x000000ff) << 24  #обращаем порядок байт в словах выходного буфера
        secByte = (ripeMdSum[i] & 0x0000ff00) << 8
        thirByte = (ripeMdSum[i] & 0x00ff0000) >> 8
        fourByte = (ripeMdSum[i] & 0xff000000) >> 24
        ripeMdSum[i] = firstByte + secByte + thirByte + fourByte

    with open(destinFileName, 'wb') as resFile:
        for i in range(5):
            stringToFile = hex(ripeMdSum[i])[2:-1]
            addString = '0' * (8 - len(stringToFile))
            resFile.write(addString + stringToFile)

    print "Hash algorithm ripemd-160 has been calculated successfully!"
        
if __name__ == "__main__":
    main()
