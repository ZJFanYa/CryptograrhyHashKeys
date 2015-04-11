# -*- coding:utf-8 -*-

import sys
import math

def checkParam(paramsNum, arguments): #проверка того, что параметры командной строки
    if (paramsNum != 3):                #введены верно
        print "There is wrong number of parameters. Main string was entered incorrectly."
        return False
    
    return True
	
def PrintStart():
    print "This programme encodes the source file according\
        to GOST-34.11-94 hash algorithm "
    print "Main string should be in a such way: "
    print "[python file name] [source file name] [result file name]"
    print "	python file name - name of file with a program"
    print "	source file name - file with the plain text"
    print "     result file name - file with a hash sum of source file"

def cicleShift(value, shift):
    mainPart = (value << shift) % 0x100000000   #сдвинули влево слово на 32 - shift позиций
    secPart = value >> (32 - shift)             #сдвинутые первые shift бит засунули в конец
    return mainPart + secPart

def intToArr(value, intLen, elemLen):       #функция представления длины потока в 64-х битах 
    resArr = []
    lenArr = intLen / elemLen
    for i in range(lenArr):
        resArr.append([])   #готовим массив для длины потока
    for i in range(lenArr):  
        resArr[lenArr - 1 - i] = value % (2 ** elemLen)   #сначала идет младшее слово
        value = value / (2 ** elemLen)
    return resArr       #массив с представленной в нем длиной текста в битах

def arrToInt(valueArr, elemLen):
    resVal = 0
    arrLen = len(valueArr)
    for i in range(arrLen):
        resVal = resVal + (valueArr[arrLen - 1 - i] << (i * elemLen))
    return resVal

def pMix(intForMix):    #pMix function for keys generation
    arrForMix = intToArr(intForMix, 256, 8)
    pMixArr = []
    for i in range(32):
        pMixArr.append(arrForMix[(i % 4) * 8 + int(i / 4)])
    pMixInt = arrToInt(pMixArr, 8)
    return pMixInt

def aMix(intForMix):  #aMix function for keys generation
    arrForMix = intToArr(intForMix, 256, 64)
    aMixArr = []
    aMixArr.append(arrForMix[2] ^ arrForMix[3])
    aMixArr.append(arrForMix[0])
    aMixArr.append(arrForMix[1])
    aMixArr.append(arrForMix[2])
    aMixInt = arrToInt(aMixArr, 64)
    return aMixInt

def keysGenerate(inp, curBlock):    #keys generation function
    keysArr = []
    for i in range(4):
        keysArr.append([])
    constArr = [0, 0xff00ffff000000ffff0000ff00ffff0000ff00ff00ff00ffff00ff00ff00ff00, 0]
    firstHalf = inp
    secHalf = curBlock
    pretender = firstHalf ^ secHalf
    keysArr[0] = pMix(pretender)

    for i in range(1, 4):
        uInt = aMix(firstHalf)
        firstHalf = uInt ^ constArr[i - 1]
        vInt = aMix(secHalf)
        secHalf = aMix(vInt)
        pretender = firstHalf ^ secHalf
        keysArr[i] = pMix(pretender)

    return keysArr

def magFun(part, key):          #magic function for gost 28147-89 
    Sbox = [10, 4, 5, 6, 8, 1, 3, 7, 13, 12, 14, 0, 9, 2, 11, 15,
            5, 15, 4, 0, 2, 13, 11, 9, 1, 7, 6, 3, 12, 14, 10, 8,
            7, 15, 12, 14, 9, 4, 1, 0, 3, 11, 5, 2, 6, 10, 8, 13,
            4, 10, 7, 12, 0, 15, 2, 8, 14, 1, 6, 5, 13, 11, 9, 3,
            7, 6, 4, 11, 9, 12, 2, 10, 1, 8, 0, 14, 15, 13, 3, 5,
            7, 6, 2, 4, 13, 9, 15, 0, 10, 1, 5, 11, 8, 14, 12, 3,
            13, 14, 4, 1, 7, 0, 5, 10, 3, 12, 8, 15, 6, 2, 9, 11,
            1, 3, 10, 9, 5, 11, 4, 15, 8, 6, 7, 14, 13, 0, 2, 12]
                            #constant replace table
    out = (part + key) & 0xffffffff

    outArr = []
    for i in range(8):
        outArr.append(out % 0x10)
        out = out / 0x10

    for i in range(8):
        outArr[i] = Sbox[i * 16 + outArr[i]]

    calc = 0
    for i in range(8):
        calc = calc + (outArr[i] << (i * 4))    #replace block
                                            #according to table
    calc = cicleShift(calc, 11)
    return calc

