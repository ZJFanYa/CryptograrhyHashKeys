import MD5Lab1_v2
import SHA1Lab2_v2
import ripeMDLab3_v2
import hashlib

testStr = "The quick brown fox jumps over the lazy dog"

def test_md5():
    result = hashlib.md5(testStr).hexdigest()
    assert result == MD5Lab1_v2.md5Hashing(testStr)
    
def test_sha1():
    result = hashlib.sha1(testStr).hexdigest()
    assert result == SHA1Lab2_v2.sha1Hashing(testStr)

def test_ripemd():
    result = hashlib.new('ripemd160')
    result.update(testStr)
    result = result.hexdigest()
    assert result == ripeMDLab3_v2.ripeMdHashing(testStr)
