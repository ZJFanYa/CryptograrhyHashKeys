import pytest
import RSALab5_v2
import random

def test_testStr():
    #testStr = "The quick brown fox jumps over the lazy dog"

    bitsNum = random.randint(0, 512)
    randInt = random.getrandbits(bitsNum)
    testStr = str(randInt)

    print testStr

    source = RSALab5_v2.rsa(testStr)

    print source

    assert testStr == source
