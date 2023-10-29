from git import Repo
import requests
from pathlib import Path
import inquirer

from settings import *


# clone function
def clone(url, path):
    try:
        repo_name = url.split('/')[4][:-4]
        path = get_path(path)

        Repo.clone_from(url, to_path=path)
        return True
    
    except Exception as e:
        print(f'Failed to clone {repo_name}. Error: {e}\n Make sure the repository URL is valid.')
        return False


def create_repo(user, token, repo_name, desc, path=Path.cwd()):
    try:
        url = f"https://api.github.com/users/{user}"

        headers = {
            "Authorization" : f"token {token}"
        }
        data = {
            "name" : repo_name,
            "description" : desc,
            "auto-init" : True
        }

        #local repo init
        Repo.init(path)

       


        response = requests.get(url, headers=headers)
        response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)
        #print(response.text)
        print(response.status_code)

        return True

    except Exception as e:
        return False




    

# main menu for a hint of UI
def menu():
    print('''
    1: Clone a repository
    2: Upload a repository
    0: gtfo
Please enter your choice: ''')
    choice = int(input())
    if choice in range(0,3):
        return choice


# MAIN
#if __name__ == '__main__':
    
    print("*** Basic Git Repos Command Line Interperter ***")

    while(True):
        c = menu()

        if c == 0:
            break
        
        elif c == 1:
            url = input("Enter the git repo URL you wish to clone:\n")
            base_dir = input("\nEnter the folder path to save in (optional):\n")

            if (clone(url, base_dir)):
                print("Successfully cloned!\n")
            else:
                print("Cloning failed. You may try again.\n")
        
        elif c == 2:
            while user == "":
                print("Enter your GitHub username and token to initilize...")
                user = input("User: ")
                while not user_exists(user):
                    print(f"Couldn't find a user by the name of {user}. Please try again.")
                    user = input("User: ")
                token = input("Token: ")
                path = input("Enter the folder path to your project: ")
                repo_name = input("Name of the repository (optional): ")
                desc = input("Description of the repository (optional): ")
                if not create_repo(user, token, repo_name, desc, path):
                    print("Something went wrong...")
                else:
                    print(f"The repository {repo_name} was created successfully!")



