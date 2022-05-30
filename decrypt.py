import os
from Crypto.Cipher import AES
import steganography as stg
import encrypt

def decrypt_file(in_filename, outfile_dir):
    IV = in_filename.rsplit("/", 1)[-1].encode("utf8")

    outfile_name = ""

    with open(in_filename, 'rb') as infile:
        while True:
            char = infile.read(1)
            if char != b'/':
                outfile_name += str(char)[2]
            else:
                break

        outfile_dir = outfile_dir+"/"+outfile_name

        key = stg.stg_decoding().encode("utf8")

        decryptor = AES.new(key, AES.MODE_CBC, IV=IV)

        with open(outfile_dir, 'wb') as outfile:
            while True:
                chunk = infile.read(16)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

if __name__ == '__main__':
    file = encrypt.encrypt_file_2("C:/Users/oktay/Desktop/label_copy.py", r"C:\Users\oktay\Desktop")
    decrypt_file(file, "C:/Users/oktay/Desktop/Slayt_goruntuler")