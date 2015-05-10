import pytest
import FiatShamirLab7
import random
import bigNumDLL
from hypothesis import given

def test_success():
    bitsLen = 128

    modul, openKey = FiatShamirLab7.keyGen(bitsLen)

    pretender = bigNumDLL.bigNum()
    pretender.Read("secret.txt", 1000000000)

    assert True == FiatShamirLab7.proove(modul, openKey, pretender, bitsLen)

def test_fail():
    bitsLen = 128

    modul, openKey = FiatShamirLab7.keyGen(bitsLen)

    random.seed()
    flag = True
    while flag:
        pret = random.getrandbits(bitsLen)
        pretender = bigNumDLL.bigNum(str(pret))
        if pretender < modul:
            flag = False
            
    assert False == FiatShamirLab7.proove(modul, openKey, pretender, bitsLen)
