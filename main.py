# Script to download to clone all GitLab repositories

import os
import subprocess
from typing import List, Tuple

import gitlab
from gitlab.v4.objects import Project

GITLAB_TOKEN = os.environ["GITLAB_TOKEN"]
GITLAB_URL = os.environ["GITLAB_URL"]
TARGET_DIR = os.environ["TARGET_DIR"]
GIT_URL_PREFIX = os.environ["GIT_URL_PREFIX"]
GIT_URL_SUFFIX = ".git"


def get_gl_projects(url: str, private_token: str) -> List[Project]:
    gl = gitlab.Gitlab(url, private_token=private_token)  # pylint: disable=invalid-name
    return gl.projects.list(all=True)


def print_info(projects: List[Project]) -> None:
    print(
        f"Cloning {len(projects)} repos from {GITLAB_URL} into '{TARGET_DIR}' directory\n"
    )


def remove_prefix(prefix: str, data: str) -> str:
    if data.startswith(prefix):
        return data[len(prefix) :]
    return data


def remove_suffix(suffix: str, data: str) -> str:
    if data.endswith(suffix):
        return data[: len(data) - len(suffix)]
    return data


def get_repo_dir_path(url: str) -> Tuple[str, ...]:
    url_repo = remove_prefix(GIT_URL_PREFIX, url)
    url_repo = remove_suffix(GIT_URL_SUFFIX, url_repo)
    return tuple(url_repo.split("/"))


def clone_projects(projects: List[Project]) -> None:
    print_info(projects)
    for project in projects:
        repo_url = project.http_url_to_repo
        repo_dir_path = get_repo_dir_path(repo_url)
        repo_target_path = os.path.join(TARGET_DIR, *repo_dir_path)
        os.makedirs(repo_target_path)
        subprocess.call(["git", "clone", repo_url, repo_target_path])


if __name__ == "__main__":
    gl_projects = get_gl_projects(GITLAB_URL, GITLAB_TOKEN)
    clone_projects(gl_projects)
