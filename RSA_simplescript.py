# Script Name: RSA_simplepresentation.py
# Description: An attempt to represent the RSA algorithm in a simple way. 
# Author: J45K1ER
# Version: 1.0
# Date: 2026-03-22
#
# In this attempt I tried to represent how RSA encryption worksusing only basic Python libraries and functions.
# To keep it painfully simple any optimizations or advanced techniques were avoided. The main goal is to show how the RSA algorithm works in a clear and understandable way.
# Here you will find mathematical steps with short explanations without getting into the details of the implementation or the mathematical theory background.
#
# Usage:
#   RSA_simplepresentation.py <prime p> <prime q> <file.txt>
#
# Example:
#   python RSA_simplepresentation.py 61 53 msg_to_be_encrypted.txt
#
# Dependencies:
#   None (Pure Python implementation)
#
# License:
#   GNU General Public License v3.0 (see LICENSE file for details)

from random import randrange
import sys
import int_str_operations

# Loading the contents of the txt file
def read_txt_file(filename):
   with open(filename, 'r', encoding='utf-8') as sentence:
            return sentence.read()

# Finding prime numbers < n
def primenumber(MyNum):
  n = 0
  i = 2
  for i in range(2,MyNum//2+1):
    if MyNum % i == 0:
      n = n + 1
      break
  if n == 0:
    return MyNum

# Extended Euclidean Algorithm - finding GCD
def gcdExtended(a,b):
    # Base Case
    if a==0:
       return b,0,1
    
    gcd,x1,y1 = gcdExtended(b%a,a)

    # Update x and y using results of recursive
    x=y1-(b//a)*x1
    y=x1
    return gcd,x,y

# function to determine all prime numbers in the ring Zn
def compute_Zn_primes(n):
    primes = []
    for i in range(2, n+1):
        prime = primenumber(i)
        if prime != None:
            primes.append(prime)
    return primes

# function to check if a meets its conditions: (1<e<phi and gcd(e, phi) = 1) - doing so we ensure, that a is invertible
def check_a(a, d, phi, primes):
    if d == primes[randrange(len(primes))]:
        #check relation between a and d: (a*d)%phi should be equal 1 (d⋅a≡1(modϕ(n))) -> if so, encryption and decryption are inverse operations
        check = (d*a)%phi
        if check == 1:
            # print the results
            print ("\nd = ",d, "\nphi = ", phi,"\ncheck = ",check)            
            return True
    else:
        return False


#Step 1: Choose two prime numbers
p = sys.argv[1]
q = sys.argv[2]
sentence = read_txt_file(sys.argv[3])
#liczby p i q do n=p*q + weryfikacja inputu
while True:
    p = int(p)
    q = int(q)
    if p==q:
        print("\nLiczby p i q nie mogą być takie same. Proszę podać różne liczby.")
    elif p*q<1000:
        print("\nLiczby p i q są zbyt małe. Proszę podać większe liczby. (p*q>999)")
    else:
       break

#obliczenie n
#Step 2: Compute modulus N - it defines the working ring Zn
N=p*q
#Step 3: Compute Euler’s Totient Function - it determines the size of the multiplicative group Zn* (phi(n))
phi=(p-1)*(q-1)

#Step 4: Find all prime numbers in the ring Zn - it will be used to check is public exponent a meets its conditions: (1<e<phi and gcd(e, phi) = 1)
primes = compute_Zn_primes(phi)

#Step 5: Choose public exponent a and private exponent d
while True:
    #Pick a random prime number a from the ring Zn
    a=primes[randrange(len(primes))]

    #Determine the inverse element d of a in the ring Zn using Extended Euclidean Algorithm
    g, x, y = gcdExtended(a, phi)
    d = phi+x
    #Check does a meets its conditions: (1<e<phi and gcd(e, phi) = 1) - doing so we ensure, that a is invertible
    if check_a(a, d, phi, primes)==1:
        break

#Step 6: Publish the public key (a, N) and keep the private key (d, N) secret
print("RSA keys generated succesfully:\nPublic key: ",a,", ",N,"\nPrivate key: ",d,", ",N)

# Print plain text that will be encrypted and then, decrypted
print ("Source plain text: ",sentence)

# Prepare string for encryption - transform string to int, make its length divisible by 3 and split it to 3-digit frames
sentence_ID = int_str_operations.prepare_string_for_encryption(sentence)

# Step 7: Encryption - for each element from the sentence ID list (3-digit frames) we perform the following operations: (element^a)%N
print ("Source text before encryption: ",sentence_ID)
for i in range(len(sentence_ID)):
  sentence_ID[i]=(int(sentence_ID[i])**a)%N
print ("Text after encryption: ",sentence_ID)

# Step 8: Decryption - for each element from the sentence ID list we perform the following operations: (element^d)%N
for i in range(len(sentence_ID)):
  sentence_ID[i]=(int(sentence_ID[i])**d)%N
print("Text after decryption: ", sentence_ID)

# Read string after decryption - make sure frames contain at least 3 digits, convert list of frames to one int and then transform it to string
sentence = int_str_operations.read_string_after_decryption(sentence_ID)

# Print decrypted message
print ("Decrypted message: ",sentence)