from django.shortcuts import render,HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import math
import random
import numpy as np
# Create your views here.
def homepage(request):
    return render(request,'index.html')


# Create your views here.
#Begin functions for Caesar Cipher
alphabets = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower())

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num ** 0.5) + 2, 2):
        if num % n == 0:
            return False
    return True
def toNum(char):
    return alphabets.index(char)


def toChar(num):
    num %= 26
    return alphabets[num]
def caesar_cipher_encrypt(message, key):
    encrypted_message = ""
    for letter in message:
        if letter.isalpha():
            encrypted_message += toChar((toNum(letter) + key))
        else:
            encrypted_message += letter
    return encrypted_message

def caesar_cipher_decrypt(message, key):
    decrypted_message = ""
    for letter in message:
        if letter.isalpha():
            decrypted_message += toChar((toNum(letter) - key))
        else:
            decrypted_message += letter
    return decrypted_message

def caesar_cipher(request):
    message_to_encrypt = ""
    message_to_decrypt = ""
    key = 0
    encryptedMessage = ""
    decryptedMessage = ""
    if request.method == 'POST':
        key = request.POST.get('key')
        if request.POST.get('encrypt'):
            message_to_encrypt = request.POST.get('message')
            encryptedMessage = caesar_cipher_encrypt(message_to_encrypt, int(key))
        elif request.POST.get('decrypt'):
            message_to_decrypt = request.POST.get('message')
            decryptedMessage = caesar_cipher_decrypt(message_to_decrypt, int(key))  
    return render(request,"caesar_cipher.html",{'encryptedMessage':encryptedMessage,'decryptedMessage':decryptedMessage,'message_to_encrypt':message_to_encrypt,'message_to_decrypt':message_to_decrypt,'key':key})
#End functions for Caesar Cipher

#Begin functions for Playfair Cipher
def fillPlayfairMatrix(key):
    key = (key + "abcdefghijklmnopqrstuvwxyz").upper().replace("J", "I")
    key = list(dict.fromkeys(key))
    return np.array(list(np.array(key).reshape(5, 5)))


def playfair_cipher_process(plainText):
    plainText = plainText.replace(" ", "").upper().replace("J", "I")
    for i in range(0, len(plainText), 2):
        if i < len(plainText) - 1 and plainText[i] == plainText[i + 1]:
            plainText = plainText[: i + 1] + "X" + plainText[i + 1 :]
    if len(plainText) % 2 != 0:
        plainText += "X"
    chunks = np.array(list(plainText)).reshape(int(len(plainText) / 2), 2)
    return chunks


def playfair_cipher_getCoordinates(letter, matrix):
    for i in range(0, 5):
        for j in range(0, 5):
            if matrix[i][j] == letter:
                return i, j


def playfair_cipher_encrypt(plainText, key):
    matrix = fillPlayfairMatrix(key)
    chunks = playfair_cipher_process(plainText)
    encrypted = ""
    for i in range(0, len(chunks)):
        x1, y1 = playfair_cipher_getCoordinates(chunks[i][0], matrix)
        x2, y2 = playfair_cipher_getCoordinates(chunks[i][1], matrix)
        if x1 == x2:
            encrypted += matrix[x1][(y1 + 1) % 5] + matrix[x2][(y2 + 1) % 5]
        elif y1 == y2:
            encrypted += matrix[(x1 + 1) % 5][y1] + matrix[(x2 + 1) % 5][y2]
        else:
            encrypted += matrix[x1][y2] + matrix[x2][y1]
    return encrypted


def playfair_cipher_decrypt(ciphertext, key):
    matrix = fillPlayfairMatrix(key)
    chunks = playfair_cipher_process(ciphertext)
    decrypted = ""
    for i in range(0, len(chunks)):
        x1, y1 = playfair_cipher_getCoordinates(chunks[i][0], matrix)
        x2, y2 = playfair_cipher_getCoordinates(chunks[i][1], matrix)
        if x1 == x2:
            decrypted += matrix[x1][(y1 - 1) % 5] + matrix[x2][(y2 - 1) % 5]
        elif y1 == y2:
            decrypted += matrix[(x1 - 1) % 5][y1] + matrix[(x2 - 1) % 5][y2]
        else:
            decrypted += matrix[x1][y2] + matrix[x2][y1]
    return decrypted

