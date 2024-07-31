seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()-=_+[]{}\\|;:',<.>/? \""

def encrypt (text: str) -> str:
    res = ""
    for i in range (len(text)):
        for j in range (len(seed)):
            if text[i] == seed[j]:
                res += seed[(i + j + 100) % (len(seed))]
    return res

def decrypt (text: str) -> str:
    res = ""
    for i in range (len(text)):
        for j in range (len(seed)):
            if text[i] == seed[j]:
                res += seed[(j - i -100) % (len(seed))]
    return res
    
# text = "patin bakar"          
# print(encrypt(text))  
# print(decrypt(encrypt(text)))

