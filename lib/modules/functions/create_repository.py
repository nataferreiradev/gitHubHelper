from ..configGenerator import config_generator
from ..validators import validator
from rich.console import Console
import requests

class CreateRepository():
    def __init__(self) -> None:
        self.config_generator = config_generator.ConfigGenerator()
        self.url = "https://api.github.com/user/repos"
        self.config_section = self.config_generator.ConfigSection.UserAutentication
        self.headers = {}
        self.json = {}
        self.console = Console()

    def create_repository(self):
        if not self.check_configured_token():
            self.console.print("[red]Not authenticated[/red]")
            return

        name = input('Type repository name: ')
        while True:
            is_public = input('Is repository public? [(Y)es | (N)o]: ').strip().lower()
            if is_public in ('y', 'n'):
                break
            self.console.print("[red]Invalid option[/red]")

        self.json = {"name": name, "private": is_public == 'n'}

        try:
            response = requests.post(self.url, headers=self.headers, json=self.json)
            if response.status_code == 201:
                print('Repository created')
            else:
                self.console.print(f"[red]Error: {response.status_code}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def check_configured_token(self):
        config = self.config_generator.get_config(self.config_section)
        if not config or not validator.strNotEmpty(config.get('token')):
            return False
        self.headers = {'Authorization': f"token {config['token']}"}
        return True
