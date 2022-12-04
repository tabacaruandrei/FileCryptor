
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
        # if not os.path.exists(file):
        #     print("Fisierul dorit nu exista.")
        # if os.path.isdir(file):
        #     print("Path-ul introdus corespunde unui director. Introduceti path-ul unui fisier.")
        # if not os.path.isfile:
        #     pass
        # if os.path.getsize(file) == 0:
        #     print("File is empty!") 
        data = open(file, 'rt', encoding="utf-8")
        k = 0
        t = 0
        newfile = os.path.splitext(file)[0] + '_1' + os.path.splitext(file)[1]
        c = 1
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
                if(ord(char)+ord(pw[t%len(pw)])) > 255:
                    lastbits += str(t)
                    lastbits += bin(ord(char)+ord(pw[t%len(pw)]))[-1]
                    lastbits += ','
                t += 1
            
            lastbits = lastbits[:-1]
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
            print(traceback.format_exc())
    except FileNotFoundError:
        print('Fisierul nu a fost gasit. Introduceti date valide.')
        print(traceback.format_exc())
    except:
        print('except general 1')
        print(traceback.format_exc())


def decrypt(file,pw):
    try:
        # if not os.path.isfile(file):
        #     print('fisierul nu exista.')
        # if os.path.splitext(file)[1] != '.crypted':
        #     print('fisierul are formatul gresit (nu e .crypted la final)')
        # elif os.path.splitext(os.path.splitext(file)[0])[1] != '.txt':
        #     print('fisierul are formatul gresit (nu e .txt.crypted)')
        newfile = os.path.splitext(os.path.splitext(file)[0])[0] + '_1' + os.path.splitext(os.path.splitext(file)[0])[1]
        goodfile = os.path.splitext(file)[0]
        
        c = 1
        while os.path.isfile(newfile):
            c += 1
            newfile = os.path.splitext(os.path.splitext(file)[0])[0] + '_' + str(c) + os.path.splitext(os.path.splitext(file)[0])[1]
        os.rename(file, newfile)
        while os.path.isfile(goodfile):
            c += 1
            goodfile = os.path.splitext(os.path.splitext(file)[0])[0] + '_' + str(c) + os.path.splitext(os.path.splitext(file)[0])[1]
        
        data = open(newfile, 'rt', encoding="utf-8")
        k = 0
        try:
            crypted = open(goodfile, 'w+', encoding="utf-8")
            
            oghash = data.readline().strip()
            lastbits = data.readline().strip()
            
            newlastbits = lastbits.split(',')
            newlastbits = {int(lb[:-1]): int(lb[-1]) for lb in lastbits.split(',')}
            
            while(1):
                char = data.read(1)
                if not char:
                    break
                if k in newlastbits:
                    newnumber = ord(char) * 2 + newlastbits[k] - ord(pw[k%len(pw)])
                    newchar = chr(newnumber)
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
    crypt(os.path.join(os.getcwd(), "plaintext.txt"), "ÈÉÊË")
    decrypt(os.path.join(os.getcwd(), "plaintext.txt.crypted"),"ÈÉÊË")