def playfair_cipher(request):
    message_to_encrypt = ""
    message_to_decrypt = ""
    keyword = ""
    encryptedMessage = ""
    decryptedMessage = ""
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        if request.POST.get('encrypt'):
            message_to_encrypt = request.POST.get('message')
            encryptedMessage = playfair_cipher_encrypt(message_to_encrypt, keyword)
        elif request.POST.get('decrypt'):
            message_to_decrypt = request.POST.get('message')
            decryptedMessage = playfair_cipher_decrypt(message_to_decrypt, keyword)
    return render(request,"playfair_cipher.html",{'message_to_encrypt':message_to_encrypt,'message_to_decrypt':message_to_decrypt,'keyword':keyword,'encryptedMessage':encryptedMessage,'decryptedMessage':decryptedMessage})

#End functions for Playfair Cipher

#Before functions for Vignere Cipher

alphabets = list("abcdefghijklmnopqrstuvwxyz".lower())


def vignere_cipher_encrypt(plainText, key):
    cipherText = ""
    for i in range(len(plainText)):
        cipherText += alphabets[
            (alphabets.index(plainText[i]) + alphabets.index(key[i])) % 26
        ]
    return cipherText


def vignere_cipher_matchKey(plainText, key):
    key = key * math.floor(len(plainText) / len(key)) + key[:len(plainText) % len(key)]
    return key


def vignere_cipher_decrypt(cipherText, key):
    plainText = ""
    for i in range(len(cipherText)):
        plainText += alphabets[
            (alphabets.index(cipherText[i]) - alphabets.index(key[i])) % 26
        ]
    return plainText

def vignere_cipher(request):
    message_to_encrypt = ""
    message_to_decrypt = ""
    key = ""
    encryptedMessage = ""
    decryptedMessage = ""
    if request.method == "POST":
        if request.POST.get('encrypt'):
            message_to_encrypt = "".join(request.POST.get('message').strip().split(" "))
            key = vignere_cipher_matchKey(message_to_encrypt,request.POST.get('keyword'))
            if(not(message_to_encrypt.isalpha() and str(key).isalpha())):
                return HttpResponse("<script>alert('Only Aphabet input will be accepted. Numerical and special characters are not allowed.');history.back()</script>")
            encryptedMessage = vignere_cipher_encrypt(message_to_encrypt, key)
        elif request.POST.get('decrypt'):
            message_to_decrypt = "".join(request.POST.get('message').strip().split(" "))
            key = vignere_cipher_matchKey(message_to_decrypt,request.POST.get('keyword'))
            decryptedMessage = vignere_cipher_decrypt(message_to_decrypt, key)
    return render(request,'vignere_cipher.html',{'message_to_encrypt':message_to_encrypt,'message_to_decrypt':message_to_decrypt,'keyword':key,'encryptedMessage':encryptedMessage,'decryptedMessage':decryptedMessage})

#End functions for Vignere Cipher

def hill_cipher(request):
    return HttpResponse("Hill Cipher...")

