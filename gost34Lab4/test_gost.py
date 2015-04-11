import subprocess
import pytest
import gost34Lab4

def run_cmd(cmd, input=None):
    pr = subprocess.Popen(cmd,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    return pr.communicate(input=input)

def get_text_digest(text):
    openssl_sign_cmd = ['openssl', 'dgst', '-hex', '-md_gost94']

    out, err = run_cmd(openssl_sign_cmd, input=text)

    if err:
        raise ValueError('OpenSSL error: %s' % err)

    out = out[9:-1]

    return out

def test_testStr():
    testStr = "The quick brown fox jumps over the lazy dog"
    result = get_text_digest(testStr)
    print result
    assert result == gost34Lab4.gostHashing(testStr)
    
def test_empty():
    empty = ""
    result = get_text_digest(empty)
    assert result == gost34Lab4.gostHashing(empty)

def test_string():
    string = "message digest"
    result = get_text_digest(string)
    assert result == gost34Lab4.gostHashing(string)
