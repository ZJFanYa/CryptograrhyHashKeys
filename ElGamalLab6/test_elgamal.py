import pytest
import ElGamalLab6
import random
import bigNumDLL

def test_testStr():
    bitsLen = 128

    y, g, p, x = ElGamalLab6.keyGen(bitsLen)
    
    message = bigNumDLL.bigNum()
    flag = True
    while flag:
        message.getRandBigNum(bitsLen)
        if message < p:
            flag = False

    a, b = ElGamalLab6.encrypt(message, g, y, p, bitsLen)

    result = ElGamalLab6.decrypt(b, a, x, p)

    assert message == result
