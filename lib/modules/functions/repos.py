import sys
import os
import pyperclip
import requests
from rich.console import Console
from rich.table import Table
from modules.validators import validator
from modules.configGenerator import config_generator 


class ReposFunc():
    def __init__(self) -> None:
        configGenerator = config_generator.ConfigGenerator()
        self.console = Console()
        self.username = sys.argv[2] if validator.check_argument_count(2) else ''
        self.url = f"https://api.github.com/users/{self.username}/repos"
        self.config = configGenerator.get_config(configGenerator.ConfigSection.UserAutentication)
        self.headers = {}
        self.params = {}
        self.user_data = {}

    def get_repos(self):
        if self.check_configured_token():
            self.check_user()

        response = requests.get(self.url,headers = self.headers,params = self.params)

        if response.status_code == 200:
            self.user_data = response.json()

            self.print_link_table()

            user_resp = input('Do you want to copy or clone some value? [(C)opy | c(L)one | (N)o]: ').strip()

            if validator.validate_case_insensitive(user_resp,'c') or not validator.validate_case_insensitive(user_resp,'l'):
                return

            if validator.validate_case_insensitive(user_resp, 'c'):
                self.copy_link()

            if validator.validate_case_insensitive(user_resp,'l'):
                self.clone_link()

            return
        self.console.print(f"[red]User {self.username} not found. Status code: {response.status_code}[/red]")

    def check_user(self):
        if self.config == None:
            return 

        if validator.check_argument_count(1):
            self.url = f"https://api.github.com/user/repos"
            self.params = {
                    'visibility': 'all',
                    'affiliation': 'owner,collaborator,organization_member'
                    }

    def check_configured_token(self):
        if self.config == None:
            return False
        if validator.strNotEmpty(self.config['token']):
            self.headers = {
                    'Authorization': f"token {self.config['token']}"
                    }
            return True
        return False

    def print_link_table(self):
        table = Table(title=f"Repositories of {self.username}")

        table.add_column("No.", style="bold")
        table.add_column("Repository", style="bold")
        table.add_column("Link")

        for i, repo in enumerate(self.user_data, start=1):
            table.add_row(str(i), repo['name'], repo['html_url'])

        self.console.print(table)

    def copy_link(self):
        index = int(input('Enter the number you want to copy: ').strip())
        if 1 <= index <= len(self.user_data):
            type_url = input('Enter the type of url you want to copy [(H)ttp | (S)sh]: ')
            if validator.validate_case_insensitive(type_url,'h'):
                url = 'git_url'
            elif validator.validate_case_insensitive(type_url,'s'):
                url = 'ssh_url'
            else:
                return

            try:
                pyperclip.copy(self.user_data[index - 1][url])
                print('URL copied to clipboard.')
            except ValueError:
                print('Error: Invalid number entered.')

    def clone_link(self):
        index = int(input('Enter the number you want to clone: ').strip())
        if 1 <= index <= len(self.user_data):
            type_url = input('Enter the method you want to uso [(H)ttp | (S)sh]: ')
            if validator.validate_case_insensitive(type_url,'h'):
                url = 'git_url'
            elif validator.validate_case_insensitive(type_url,'s'):
                url = 'ssh_url'
            else:
                return

            try:
                os.system(f'git clone {self.user_data[index - 1][url]}')            
            except ValueError:
                print('Error: Invalid number entered.')
