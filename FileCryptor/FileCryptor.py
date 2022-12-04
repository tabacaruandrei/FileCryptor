
import sys
import os
import hashlib
import traceback


def hash(filePath):
    try:
        m = hashlib.sha1()
        f = open(filePath,"rb")
        while True:
            data = f.read(4096)
            if len(data)==0: 
                break
            m.update(data)
        f.close()
        return m.hexdigest()
    except:
        return ""


def crypt(file,pw):
    try:
        data = open(file, 'rt', encoding="utf-8")
        k = 0
        newfile = os.path.splitext(file)[0] + '_2' + os.path.splitext(file)[1]
        c = 2
        while os.path.isfile(newfile):
            c += 1
            newfile = os.path.splitext(file)[0] + '_' + str(c) + os.path.splitext(file)[1]
        try:
            crypted = open(newfile, 'w+', encoding="utf-8")
            m = hash(file)
            crypted.write(m)
            crypted.write('\n')
            lastbits = ""
            while(1):
                char = data.read(1)
                if not char:
                    break
                if(ord(char) + ord(pw[k%len(pw)])) > 255:
                    lastbits += bin(ord(char)+ord(pw[k%len(pw)]))[10]
            crypted.write(lastbits)
            crypted.write('\n')
            data.seek(0)
            
            while(1):
                char = data.read(1)
                if not char:
                    data.close()
                    break
                if(ord(char) + ord(pw[k%len(pw)])) > 255:
                    newnumber = int(bin(ord(char)+ord(pw[k%len(pw)]))[2:10],2)
                    newchar = chr(newnumber)
                else:
                    newchar = chr(ord(char) + ord(pw[k%len(pw)]))
                crypted.write(newchar)
                k += 1
            
            crypted.close()
            
            cryptedfile = file + '.crypted'
            d = 1
            while os.path.isfile(cryptedfile):
                d += 1
                cryptedfile = os.path.splitext(file)[0] + '_' + str(d) + os.path.splitext(file)[1] + '.crypted'
            os.rename(newfile, cryptedfile)
        except:
            print('except general 2')
    except FileNotFoundError:
        print('file not found error')
    except:
        print('except general 1')


def decrypt(file,pw):
    # if not os.path.isfile(file):
    #     print('fisierul nu exista.')
    # if os.path.splitext(file)[1] != '.crypted':
    #     print('fisierul are formatul gresit (nu e .crypted la final)')
    # elif os.path.splitext(os.path.splitext(file)[0])[1] != '.txt':
    #     print('fisierul are formatul gresit (nu e .txt.crypted)')
    newfile = os.path.splitext(os.path.splitext(file)[0])[0] + '_2' + os.path.splitext(os.path.splitext(file)[0])[1]
    goodfile = os.path.splitext(file)[0]
    
    c = 2
    while os.path.isfile(newfile):
        c += 1
        newfile = os.path.splitext(os.path.splitext(file)[0])[0] + '_' + str(c) + os.path.splitext(os.path.splitext(file)[0])[1]
    os.rename(file, newfile)
    
    try:
        data = open(newfile, 'rt', encoding="utf-8")
        k = 0
        t = 0 # last bit
        try:
            crypted = open(goodfile, 'a+', encoding="utf-8")
            
            oghash = data.readline().strip()
            
            lastbits = data.readline().strip()
            
            while(1):
                char = data.read(1)
                if not char:
                    break
                if (ord(char) - ord(pw[k%len(pw)])) < 0:
                    newnumber = ord(char) * 2 - ord(pw[k%len(pw)]) + int(lastbits[t])
                    newchar = chr(newnumber)
                    t += 1
                else:
                    newchar = chr(ord(char) - ord(pw[k%len(pw)]))
                crypted.write(newchar)
                k += 1
            data.close()
            os.remove(newfile)
            crypted.close()
        except:
            pass
    except:
        pass


def execinput():
    # INPUT: FileCryptor.py crypt abc.exe my_pass ⇒ va crea fisierul abc.exe.crypted
    # INPUT: FileCryptor.py decrypt abc.exe.cryped my_pass ⇒ va crea fișierul abc.exe
    if (len(sys.argv) - 1) < 3:
        print('Sintaxa incorecta1. Utilizati formatul:\n')
        print('FileCryptor.py [crypt/decrypt] path_fisier parola_criptare')
    else:
        if(sys.argv[1] == 'crypt'):
            crypt(sys.argv[2], sys.argv[3])
        elif(sys.argv[1].lower == 'decrypt'):
            decrypt(sys.argv[2], sys.argv[3])
        else: 
            print('Sintaxa incorecta. Utilizati formatul:\n')
            print('FileCryptor.py [crypt/decrypt] [path_fisier] [parola_criptare]')


if __name__ == "__main__":
    crypt(os.path.join(os.getcwd(), "plaintext.txt"), "ABCD")
    decrypt(os.path.join(os.getcwd(), "plaintext.txt.crypted"),"ABCD")