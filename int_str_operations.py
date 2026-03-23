import math

# Simple transform string to int using UTF-8 encoding
def string_to_int(s):
   return int.from_bytes(s.encode(), byteorder='little')

# Simple transform int to string using UTF-8 encoding
def int_to_string(i):
    length = math.ceil(i.bit_length() / 8)
    return i.to_bytes(length, 'little').decode('utf-8')

# Prepare string for encryption
def prepare_string_for_encryption(s):
    # 1. transform string to int using UTF-8 encoding 
    sentence_ID = string_to_int(s)
    sentence_ID=str(sentence_ID)

    # 2. if necessary add 0 at the beginning to get the right length
    if len(sentence_ID)%3==1:
        sentence_ID="00"+sentence_ID #wstawienie 0 na poczatku by uzyskac dobra dlugosc - podzial na 3 bedzie pozniej
    if len(sentence_ID)%3==2:
        sentence_ID="0"+sentence_ID #wstawienie 0 na poczatku by uzyskac dobra dlugosc - podzial na 3 bedzie pozniej

    # 3. split numeric value to frames of max 3 digits
    sentence_ID=([sentence_ID[i:i+3] for i in range(0, len(sentence_ID), 3)])
    return sentence_ID

# Prepare string for decryption
def read_string_after_decryption(sentence_ID):
    newstring=[]
    # 1. make sure frames contain 3-digit numbers - after converting to int and performing the necessary calculations 0s at the beginning are lost
    # To fix this, we check the value of each frame and add 0s at the beginning if necessary to make it 3-digit number again
    for i in range (len(sentence_ID)):
        if sentence_ID[i] < 10:
            newstring+=["00"+str(sentence_ID[i])]
        elif sentence_ID[i] < 100:
            newstring+=["0"+str(sentence_ID[i])]
        else:
            newstring+=[str(sentence_ID[i])]

    # 2. convert list of frames to one int and then transform it to string using UTF-8 encoding
    newstring = int(''.join(newstring))
    sentence = int_to_string(newstring)
    return sentence