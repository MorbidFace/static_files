import os
import shutil

def copy_files(from_path, to_path):
    if (os.path.exists(from_path)):
        print(f"Copying from {from_path} to {to_path}...")      
        print("----------------------------------------------")
        list_of_files = os.listdir(from_path) 
        for file in list_of_files:
            existing_file_path = os.path.join(from_path, file)
            new_file_path = os.path.join(to_path, file)
            if (os.path.isfile(existing_file_path)):
                shutil.copy(existing_file_path, new_file_path)
                print(f"Copying file from {existing_file_path} to {new_file_path}... DONE!")
            else:
                if (os.path.exists(new_file_path)):
                    shutil.rmtree(new_file_path)
                os.mkdir(new_file_path)
                print("----------------------------------------------")
                print(f"Directory {existing_file_path} exists:")  
                print(f"Creating directory {new_file_path}... DONE!")
                copy_files(existing_file_path, new_file_path)