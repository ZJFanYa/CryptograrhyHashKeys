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
    print "	source file name - file with a plain text"
    print "     result file name - file with a hash sum of source file"

def intTo8Hex(value):       #функция представления длины потока в 64-х битах 
    value = value * 8       #получаем длину потока в битах
    resArr = []
    for i in range(8):
        resArr.append([])   #готовим массив для длины потока
    for j in range(2):  
        for i in range(4):
            resArr[(3 - i) + 4 * (1 - j)] = value % 0x100   #сначала идет старшее слово
            value = value / 0x100

    return resArr       #массив с представленной в нем длиной текста в битах

def cicleShift(value, shift):
    mainPart = (value << shift) % 0x100000000   #сдвинули влево слово на 32 - shift позиций
    secPart = value >> (32 - shift)             #сдвинутые первые shift бит засунули в конец
    return mainPart + secPart

def sha1Hashing(sourceArr):
    wordsArr = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0] #array with hash values
    constArr = [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6]             #array with additionals constants
    
    codArr = []             #массив для хранения текущего потока из 16 слов
    for i in range(16):
        codArr.append([])

    copyArr = []            # массив с временной копией слов искомого хэша
    for i in range(5):
        copyArr.append([])

    cicleArr = []           #array for keeping 80 32-bits words
    for i in range(80):
        cicleArr.append([])
        
    for i in range(len(sourceArr) / 16):
        for j in range(16):
            codArr[j] = sourceArr[i * 16 + j] #fill current 16 32-bits block
            
        for j in range(5):
            copyArr[j] = wordsArr[j]    #do temporary copy of hash values array

        for j in range(16):             #first 16 words of cicle array is
            cicleArr[j] = codArr[j]     #16 words of current block
        for j in range(16, 80):
            cicleArr[j] = cicleShift((cicleArr[j - 3] ^ cicleArr[j - 8] ^ cicleArr[j - 14] ^\
                          cicleArr[j - 16]), 1) #other 64 words are calculated on formuls
            
        for j in range(80):
            if j < 20:
                funcNow = (wordsArr[1] & wordsArr[2]) | ((~(wordsArr[1])) & wordsArr[3])
            elif (j >= 40 and j < 60):
                funcNow = (wordsArr[1] & wordsArr[2]) | (wordsArr[1] & wordsArr[3]) |\
                          (wordsArr[2] & wordsArr[3])
            else:
                funcNow = wordsArr[1] ^ wordsArr[2] ^ wordsArr[3]
            temp = (cicleShift(wordsArr[0], 5) +\
                   funcNow + wordsArr[4] +\
                   cicleArr[j] + constArr[int(j / 20)]) % 0x100000000
            wordsArr[4] = wordsArr[3]
            wordsArr[3] = wordsArr[2]
            wordsArr[2] = cicleShift(wordsArr[1], 30)
            wordsArr[1] = wordsArr[0]
            wordsArr[0] = temp
                
        for j in range(5):
            wordsArr[j] = (wordsArr[j] + copyArr[j]) % 0x100000000
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
    lenArr = intTo8Hex(plainTextLen)        #найти 64-х битное представление длины файла

    for i in range(8):
        plainText = plainText + chr(lenArr[i]) #добавляем представление длины в конец потока

    plainTextLen = len(plainText)

    sha1Arr = []
    for i in range(plainTextLen / 4):   #split source data to the 32-bits words
        value = 0
        for j in range(4):
            value = value + (ord(plainText[i * 4 + j]) << ((3 - j) * 8))  #words order is stright
        sha1Arr.append(value)

    sha1Sum = sha1Hashing(sha1Arr)      #calculate sha1-hash sum

    with open(destinFileName, 'wb') as resFile:     #write result to the file
        for i in range(5):
            stringToFile = hex(sha1Sum[i])[2:-1]    #take only words from the hex-string, throw unnecessary symbols
            addString = '0' * (8 - len(stringToFile))   #add necessary number of zeroes
            resFile.write(addString + stringToFile)     

    print "Hash algorithm md5 has been calculated successfully!"
        
if __name__ == "__main__":
    main()
