from git import Repo
import requests
from pathlib import Path
import time


def get_path(path=Path.cwd()):
    return path

# clone function
def clone(url, path):
    try:
        repo_name = url.split('/')[4][:-4]
        path = get_path(path)+repo_name

        Repo.clone_from(url, to_path=path)
        return True
    
    except Exception as e:
        print(f'Failed to clone {repo_name}. Error: {e}\nMake sure the repository URL is valid.')
        return False
    


def create_new_repo(token, repo_name, desc, path=Path.cwd()):
    try:
        if not repo_name:
            repo_name = str(path).split('\\')[-1]
            #local repo init
            repo = Repo.init(get_path(path))
        else:
            #local repo init
            repo = Repo.init(get_path(path)+f"\\{repo_name}")

        

        headers = {
            "Authorization" : f"token {token}"
        }
        data = {
            "name" : repo_name,
            "description" : desc,
            "auto-init" : True
        }

        response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)
        #print(response.status_code)
        if not response.status_code == 201:
            assert f"POST has not returned 201. Status: {response.status_code}"
        
        #repo_name = str(path).split('\\')[-1] #TEMP
        '''new_branch_name = 'test-branch' 
        new_branch = repo.create_head(new_branch_name)
        new_branch.checkout()'''
        repo.active_branch.create()
        repo.active_branch.checkout()
        #repo = Repo.init(get_path(path))

        user = "Efrat-w" #TEMP
        #remote = repo.create_remote(repo_name, url=f"https://github.com/{user}/{repo_name}")

        for file in Path(path).iterdir():
            repo.git.add(file)
        
        a = repo.is_dirty()
        
        
        message = "commit message"
        try:
            repo.git.commit('-m', message) # same as git commit -m "commit message"
        except:
            print("Nothing to commit.")
            return True
        
        try:
            repo.git.remote("set-url", "origin", f"https://github.com/{user}/{repo_name}")
        except:
            # If the remote repository does not exist, add a new one
            repo.git.remote("add", "origin", f"https://github.com/{user}/{repo_name}")

        repo.git.remote("add", "origin", f"https://github.com/{user}/{repo_name}")
        a = repo.git.status()
        repo.remote("origin").push('+refs/heads/*:refs/remotes/origin/*')
        a = repo.git.status()
        
        return True

    except Exception as e:
        print(f'Failed to create {repo_name}. Error: {e}\n')
        return False