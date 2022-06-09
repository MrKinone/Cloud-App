from Crypto.Cipher import AES
import steganography as stg
import string
import random
import csv

def encrypt_file(in_filename):
    key = stg.stg_decoding().encode("utf8")

    letters = string.ascii_lowercase
    IV = ''.join(random.choice(letters) for i in range(16))
    out_filename = IV
    # IV = get_random_bytes(16)
    IV = bytes(IV, 'utf-8')
    outfile_dir= in_filename.rsplit("/", 1)[0]+"/"+out_filename
    encryptor = AES.new(key, AES.MODE_CBC, IV=IV)

    csv_name = []
    csv_name.append(out_filename)
    with open(in_filename, 'rb') as infile:
        with open(outfile_dir, 'wb') as outfile:
            name = in_filename.rsplit("/", 1)[-1]+"/"
            csv_name.append(name[:-1])
            outfile.write(name.encode("utf8"))
            while True:
                chunk = infile.read(16)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    empty = ' ' * (16 - len(chunk) % 16)
                    chunk = chunk + bytes(empty, 'utf-8')
                outfile.write(encryptor.encrypt(chunk))

    with open('name.csv', 'a') as writeFile:
        writeFile.write(csv_name[0]+","+csv_name[1]+"\n")

    return outfile_dir


if __name__ == '__main__':
    outfile = encrypt_file("C:/Users/oktay/Desktop/Screenshot_1.jpg")