def cipherGost(data, key):    #gost 28147-89 function
    oldPart = data >> 32      #divide input value to big and little parts
    youngPart = data & 0xffffffff
    
    subKeys = intToArr(key, 256, 32)    #split key to 8 32-bits subkeys
    
    subKeysArr = []                     #form 32 subkeys 
    for i in range(32):
        subKeysArr.append([])
    for i in range(24):
        subKeysArr[i] = subKeys[7 - (i % 8)]
        
    for i in range(24, 32):
        subKeysArr[i] = subKeys[i % 8]

    for i in range(32):                 #algorythm of gost 28147-89
        newYoungPart = oldPart ^ magFun(youngPart, subKeysArr[i])
        oldPart = youngPart
        youngPart = newYoungPart

    cipher = (youngPart << 32) + oldPart        #little part get big, and vice versa
    return cipher

def cipherMix(inp, ciphKeys):               #ciphered mixing function
    outArr = []
    for i in range(4):
        outArr.append([])

    inArr = intToArr(inp, 256, 64)          #divide 256-bits hashIn to
                                            #4 64-bits blocks
    for i in range(4):
        outArr[i] = cipherGost(inArr[i], ciphKeys[3 - i]) #calc
                                       #result value according to gost 28147-89
                                        #algorythm
    out = arrToInt(outArr, 64)
    return out

def simpleShift(shiftInt):                  #function for mixing algorythm
    shiftArr = intToArr(shiftInt, 256, 16)
    resArr = []
    for i in range(16):
        resArr.append([])

    resArr[0] = shiftArr[15] ^ shiftArr[14] ^ shiftArr[13] ^ shiftArr[12] ^\
                shiftArr[3] ^ shiftArr[0]
    for i in range(15):
        resArr[i + 1] = shiftArr[i]
    resInt = arrToInt(resArr, 16)
    return resInt    

def fixMix(inp, fix, curBlock):     #mixing mixing function
    for i in range(12):
        fix = simpleShift(fix)

    act = fix ^ curBlock
    act = simpleShift(act)

    almost = inp ^ act
    for i in range(61):
        almost = simpleShift(almost)

    return almost

def hashRound(hIn, curBlock):
    keys = keysGenerate(hIn, curBlock)  #generate keys for algorythm step
    fixed = cipherMix(hIn, keys)        #do ciphering mixing
    hOut = fixMix(hIn, fixed, curBlock) #do mixing mixing

    return hOut

def splitText(text):
    textNum = []
    for i in range(len(text)):
        textNum.append(ord(text[len(text) - 1 - i]))
    return textNum

def invBytes(value):
    valueArr = intToArr(value, 256, 8)
    invArr = []
    for i in range(32):
        invArr.append(valueArr[31 - i])

    value = arrToInt(invArr, 8)
    return value

def gostHashing(plainText):
    textLen = 0                     #message length in bits
    curBlock = 0                    #current block of message
    controlSum = 0                  #control sum on all blocks
    hashVal = 0                     #result hash

    if plainText:
        constMod = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff #modul for algorithm
        numText = splitText(plainText)                              #invert bytes in the message 
        
        textLen = (len(numText) * 8) & constMod                 
        
        if not textLen % 0x100:                                     
            roundsNum = textLen / 0x100                         #calculate number of steps in algorithm
        else:
            roundsNum = int(textLen / 0x100) + 1
                                          
        blockArr = []                                           
        for i in range(32):
            blockArr.append([])

        for i in range(roundsNum - 1):              #internal algorithm iteration
            for j in range(32): 
                blockArr[31 - j] = numText[len(numText) - 1 - i * 32 - j]   #fill current block from end of
                                                                             #message
            curBlock = arrToInt(blockArr, 8)
            controlSum = (controlSum + curBlock) & constMod              #calc temporary control sum
            hashVal = hashRound(hashVal, curBlock)                      #do algorithm step

        for i in range(32):
            blockArr[i] = 0                                 #fill last block by nulls
        count = 0
        while((len(numText) - 1 - (roundsNum - 1) * 32 - count) >= 0):
            blockArr[31 - count] = numText[len(numText) - 1 - (roundsNum - 1) *\
                                           32 - count]     #fill last block by data, while it is
            count = count + 1
        curBlock = arrToInt(blockArr, 8)                #convert to value
        controlSum = (controlSum + curBlock) & constMod #calc temporary control sum
	hashVal = hashRound(hashVal, curBlock)      #do external algorythm iteration        
    
    hashVal = hashRound(hashVal, textLen)       #do algorythm length step
    hashVal = hashRound(hashVal, controlSum)    #do algorythm sum step

    hashVal = invBytes(hashVal)
    
    for i in range(4):
        stringToFile = hex(hashVal)[2:-1]       #form result hash string
        addString = '0' * (64 - len(stringToFile)) #write nulls at the left side
        resStr = addString + stringToFile
        
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

    gostSum = gostHashing(plainText)

    with open(destinFileName, 'wb') as resFile:
        resFile.write(gostSum)

    print "Hash algorithm gost 34.11-94 has been calculated successfully!"
        
if __name__ == "__main__":
    main()
