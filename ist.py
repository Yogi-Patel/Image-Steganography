import sys 
from skimage import io
import cv2
import numpy 
from numpy import asarray 
import random 
from twofish import Twofish
import re
from PIL import Image
from datetime import date
from datetime import datetime
from os import path 
from pathlib import Path

def size_finder(len_message): 
    # Returns a size width, height 
    # Returns a list

    max_bits = len_message * 8 
    width = random.randrange(1280, 1920, 1)
    height = random.randrange(720, 1080, 1)
    while(True):
         if(max_bits > width*height*3):
             width = random.randrange(width, 2*width, 1)
             height = random.randrange(height, 2*height , 1)
             continue 
         else: 
             break 

    liz = [width, height]
    return liz
    

def key_gen(): 
    key_supply = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz"
    key = ""

    for i in range(0,32):
        key += key_supply[random.randint(0, len(key_supply)-1)]

    return key 

def encrypt_twofish(message, key = ""): 
    # Encrypts the text using twofish 
    # Returns the binary of the encrypted text
    # Do not convert message to binary

    
    bin_encrypted = ""
    if (len(key) == 0):
        key = key_gen()

    chunks = [message[i:i+16] for i in range(0, len(message), 16)]

    T = Twofish(key.encode('UTF-8'))
    for i in chunks: 
        if (len(i) != 16):
            i += " "*(16-len(i))

        x = T.encrypt(i.encode('UTF-8'))
        bin_encrypted += "".join('{:08b}'.format(b) for b in x)

    chunks = [bin_encrypted[i:i+8] for i in range(0, len(bin_encrypted), 8)]
    encrypted = ""
     
    for i in chunks:
        encrypted += binary_to_text(i)
        
    return {"encrypted": encrypted, "key": key}