#Begin functions for RSA CipherText

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def eea(a, b):
    if b == 0:
        return (1, 0)
    (q, r) = (a // b, a % b)
    (s, t) = eea(b, r)
    return (t, s - (q * t))


def find_inverse(x, y):
    inv = eea(x, y)[0]
    if inv < 1:
        inv += y  # we only want positive values
    return inv





def rsa_generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        return (False,0)
    elif p == q:
        return (False,1)
    # n = pq
    n = p * q
    # Phi is the totient of n
    phi = (p - 1) * (q - 1)
    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    e=17
    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
        print(e)

    # Use Extended Euclid's Algorithm to generate the private key
    d = find_inverse(e, phi)
    while e==d:
        i=2
        d = find_inverse(e, phi**i)
        i+=1

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def rsa_cipher_encrypt(pk, message):  
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = (message ** int(key)) % int(n)
    # Return the array of bytes
    return cipher


def rsa_cipher_decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = (ciphertext ** int(key)) % n
    # Return the array of bytes as a string
    return plain

def rsa_cipher(request):
    p=""
    q=""
    publicKey = ""
    privateKey = ""
    message_to_encrypt = ""
    encryptedMessage = ""
    message_to_decrypt = ""
    decryptedMessage = ""
    if request.method == 'POST':
        if request.POST.get('genkey'):
            p = int(request.POST.get('p'))
            q = int(request.POST.get('q')) 
            request.session['p'] = p
            request.session['q'] = q         
            publicKey , privateKey = rsa_generate_keypair(p,q)
            if(publicKey==False and privateKey==0):
                return HttpResponse("<script>alert('Both p and q must be prime numbers');history.back()</script>")
            elif(publicKey==False and privateKey==1):
                return HttpResponse("""<script>alert("p and q shouldn't be equal");history.back()</script>""")

            request.session['publicKey'] = publicKey
            request.session['privateKey'] = privateKey
        if request.POST.get('encrypt'):
            p = request.session.get('p')
            q = request.session.get('q')
            privateKey = tuple(request.session.get('privateKey'))
            message_to_encrypt = int(request.POST.get('message'))
            publicKey = tuple(int(num) for num in request.POST.get('key').replace('(',"").replace(')',"").split(","))
            encryptedMessage = rsa_cipher_encrypt(publicKey,message_to_encrypt)
        elif request.POST.get('decrypt'):
            p = request.session.get('p')
            q = request.session.get('q')
            publicKey = tuple(request.session.get('publicKey'))
            message_to_decrypt = int(request.POST.get('message'))
            privateKey = tuple(int(num) for num in request.POST.get('key').replace('(',"").replace(')',"").split(","))
            decryptedMessage = rsa_cipher_decrypt(privateKey,message_to_decrypt)
    return render(request,'rsa_cipher.html',{'p':p,'q':q,'publicKey':publicKey,'privateKey':privateKey,'message_to_encrypt':message_to_encrypt,'encryptedMessage':encryptedMessage,'message_to_decrypt':message_to_decrypt,'decryptedMessage':decryptedMessage})

#End functions for RSA CipherText

# Begin functions for ELGamal CipherText  

def elgamal_cipher(request):
    p =g=a=key=c1=c2= ""
    message_to_encrypt = ""
    encrKey = ""
    sec_a = ""
    message = ""
    if request.method == 'POST':
        if request.POST.get('genkey'):
            p = int(request.POST.get('p'))
            g = int(request.POST.get('g'))
            a = int(request.POST.get('a'))
            request.session['p'] = p
            request.session['g'] = g
            request.session['a'] = a
            if(not is_prime(p)):
                return HttpResponse("<script>alert('p must be prime number');history.back()</script>")
            alpha = (g**a)%p
            key=encrKey = (p,g,alpha)
            request.session['key'] = key
            request.session['alpha'] = alpha

        elif request.POST.get('encrypt'):
            p = request.session.get('p')
            g = request.session.get('g')
            a = request.session.get('a')
            key = tuple(request.session.get('key'))
            prime,gen,alpha= encrKey = tuple(int(num) for num in request.POST.get('key').replace('(',"").replace(')',"").split(","))
            message_to_encrypt = int(request.POST.get('message'))
            if(message_to_encrypt >= p-1):
                return HttpResponse("<script>alert('m should be less than p-1');history.back()</script>")
            r = random.randrange(1,prime-1)
            rem = gcd(r,prime-1)
            while rem != 1:
                r = random.randrange(1,prime-1)
                rem = gcd(r,prime-1)
            c1 = (gen**r)%prime
            c2 = (message_to_encrypt* alpha**r)%prime
            request.session['c1'] = c1
            request.session['c2'] = c2
            request.session['encrKey'] = encrKey
            request.session['message_to_encrypt'] = message_to_encrypt

        elif request.POST.get('decrypt'):
            p = int(request.session.get('p'))
            g = request.session.get('g')
            a = request.session.get('a')
            encrKey = tuple(request.session.get('encrKey')) or None
            message_to_encrypt = request.session.get('message_to_encrypt')
            key = tuple(request.session.get('key'))
            c1 = int(request.POST.get('c1'))
            c2 = int(request.POST.get('c2'))
            sec_a = int(request.POST.get('a'))
            message = (find_inverse((c1 ** sec_a) % p, p) * (c2 % p)) % p


    return render(request,'elgamal_cipher.html',{'p':p,'g':g,'a':a,'key':key,'encrKey':encrKey,'c1':c1,'c2':c2,'message_to_encrypt':message_to_encrypt,'sec_a':sec_a,'message':message})


# End functions for ELGamal CipherText