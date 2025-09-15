import random
import string

length = int(input("How many characters do you want in your password? "))


letters = string.ascii_letters  
numbers = string.digits         
symbols = string.punctuation    


all_chars = letters + numbers + symbols


password = ""
for i in range(length):
    password += random.choice(all_chars)


print("Here is your password:", password)
