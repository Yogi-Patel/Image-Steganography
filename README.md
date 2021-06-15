# Description 
Command-line Image Steganography program that allows you to hide text as well as images inside of other images. 
The Least Significant Bit replacement algorithm is used to carry out the image steganography 


## Uses
The program provides different ways(methods) through which you can hide/extract information(images or text) inside images and they are as follows: 

### 1) Simple Embed 
**usage:** `python ist.py -E <name of cover image w/ extension> <text file containing the message> <name of steg object w/ extension>`

**Description:** This simply hides the message inside the cover image and saves the resultant image as the name provided. No text-encryption is done on the message

### 2) Simple Extract 
**usage:** `python ist.py -D <name of steg object w/ extension> [--savetofile]`

**Description:** This allows you to extract the message that is embedded inside the steg object (the image containing the text message). `--savetofile` is optional. It saves the extracted message into a .txt file. It is helpful when you have to extract a long message and displaying it in the command prompt is not ideal. 

### 3) Embed with Twofish Encryption
**usage:** `python ist.py -ET <name of cover image w/ extension> <text file containing the message> <name of steg object w/ extension>`

**Description:** This hides the message inside the cover image and saves the result as the name provided. Before embedding the message inside the image, the message is encrypted with the Twofish algorithm. The key that is required to decrypt it is stored into a file named Key.txt. This method of encrypting generates a random key of it's own. If you require providing a Key of your own, use method 5 (Embed Using Twofish with Key of your own).

### 4) Extract Twofish Encrypted Message 
**usage:** `python ist.py -DT <name of steg object w/ extension> key[.txt]  [--savetofile]`

**Description:** This method allows the user to extract the message and decrypt it. While providing the key, the key can either be written by the user or stored in a file and the name of the file (alongwith the extension) can be passed into the program. `--savetofile` option is same as the one mentioned in method 2 (Simple Extract) above. 

### 5) Embed Using Twofish With Key of Your Own
**usage:** `python ist.py -ETK <name of cover image w/ extension> <text file containing the message> <name of steg object w/ extension> <Key>`

**Description:** This works the same way as method 3 (Embed with Twofish Encryption) but this method allows the user to provide their own Key that is used for encrypting the message. The length of the key should be (0,32] i.e., the length of the key should be greater than 0 and should not exceed 32 

### 6) Embed an Image Inside Another Image 
**usage:** `python ist.py -IE <name of steg object w/ extension> <image you want to hide w/ extension> <mode (1,2 or 4)> `

**Description:** This method allows the user to hide an Image inside another image. The user is not allowed to choose their own cover image because the cover image should have a resolution that perfectly fits the image they want to hide. While entering the mode, the user has to enter 1, 2 or 4. This tells the program how many least significant bits to replace. For example, using 4 as the mode will replace the 4 least significant bits of the cover image with the image you want to hide. 

Note: Using a higher mode will have more impact on the image quality of the cover image than using a lower mode value

### 7) Extract Image Hidden in Another Image 
**usage:** `python ist.py -ID <name of steg object w/ extension> <save extracted image as> <mode (1,2 or 4)>`

**Description:** This method allows the user to extract the image that is hidden inside the cover image. The user needs to know the mode value that was used while hiding the image inside the cover image. Using the wrong mode value will end up in a failure. The extracted image is stored as the name provided by the user themselves




#### NOTE: 
This command-line program is not fool-proof. 
This program was made with modularity in mind. So, if you need to make changes to the interface (i.e., the command-line), you can easily do so. 
You just need to know the working of the individual modules and you need to call them in the right order to carry out the image-steganography. 
