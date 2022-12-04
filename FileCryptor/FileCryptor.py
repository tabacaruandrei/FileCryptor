
import os
import hashlib


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
            crypted.write('\n\n')
            lastbits = []
            while(1):
                char = data.read(1)
                if not char:
                    data.close()
                    break
                if(ord(char) + ord(pw[k%len(pw)])) > 255:
                    newnumber = int(bin(ord(char)+ord(pw[k%len(pw)]))[2:10],2)
                    lastbits.append(bin(ord(char)+ord(pw[k%len(pw)]))[10])
                    newchar = chr(newnumber)
                else:
                    newchar = chr(ord(char) + ord(pw[k%len(pw)]))
                crypted.write(newchar)
                k += 1
            crypted.seek(0)
            lines = crypted.readlines()
            if(len(lastbits) != 0):
                for i in lastbits:
                    crypted.write(i)
                crypted.write('\n')
            crypted.close()
            cryptedfile = file + '.crypted'
            d = 1
            while os.path.isfile(cryptedfile):
                d += 1
                cryptedfile = os.path.splitext(file)[0] + str(d) + os.path.splitext(file)[1] + '.crypted'
            os.rename(newfile, cryptedfile)
        except FileExistsError:
            print('file exists error')
        except:
            print('except general 2')
    except FileNotFoundError:
        print('file not found error')
    except:
        print('except general 1')


def decrypt(file,pw):
    newfile = os.path.splitext(os.path.splitext(file)[0])[0] + '_2' + os.path.splitext(os.path.splitext(file)[0])[1]
    goodfile = os.path.splitext(file)[0]
    try:
        os.rename(file, newfile)
    except:
        pass
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


if __name__ == "__main__":
    crypt(os.path.join(os.getcwd(), "plaintext.txt"), "ABCD")
    decrypt(os.path.join(os.getcwd(), "plaintext.txt.crypted"),"ABCD")