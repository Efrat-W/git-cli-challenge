from back import *
import inquirer

user = ""
token = ""

def clone_repo():
    '''questions = [
    inquirer.List('url_type', message="Please select an action you'd like to perform: ", choices=list(['HTTP', 'SSH'])),
]
    answers = inquirer.prompt(questions)
    url_type = answers['url_type']
    ###important: check if ssh works too###
    '''
    
    prompts = [
        inquirer.Text('url', message="Enter the git repo URL you wish to clone:"),
        inquirer.Text('base_dir', message="Enter the folder path to save in (optional):")
    ]

    answers = inquirer.prompt(prompts)
    url = answers['url']
    base_dir = answers['base_dir']

    if (clone(url, base_dir)):
        print("Successfully cloned!\n")
    else:
        print("Cloning failed. You may try again.\n")


def create_repo():
    #user, token = login()
    token = set_token()
    path = inquirer.prompt([inquirer.Text('path', message="Enter the folder path to your project:")])['path']
    repo_name = inquirer.prompt([inquirer.Text('repo_name', message="Name of the repository (optional):")])['repo_name']
    desc = inquirer.prompt([inquirer.Text('desc', message="Description of the repository (optional):")])['desc']

    if not create_new_repo(token, repo_name, desc, path):
        print("Something went wrong...")
    else:
        print(f"The repository {repo_name} was created successfully!")


def exit_cli():
    exit()


def set_user():
    user = ""
    while not user:
        user_answer = inquirer.prompt([inquirer.Text('user', message="User:")])
        user = user_answer['user']
        if not user_exists(user):
            print(f"Couldn't find a user by the name of {user}. Please try again.")
            user = ""
    return user

def set_token():
    return inquirer.prompt([inquirer.Password('token', message="Token:")])['token']

#login
def login():
    user = set_user()
    token = set_token()
    return user, token


#check if user exists
def user_exists(user):
    url = f"https://api.github.com/users/{user}"
    response = requests.get(url)
    return response.status_code == 200




if __name__ == '__main__':
    while True:
        menu = {
            'Login' : login,
            'Clone an existing Repository' : clone_repo,
            'Create a new Repository' : create_repo,
            'gtfo' : exit_cli
        }

        questions = [
            inquirer.List('menu', message="Please select an action you'd like to perform: ", choices=list(menu.keys())),
        ]


        answers = inquirer.prompt(questions)
        choice = answers['menu']
        if choice in menu:
            menu[choice]()

