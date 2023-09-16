'''
Created on Nov 29, 2022

@author: Hamza
'''
import hashlib
import binascii
import time
import itertools
import matplotlib.pyplot as plt
import random
from matplotlib import rcParams

def read_dictionary(file_name):
    dict_array = []
    dict_file = open(file_name)
    
    for line in dict_file:
        dict_array.append(line.rstrip('\n')) # rstrip('\n') removes newline characters 
    
        
    return dict_array

def hash_pass_256(word):
    hash256 = hashlib.pbkdf2_hmac('sha256', word.encode(), 'saltPhrase'.encode(), 100000)
    hashed = binascii.hexlify(hash256)
    return hashed

def hash_pass_512(word):
    hash512 = hashlib.pbkdf2_hmac('sha512', word.encode('utf-8'),'saltPhrase'.encode('utf-8'), 100000)
    hashed = binascii.hexlify(hash512)
    return hashed
        
def take_input():
    file = input("Enter name of .txt file (so if its named dict.txt entered dict.txt): ")
    dict_array = read_dictionary(file)
    
    #Empty dictionary to store times password and number of guesses
    guesses_data = {}
    sha256_time = {}
    sha512_time = {}
    
    # Ask for if user wants to encrypt in SHA256 hash or SHA512 hash
    #take input
    while(True):
        hash_type = input("Enter 1 for SHA256 hash, Enter 2 for SHA512 hash, or q to exit: ")
        #Exit program if q is entered
        if hash_type == 'q':
            break
        #Start program
        while(True):
            try:
                hash_type = int(hash_type)
            except ValueError:
                print("Not an int try again")
                
            if (hash_type != 1 and hash_type != 2):
                break
            else:
                #Take password input
                password = input("Enter Password: ")
                
                print("Pwd is:" + password + " Length is: ", len(password))
                print("===========================================")
                print("Attemping to crack password.....")
                

                #Hash password to either SHA256 or SHA512 based on user input
                hashed = ''
                if (hash_type == 1):
                    hashed = hash_pass_256(password)
                    print("SHA256: " + hashed.decode())
                elif (hash_type == 2):
                    hashed = hash_pass_512(password)
                    print("SHA512: " + hashed.decode())
                #Begin the timer
                start = time.time()
                #Limit of combinations of words we are taking, keep as a variable so its not hardcoded
                all_combinations = []
                max_limit = 3
                for x in range(1, max_limit+1):
                    for i in itertools.product(dict_array, repeat=x):
                        curr = ''.join(map(str, i))
                        if (len(curr) == len(password)):
                            all_combinations.append(curr)
                
                #Crack password for sha256 hash
                guesses = 0
                if (hash_type == 1):
                    for word in all_combinations:
                        guesses += 1
                        if hash_pass_256(word) == hashed:
                            total_time = time.time()-start
                            print("Guessed it " + word)
                            guesses_data[word] = guesses
                            sha256_time[word] = total_time
                            print(guesses_data)
                            print("Elapsed time: ",str(total_time) + " seconds.")
                            break
                #Crack password for sha512 hash
                elif (hash_type == 2):
                    for word in all_combinations:
                        guesses += 1
                        if hash_pass_512(word) == hashed:
                            total_time = time.time()-start
                            print("Guessed it " + word)
                            guesses_data[word] = guesses
                            sha512_time[word] = total_time
                            print(guesses_data)
                            print("Elapsed time: ",str((time.time()-start)) + " seconds.")
                            break
                print("===========================================")
                break
    #Display data in graphs
    print("Guesses data ", guesses_data)
    print("SHA256 ", sha256_time)
    print("SHA512 ", sha512_time)
    #===========================================================================================================
    # Plot the data for the number of guesses and length of words
    color=['red','orange','yellow','green','blue','purple', 'pink', 'black', 'brown']
    used_colors = []
    for item in guesses_data.keys():
        while(True):
            curr_color = color[random.randint(0, len(color) -1)]
            if (len(used_colors) == len(color)):
                used_colors = []
            if (used_colors.count(curr_color) == 0):
                used_colors.append(object)
                plt.scatter(len(item), guesses_data[item], s=100 , c=curr_color, label= "{'" + str(item) + "' : " + str(guesses_data[item]) + "}")
                break
    plt.xlabel('Password Difficulty')
    plt.ylabel('Number of Guesses')
    plt.title("Password Difficulty vs. Number of Guesses \n Dictionary Size: " + str(len(dict_array)))
    plt.legend()
    plt.show()
    used_colors = []
    #===========================================================================================================
    #Plot the data for the SHA256 data
    for item in sha256_time.keys():
        while(True):
            curr_color = color[random.randint(0, len(color) -1)]
            if (len(used_colors) == len(color)):
                used_colors = []
            if (used_colors.count(curr_color) == 0):
                used_colors.append(object)
                plt.scatter(len(item), sha256_time[item], s=100 , c=curr_color, label= "{'" + str(item) + "' : " + str(sha256_time[item]) + "}")
                break
    plt.xlabel('Password Difficulty')
    plt.ylabel('Time to crack SHA256 (seconds)')
    plt.title("Password Difficulty vs. Time Taken To Crack SHA256 \n Dictionary Size: " + str(len(dict_array)))
    plt.legend()
    plt.show()
    used_colors = []
    #===========================================================================================================
    #Plot the data for the SHA256 data
    for item in sha512_time.keys():
        while(True):
            curr_color = color[random.randint(0, len(color) -1)]
            if (len(used_colors) == len(color)):
                used_colors = []
            if (used_colors.count(curr_color) == 0):
                used_colors.append(object)
                plt.scatter(len(item), sha512_time[item], s=100 , c=curr_color, label= "{'" + str(item) + "' : " + str(sha512_time[item]) + "}")
                break
    plt.xlabel('Password Difficulty')
    plt.ylabel('Time to crack SHA512 (seconds)')
    plt.title("Password Difficulty vs. Time Taken To Crack SHA512 \n Dictionary Size: " + str(len(dict_array)))
    plt.legend()
    plt.show()
    used_colors = []
take_input()