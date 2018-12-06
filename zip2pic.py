import time
import hashlib
import os
import text_to_image
import progressbar
import zipfile
import binascii
from PIL import Image

def file_to_hex_string(file_path):
    with open (file_path, 'rb') as f:
        content = f.read()
    hex_content = binascii.hexlify(content)
    hex_content = hex_content.decode("utf-8")
    return hex_content

def write_image_from_hex(hex_content, out_path): # out path including .png
    text_to_image.encode(hex_content, 'images/' + out_path)

def decode_image_to_hex(path): # Returns the string of the hex with a file
#    print("Decoding ", path)
    return text_to_image.decode('images/' + path) 
def write_hex_to_text_file(hex_content):
    with open("temporary-hex-output.txt", "a") as myfile:
        myfile.write(hex_content)
def prepare_env():
    # Create image dir if nessesary
    if not os.path.exists("images"):
        os.mkdir("images")
    # Remove files in images dir
    files = os.listdir('images')
    if len(files) > 0:
        print("cleaning up old images")
        for f in files:
            os.remove("images/" + str(f))
    # Create temp hex file if it doesn't exist
    if not os.path.exists("temporary-hex-output.txt"):
        print("creating new temp hex file")
        open('temporary-hex-output.txt', 'a').close()
    else:
        print("removing old hex file and creating new one")
        os.remove('temporary-hex-output.txt')
        open('temporary-hex-output.txt', 'a').close()
    # Remove the previous final.zip
    if os.path.exists("final.zip"):
        print('removing old final.zip')
        os.remove('final.zip')
def cleanup():
    print('cleaning up files')
    files = os.listdir('images')
    for f in files:
        if not f.endswith('.png'): # Remove any files created by the OS
            os.remove("images/" + str(f))
    os.remove('temporary-hex-output.txt')
def convert_from_pictures(img_dir):
    print('converting from pictures')
    files = os.listdir(img_dir)
    file_as_int = []
    for f in files:
        if f.endswith('.png'):
            file_as_int.append(int(f[:-4])) 
    file_as_int = sorted(file_as_int)
    sorted_files = []
    for f in file_as_int:
        sorted_files.append(str(f) + '.png')
    bar = progressbar.ProgressBar() # Setup bar
    for filename in bar(sorted_files):
        if filename.endswith(".png"):
            hex_cont = decode_image_to_hex(filename)
            write_hex_to_text_file(hex_cont)
    with open('temporary-hex-output.txt') as f, open('final.zip', 'wb') as fout:
        for line in f:
            fout.write(
                binascii.unhexlify(''.join(line.split()))
            )

def convert_to_pictures(path_of_file, increment_val): # Increment value is the size that will be in one picutre. Larger the number, the less pictures but each picture has a larger file size.
    print("converting to pictures")
    all_hex_content = file_to_hex_string(path_of_file)
    total_chars = len(all_hex_content)
    image_count = 0
    n = increment_val # Just to make the next line shorter
    split_hex_content = [all_hex_content[i:i + n] for i in range(0, len(all_hex_content), n)] # Converts it into a set of n length elements, leaving the last one
    bar = progressbar.ProgressBar() # Setup progress bar
    for hex_content in bar(split_hex_content):
        write_image_from_hex(hex_content, str(image_count) + '.png')
        image_count += 1
def get_sha(path):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha256 = hashlib.sha256()
    sha_match = False
    with open('Archive.zip', 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    sha_init = sha256.hexdigest()
    return sha256.hexdigest()

def main():
    prepare_env()
    # First lets check the SHA 256 of the intial file
    sha_init = get_sha('Archive.zip')
    print("SHA Initial", sha_init)

    convert_to_pictures('Archive.zip', 10000) # Actually convert
    convert_from_pictures('images')

    sha_fin = get_sha('final.zip')
    print("SHA Final", sha_fin)

    sha_match = sha_init == sha_fin
    print("SHA Initial = final? ", sha_match)
    cleanup()
main()
