import subprocess
import os

def commit_changes(repo_url):
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_url, check=True)
        subprocess.run(['git', 'commit', '-m', 'Automatic saving of changes'], cwd=repo_url, check=True)
        print('The changes have been successfully commit.')
    except subprocess.CalledProcessError as e:
        print(f'Error while committing changes: {e}')

def stash_changes(repo_url):
    try:
        subprocess.run(['git', 'stash'], cwd=repo_url, check=True)
        print('The changes have been successfully hidden in the stash.')
    except subprocess.CalledProcessError as e:
        print(f'Error when hiding changes in stash: {e}')

def apply_stash(repo_url):
    try:
        subprocess.run(['git', 'stash', 'apply'], cwd=repo_url, check=True)
        print('The changes from the stash have been successfully applied.')
    except subprocess.CalledProcessError as e:
        print(f'Error when applying changes from stash: {e}')

def update_repository(repo_url):
    try:
        stash_changes(repo_url)  # Попробуем спрятать изменения перед pull
        subprocess.run(['git', 'pull'], cwd=repo_url, check=True)
        apply_stash(repo_url)  # Применяем изменения из стэша после pull
        print('The repository has been successfully updated.')
    except subprocess.CalledProcessError as e:
        print(f'Error when updating the repository: {e}')

try:
    repo_url = os.getcwd()
    update_repository(repo_url)
except Exception as e:
    error_message = f'error: {e}\n'
    with open('log.txt', 'a') as error_file:
        error_file.write(error_message)