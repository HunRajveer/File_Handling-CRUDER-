
# project on CRUD operation
# we cannot remove a file it can only be remove my os so import os
import os 

from pathlib import Path
def readfile():
    # Path is used to copy the path
    p = Path("")
    # .rglob will collect all file form folder and store it in form of list so we can iterate it using loop ("*") will collect all file which present in folder
    items = list(p.rglob("*"))
    for i , file in enumerate(items):
        print(f"{i+1}-{file}")
def read():
    # readfile function will fatch and disply file form path  
    readfile()
    # enter the file name
    file_name = input("enter the file name")
    p = Path(file_name) 
    if p.exists():
        with open(file_name,"r") as file:
            print(file.read())
    else:
        print("file does not found")
def update ():
    try:
        readfile()
        file_name = input("Enter the file name: ")
        p = Path(file_name)
        if p.exists():
            #  we use with bcs we dont need to colse it 
            with open(file_name, "r") as file:
                print("Current content:\n", file.read())
            
            choice = input("Press 1 to Overwrite | Press 2 to Append: ")
            mode = "w" if choice == "1" else "a"
            
            content = input("Enter the new content: ")
            with open(file_name, mode) as file:
                file.write("\n" + content)
            print("File updated successfully!")
        else:
            print("File does not exist") 
    except Exception as e:
        print(e) 
def delete():
    try:
        readfile()
        file_name = input("Enter the file name: ")
        p = Path(file_name)
        if p.exists():
            os.remove(p)
            print("file deleted sucessfully")
        else:
            print("file does not exist ")  
    except Exception  as e:
        print(e)          
def rename():
    try:
        readfile()
        file_name = input("Enter the file name: ")
        p = Path(file_name)
        if p.exists():
            new_file = input("enter the new file name")
            p.rename(new_file)
            print("file is rename sucessfully")
        else:
            print("file does not exist")
    except Exception as e:
        print(e)





        
def create ():
    try:
        readfile()
        file_name = input("enter the file name")
        # path will check if exists 
        p = Path(file_name)
        if p.exists():
            print("File already exists")
        else:
            with open(file_name,"w") as file:
                content = input("enter your file content")
                file.write((content))
                print("File Added")
    except Exception as e:
        print(e) 
def create_folder():
    try:
        readfile()
        folder_name = input("Enter the folder name: ")
        p = Path(folder_name)
        if p.exists():
            print("Folder already exists")       
        else:
            p.mkdir()                             
            print("Folder created successfully")
    except Exception as e:
        print(e)  

def remove_folder():
    try:
        readfile()
        folder_name = input("enter the folder name")
        p = Path(folder_name)
        if p.exists():
            p.rmdir()
            print("folder removed sucessfully")
        else:
            print("folder does not exist")
    except Exception as e:
        print(e)   
def create_file_in_folder ():
    try:
        folder_name = input("enter the folder name")
        file_name = input("enter the file name")
        p = Path(folder_name/file_name)
        if p.exists():
            print("File already exists")
        else:
            with(open("file name","w")) as file:
                content = input("enter the content")
                file.write(content)
                print("file created successfully")
    except Exception as r:
        print(r)            










print("press 1 to create a file")
print("press 2 to read a file")
print("press 3 to update a file")
print("press 4 to delete a file")
print("press 5 to rename a file")
print("press 6 to create a folder")
print("press 7 to remove a folder")
print("press 8 to create_file_in_folder")

option = int(input("enter the choice"))
if option==1:
    create()
elif option ==2:
    read()
elif option ==3:
    update()    
elif option==4:
    delete()
elif option==5:
    rename()
elif option==6:
    create_folder()
elif option==7:
    remove_folder()  
elif option==8:
    create_file_in_folder ()               

