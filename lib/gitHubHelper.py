import sys
from modules.functions.repos import ReposFunc 
from modules.functions.config import config
from modules.functions.create_repository import CreateRepository
from modules.validators import validator
from rich.console import Console

def print_help():
    print('Usage:')
    print('  Remenber to config your user and token this will\n  - make possible to see yors private repositories')
    print('  python github_user_repos.py <function> <args>')
    print('Functions:')
    print('  -r --repos <user> - List repositories of the specified GitHub user')
    print('  -c --create       - Create a new reopository for authenticated user')
    print('     --config       - Start the process to config token and user')

def main():
    console = Console()
    if not validator.check_argument_count(1):
        console.print('[red]No function passed as parameter. Use -h to see the list of functions.[/red]')
        print_help()
        return

    func = sys.argv[1]

    if func in ['-r','--repos']:
        reposFunc = ReposFunc()
        reposFunc.get_repos()
    elif func == '--config':
        config()
    elif func in ['-c','--create']:
        createRepository = CreateRepository()
        createRepository.create_repository()
    elif func in ['-h', '--help']:
        print_help()
    else:
        console.print('[red]Invalid function. Use -h for help.[/red]')

if __name__ == "__main__":
    main()