def decrypt_twofish(message, key):
    # decrypts the encrypted text 
    # Returns the decrypted text
    decrypted = ""
    encrypted = text_to_binary(message)
    chunks = [encrypted[i:i+128] for i in range(0, len(encrypted), 128)]

    #key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$"
    
    T = Twofish(key.encode('UTF-8'))
    for i in chunks:
        temp = int(i, 2).to_bytes(len(i) // 8, byteorder='big')
        decrypted += T.decrypt(temp).decode()

    return decrypted

def possibility_check(message, image):
    # Check if the image can be used to encrypt 
    total_bits = len(message) * 8 + (7 * 8)
    
    img = cv2.imread(image)
    

    max_bits = img.shape[0] * img.shape[1] * 3
    if (total_bits < max_bits): 
        return True 
    else:
        return False 

def D_list(a,b,c):
    # Creates and returns an n-dimension array 
    # c is the rows > b is the columns > a is the dimension 
    iz=[[["0"]*a]*b]*c
    return iz

def character_to_binary(character):
    # Converts a single character to binary 
    # Returns a String 
    deci = ord(character)
    binary =  bin(deci).replace("0b", "")
    additional_zeros = 8 - len(binary)
    return ("0"*additional_zeros + binary)

def text_to_binary(text): 
    # Convert text message to binary 
    # Returns a String. Done to make sure each character is converted to 8 bits and not less 
    binary = ""
    for i in text: 
        temp = character_to_binary(i)
        binary = binary + temp

    return binary

def binary_to_text(binary):
    # Converts binary to text 
    # Retruns a String character 
    temp = binary_to_decimal(binary)
    character = chr(temp)
    return character

def image_to_binary(image):
    # Converts the pixel  values of image sent to into binary values
    # Returns an array of Strings 
    
    img = cv2.imread(image)	
     

    numpy_array = asarray(img) 
    shape = numpy_array.shape	
    bin_array = D_list(shape[2], shape[1], shape[0])

    for i in range(0,shape[0]):
        for j in range(0, shape[1]):
            for k in range(0, shape[2]):
                bin_array[i][j][k] = (decimal_to_binary(numpy_array[i][j][k]))
                bin_array = numpy.array(bin_array)

    return bin_array

def decimal_to_binary(number):
    # Converts a number to it's binary equivalent 
    # Returns a String 
    binary =  bin(number).replace("0b", "")
    additional_zeros = 8 - len(binary)
    return ("0"*additional_zeros + binary)

def binary_to_decimal(number):
    # Converts binary to Decimal 
    # Returns an int but requires binary to be in String when passed to it 
    decimal = int(number,2)
    return decimal

def check(message):
    # Check if message has the end of file message 
    try:
        message.rindex("#!EOF!#")
        return True 
    except: 
        return False

def embed(message, image, dest):
    # Embed message into the image and save it as dest 

    message = text_to_binary(message + "#!EOF!#")
    length = len(message)
    n = 0 

    image = cv2.imread(image)

    image = asarray(image)

    shape = image.shape

    flag = False
    for i in range(0,shape[0]):
        for j in range(0, shape[1]):
            for k in range(0, shape[2]):
                if(n >= length): 
                    flag = True
                    break
                temp = image[i][j][k]
                temp = decimal_to_binary(temp)
                temp = temp[:-1] + message[n]
                n += 1 
                temp = binary_to_decimal(temp)
                image[i][j][k] = temp 

            if(flag):
                break
        if(flag):
            break

    cv2.imwrite(dest, image)

def extract(image): 
    # Extract message from the image
    temp_8 = ""
    message = ""
    image = cv2.imread(image)
    shape = image.shape
    flag = False
    

    for i in range(0,shape[0]):
        for j in range(0, shape[1]):
            for k in range(0, shape[2]):
                temp = image[i][j][k]
                temp = decimal_to_binary(temp)
                
                temp_8 += temp[-1]

                if(len(temp_8) == 8):
                    message += binary_to_text(temp_8)
                    
                    temp_8 = ""
                    flag = check(message)

                if(flag):
                    message = message[:message.rindex("#!EOF!#")]
                    break
            if(flag):
                break
        if(flag):
            break 

    return message

def image_array_to_string(image):
    # Converts an image to a single line binary String 
    # Returns a String 

    String_image = ""
    image = cv2.imread(image)
    image = numpy.asarray(image).flatten()
    #print(image)

    for i in image: 
        String_image +=decimal_to_binary(i)
        #print(String_image)
    return String_image

def perfect_fit(mode):
    # Function used to find the width and height of the image that will contain the image 
    # that you want to hide 
    # Returns a dictionary 

    mode_options = [1, 2, 4]
    pix_rat = [8, 4, 2]
    try:
        pixel_ratio = pix_rat[mode_options.index(mode)]
    except: 
        print("Using default mode = 4")
        mode = 4 

    if mode == 1: 
        return {'width': 4, 'height': 2, 'mode': mode}
    elif mode == 2: 
        return {'width': 2, 'height': 2, 'mode': mode}
    else: 
        return {'width': 2, 'height': 1, 'mode': mode}

def random_image(liz, name):
    # Saves an image of size width*height as name 

    width = liz[0]
    height = liz[1]

    url = "https://placekitten.com/"+str(width)+"/"+str(height)

    image = io.imread(url)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    cv2.imwrite(name, image)

def embed_image(image, embedee, mode):
    # Saves the image into the cover image 
    # Does not return anything 

    image_name = image
    fit = perfect_fit(mode)
    mode = fit['mode']

    shape_e = numpy.asarray(cv2.imread(embedee)).shape
    random_image([shape_e[1]*fit['width'], shape_e[0]*fit['height']], image)

    image = cv2.imread(image)
    embedee = image_array_to_string(embedee)
    

    chunks = [embedee[i:i+mode] for i in range(0, len(embedee), mode)]
    shape = numpy.asarray(image).shape
    

    n = 0 
    for i in range(0,shape[0]):
        for j in range(0, shape[1]):
            for k in range(0, shape[2]):
                
                image[i][j][k] =binary_to_decimal(decimal_to_binary(image[i][j][k])[:-mode] + chunks[n])
                
                n += 1 


    cv2.imwrite(image_name, image)
    
def extract_image(image, dest, mode):
    # Function is used to remove the the image from the cover image 
    # Does not return anything 

    shape_e = numpy.asarray(cv2.imread(image)).shape
    image = cv2.imread(image)
    
    fit = perfect_fit(mode)

    width = int(shape_e[1] / fit['width'])
    height = int(shape_e[0] / fit['height'])

    String_image = ""

    for i in range(0,shape_e[0]):
        for j in range(0, shape_e[1]):
            for k in range(0, shape_e[2]):
                temp =decimal_to_binary(image[i][j][k])[-mode:]
                
                String_image += temp


    chunks = [String_image[i:i+8] for i in range(0, len(String_image), 8)]
    
    liz = numpy.zeros((height, width, 3))

    n = 0
    for i in range(0,height):
        for j in range(0, width):
            for k in range(0, 3):
                temp =binary_to_decimal(chunks[n])
                
                liz[i][j][k] = temp
                n += 1
                

    cv2.imwrite(dest, liz)


def help():
    print()
    print("__Simple Embed__")
    print("usage: -E image_name_with_ext  file_containing_message  save_steg_image_as \n")

    print("__Simple Extract__")
    print("usage: -D image_name_with_ext [--savetofile] ")
    print("NOTE: --savetofile option is optional and using it saves the extracted message to a file\n")
    
    print("__Embed with Twofish Ecryption__")
    print("usage: -ET image_name_with_ext  file_containing_message  save_steg_image_as")
    print("NOTE: This mode generates it's own key and saves it to file Key.txt")
    print("\tEach key is stored in the Key_backup.txt file \n")
    
    print("__Extract Twofish Encrypted Message__ ")
    print("usage: -DT image_name_with_ext key[.txt] [--savetofile]")
    print("NOTE: The Key an be stored in a file and the filename can be passed or the key can be typed directly")
    print("\tThe --savetofile option is optional and saves the extracted message to a file \n ")
    
    print("__Embed Using Twofish With Key of Your Own__ ")
    print("usage: -ETK image_name_with_ext  file_containing_message  save_steg_image_as  Key")
    print("NOTE: The key size should be between 0 and 32 \n")

    print("__Embed an Image Inside Another Image__")
    print("usage: -IE image_name_with_ext image_to_hide_with_ext  mode(1,2 or 4)")
    print("mode is necessary \n")

    print("__Extract Image Hidden in Another Image__")
    print("usage: -ID image_name_with_ext save_extracted_as_with_ext mode(1,2 or 4)")
    print("It is important to know what mode was used \n\n")

    print("ALL FILES SHOULD BE IN THE SAME LOCATION AS THE PROGRAM")
    print('MAKE SURE ALL FILE EXTENSIONS ARE PROVIDED CORRECTLY WITH THE FILENAME')
    print('MAKE SURE YOU ARE RUNNING THE PROGRAM ON THE CORRECT FILES')

def main():
    args = sys.argv[1:]

    mode = -1 
    mode_list = ['-E', '-D', '-ET', '-DT', '-ETK', '-h', '--help', '-IE', '-ID']
    if args[0] in mode_list:
        mode = mode_list.index(args[0])

    if mode == 0:
        image = args[1]
        f = open(args[2], 'r')
        message = f.read()
        dest = args[3]
        f.close()
        if possibility_check(message, image): 
            embed(message, image, dest)
        else: 
            print("Image cannot hold entire message. Use bigger image or smaller message")
    elif mode == 1: 
        image = args[1]
        message = extract(image)
        
        if args[-1] == "--savetofile":
            today = str(date.today())
            today = today.replace('-', "_")
            f = open("message"+today+".txt", "a")
            now = str(datetime.now())
            f.write("Time and date:" + now +"\n \nMessage: \n" + message +"\n\n")
            print("Message stored in .txt file")
            f.close()
        else: 
            print("EXTRACTED MESSAGE BELOW: \n \n ")
            print(message)
        
    elif mode == 2:
        image = args[1]
        f = open(args[2], 'r')
        message = f.read()
        dest = args[3]
        f.close()
        if possibility_check(message, image): 
            dict = encrypt_twofish(message)
            message = dict['encrypted']
            print("The generated key is (used to decode the message): ", dict['key'])
            print("Key is stored in Key.txt as well")
            f = open("Key.txt", "w")
            f1 = open("Key_backup.txt", 'a')
            f1.write(dict['key'] + "\n")
            f.write(dict['key'])
            f.close()
            f1.close()
            embed(message, image, dest)
        else: 
            print("Image cannot hold entire message. Use higher resolution image or smaller message")
    
    elif mode == 3: 
        image = args[1]
        key = ""
        if path.exists(args[2]):
            f = open(args[2], "r")
            key = f.read()
        else: 
            key = args[2]

        message = extract(image)
        message = decrypt_twofish(message, key)
        if args[-1] == "--savetofile":
            today = str(date.today())
            today = today.replace('-', "_")
            f = open("message"+today+".txt", "a")
            now = str(datetime.now())
            f.write("Time and date:" + now +"\n \nMessage: \n" + message + "\n\n")
            print("Message stored in .txt file")
            f.close()
        else: 
            print("EXTRACTED MESSAGE BELOW: \n \n ")
            print(message)
    elif mode == 4: 
        image = args[1]
        f = open(args[2], 'r')
        message = f.read()
        dest = args[3]
        key = args[4]
        f.close()
        if len(key) <= 32 and len(key) > 0:
            pass 
        else: 
            print("The key length is not in between 0 and 32")
            return 
        
        if possibility_check(message, image): 
            dict = encrypt_twofish(message, key)
            message = dict['encrypted']
            embed(message, image, dest)
        else: 
            print("Image cannot hold entire message. Use higher resolution image or smaller message")

    elif mode == 5 or mode == 6: 
        help()

    elif mode == 7: 
        image = args[1]
        embedee = args[2]
        embed_mode = int(args[3])
        embed_image(image,embedee,embed_mode)

        print("Image hidden inside another image and stored as: ", image)

    elif mode  == 8:
        image = args[1]
        dest = args[2]
        embed_mode = int(args[3])
        extract_image(image, dest, embed_mode)

        print("The image has been extracted and stored as: ", dest)
    else:
        print("Proper commands required")


if __name__ == '__main__':
    try:
        print()
        main()
        
    except:
        print("Exception occured. Please make sure you are using the program correctly")
        print("Refer to the following for help: \n ")
        help()
