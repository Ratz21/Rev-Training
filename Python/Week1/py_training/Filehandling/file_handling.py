""" OS MODULE AND FILE HANDLING"""


import os

print(os.getcwd()) #prints current working directory

os.chdir("C:/users/Desktop") # changes the current working directory

print(os.listdir("D:\Revature-Training\Python\Week1"))  # List all the directories

os.mkdir("test.py") # creating and removing a directory
os.rmdir("test.py")

os.path.join("folder", "File.txt") # joins paths

os.system("cls")  # clears terminal

# how to give acces to environment variables like PATH USER etc

print(os.environ['PATH'])

os.path.exists('D:\Revature-Training\Python\Week1')

# tells if the path exists or not


