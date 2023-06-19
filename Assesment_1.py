"""IN THIS ASSESMENT WE NEED TO MAKE A LOGIN WHERE PEOPLE CAN SIGN UP AND MAKE A RANDOM PASSWORD
WE SHOULD ALSO BE ABLE TO VIEW A LIST OF LOGINS"""

#Alex Mclachlan id-320377013 10/04/2023


import string
import random

print("\nWelcome\n")

user_choice = input("Select an option\n \n L) Log in\n C) Create an account\n V) View accounts\n Q) Quit \n \n Selection: ").lower()


#This code is the log in, it checks the accounts file and validates
if user_choice == "l":
    print("Lets log in...!")
    print("-"*40)
    print(" ")
    entered_username = input("Enter username: ")
    entered_password = input("Enter password: ")

    accounts_file_in = open("accounts.txt", "r")
    accounts_dictionary = {}

    for line in accounts_file_in:
        name, password = line.split(" ")

        accounts_dictionary[name] = password.rstrip()
    accounts_file_in.close()

    is_logged_in = False
    for name, password in accounts_dictionary.items():
        if entered_username == name and entered_password == password:
            is_logged_in = True
            break

    print("-" * 40)
    print(" ")
    if is_logged_in == True:
        print('Welcome.')
    else:
        print('Invalid login')
    quit()

#this code views accounts
if user_choice == "v":
    accounts_file_in = open("accounts.txt", "r")
    accounts_dictionary = {}

    for line in accounts_file_in:
        name, password = line.split(" ")

        accounts_dictionary[name] = password.rstrip()
    accounts_file_in.close()

    for name, password in accounts_dictionary.items():
        print(f"User Name: {name:20s} Password: {password}")
    quit()




#this code is for account creation

if user_choice == "c":
    print("Lets sign you up.")
    print("-" * 40)
    print(" ")
    file_out = open("accounts.txt","a")
    username = input("Please enter user name: ")

    file_out.write(username +" ")
    user_choice = input("Would you like to\n A) Create your own password\n B) Randomly generate a password \n \n Selection: ")

    if user_choice == "a":
        password = input("Please enter Password: " )

        file_out.write(password +"\n")
    elif user_choice == "b":
        print("Lets generate a password\n")
        characters = []
        for char in string.ascii_letters:
            characters.append(char)
        use_numbers = input("Would you like to include numbers? [y]/n: ")
        if use_numbers == "y" or "":
            for char in string.digits:
                characters.append(char)
        use_symbols = input("Would you like to use symbols? [y]/n: ")
        if use_symbols == "y" or "":
            for char in string.punctuation:
                characters.append(char)
        password_length = int(input("How many characters long would you like your password? ") or 10)
        password = ""
        for i in range(password_length):
            password += random.choice(characters)
        file_out.write(password + "\n")
        file_out.close()
    print("\nThank you for signing up.\n You can now log in with your password: " + password)
    quit()
     #that code is writing the username, creating a space, then the password and a new line


#this code quits the program
if user_choice == "q":
    from time import sleep
    print("Exiting program...")
    sleep(2)
else:
     print("Invalid choice.")

