
import sys
import os
import hashlib


def hash(filePath,fileSize):
    try:
        m = hashlib.sha1()
        f = open(filePath,"rb")
        while True:
            data = f.read(fileSize)
            if len(data)==0: 
                break
            m.update(data)
        f.close()
        return m.hexdigest()
    except:
        return ""


def crypt(file,pw):
    try: 
        if not os.path.isfile(file):
            raise Exception("Path-ul introdus nu corespunde unui fisier. Introduceti path-ul unui fisier.")
        if os.path.getsize(file) == 0:
            raise Exception("Fisierul introdus este gol. Introduceti date valide.")
        
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
            lastbits = ""
            while(1):
                char = data.read(1)
                if not char:
                    break
                if(ord(char)+ord(pw[t%len(pw)])) > 255:
                    lastbits += bin(ord(char)+ord(pw[t%len(pw)]))[-1]
                else:
                    lastbits += '2'
                t += 1
                
            m = hash(file,t)
            crypted.write(m)
            crypted.write('\n')
            
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
            print('Criptare realizata cu succes.')
            print('Locatie fisier criptat:', cryptedfile)
        except:
            print('Au aparut probleme in timpul procesului de criptare. Introduceti date valide.')
    except Exception as e:
        print(e)
    except:
        print('Au aparut probleme in timpul procesului de criptare. Introduceti date valide.')


def decrypt(file,pw):
    try:
        if not os.path.isfile(file):
            raise Exception("Path-ul introdus nu corespunde unui fisier. Introduceti path-ul unui fisier.")
        if os.path.splitext(file)[1] != '.crypted':
            raise Exception('Fisierul nu are formatul corespunzator unui fisier criptat(".txt.crypted"). Introduceti date valide.')
        elif os.path.splitext(os.path.splitext(file)[0])[1] != '.txt':
            raise Exception('Fisierul nu are formatul corespunzator unui fisier criptat(".txt.crypted"). Introduceti date valide.')
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
            
            for count, line in enumerate(data):
                pass
            if(count+1 < 3):
                raise Exception("Fisierul criptat contine date invalide. Introduceti date valide.")
            
            data.seek(0)
            oghash = data.readline().strip()
            lastbits = data.readline().strip()
            x = ''
            if any(x not in set("012") for x in lastbits):
                raise Exception("Fisierul criptat contine date invalide. Introduceti date valide.")
            
            while(1):
                char = data.read(1)
                if not char:
                    break
                if(int(lastbits[k]) != 2):
                    newnumber = ord(char) * 2 + int(lastbits[k]) - ord(pw[k%len(pw)])
                    newchar = chr(newnumber)
                else:
                    newchar = chr(ord(char) - ord(pw[k%len(pw)]))
                crypted.write(newchar)
                k += 1
            data.close()
            os.remove(newfile)
            crypted.close()
            
            newhash = hash(goodfile,k)
            if(newhash == oghash):
                print('Decriptare realizata cu succes.')
                print('Locatie fisier decriptat:', goodfile)
            else:
                print('Decriptare esuata. Introduceti date valide.')
        except Exception as e:
            print(e)
        except:
            print('A aparut o problema in timpul decriptarii. Introduceti date valide.')
    except Exception as e:
        print(e)
    except:
        print('A aparut o problema in timpul decriptarii. Introduceti date valide.')


def execinput():
    # INPUT: FileCryptor.py crypt abc.exe my_pass ⇒ va crea fisierul abc.exe.crypted
    # INPUT: FileCryptor.py decrypt abc.exe.crypted my_pass ⇒ va crea fișierul abc.exe
    if (len(sys.argv) - 1) < 3:
        print('Sintaxa incorecta1. Utilizati formatul:\n')
        print('FileCryptor.py [crypt/decrypt] path_fisier parola_criptare')
    else:
        if(sys.argv[1].lower() == 'crypt'):
            crypt(sys.argv[2], sys.argv[3])
        elif(sys.argv[1].lower() == 'decrypt'):
            decrypt(sys.argv[2], sys.argv[3])
        else: 
            print('Sintaxa incorecta. Utilizati formatul:\n')
            print('FileCryptor.py [crypt/decrypt] [path_fisier] [parola_criptare]')


if __name__ == "__main__":
    execinput()