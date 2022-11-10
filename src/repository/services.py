from github import Github
from . import utils
import requests

github = Github()

def get_nik(user):
    """Поиск nik в github пользователя"""
    account = user.user_account.all()
    nik = ''
    for item in account:
        nik = item.nickname_git
        return nik

def get_my_repository(repository, nik):
    """Поиск репозитория пользователя"""
    user_repos = get_user_repos(nik)
    cur_repo = repository.split('/')[-1]
    if cur_repo in user_repos:
        return cur_repo


def get_user_repos(nik):
    """Поиск всех репозиториев пользователя"""
    user_info = requests.get(f'https://api.github.com/users/{nik}/repos')
    repos = user_info.json()
    user_repos = []
    for repo in repos:
        user_repos.append(repo.get('name'))
    return user_repos

def get_stars_count(nik, repo):
    """Получение колличества звезд репозитория"""
    repo_info = requests.get('https://api.github.com/repos/' + nik + '/' + repo)
    stars = repo_info.json()['stargazers_count']
    return stars

def get_forks_count(nik, repo):
    """Получение колличества форков репозитория"""
    repo_info = requests.get('https://api.github.com/repos/' + nik + '/' + repo)
    forks_count = repo_info.json()['forks_count']
    return forks_count

def get_last_commit(nik, repo):
    """Получение даты последнего комментария репозитория"""
    repo_info = requests.get(f'https://api.github.com/repos/{nik}/{repo}/commits')
    last_commit = repo_info.json()[0]['commit']['author']['date']
    return last_commit

def get_commits_count(nik, repo):
    """Получение даты последнего комментария репозитория"""
    repo_info = requests.get(f'https://api.github.com/repos/{nik}/{repo}/commits')
    commits_count = 0
    commits = repo_info.json()
    for commit in commits:
        commits_count += 1
    return commits_count

def get_repository(repository):
    return github.get_repo(f'{"/".join(repository.split("/")[-2:])}')


def get_projects_stats(projects):
    for project in projects:
        repository = get_repository(project.repository)
        utils.repository_stats(project, repository)
    return projects


def get_project_stats(project):
    repository = get_repository(project.repository)
    utils.repository_stats(project, repository)
    return project
