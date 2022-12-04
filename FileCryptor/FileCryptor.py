
import os


def crypt(file,pw):
    data = open(file, 'rt', encoding="utf-8")
    k = 0
    newfile = os.path.splitext(file)[0] + '_2' + os.path.splitext(file)[1]
    crypted = open(newfile, 'a+', encoding="utf-8")
    while(1):
        char = data.read(1)
        if not char:
            data.close()
            break
        crypted.write(chr(ord(char) + ord(pw[k%len(pw)])))
        newchar = chr(ord(char))
        k += 1
    crypted.close()
    os.rename(newfile, file + '.crypted')


def decrypt(file,pw):
    newfile = os.path.splitext(os.path.splitext(file)[0])[0] + '_2' + os.path.splitext(os.path.splitext(file)[0])[1]
    goodfile = os.path.splitext(file)[0] 
    os.rename(file, newfile)
    data = open(newfile, 'rt', encoding="utf-8")
    k = 0
    crypted = open(goodfile, 'a+', encoding="utf-8")
    while(1):
        char = data.read(1)
        if not char:
            data.close()
            break
        newchar = chr(ord(char) - ord(pw[k%len(pw)]))
        crypted.write(newchar)
        k += 1
    data.close()
    os.remove(newfile)
    crypted.close()


if __name__ == "__main__":
    crypt(os.path.join(os.getcwd(), "plaintext.txt"), "ABCD")
    decrypt(os.path.join(os.getcwd(), "plaintext.txt.crypted"),"ABCD")