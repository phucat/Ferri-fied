from git import Repo
import re
import logging


def extract_info(dir):
    repo = Repo(dir)

    try:
        project = re.search(r'/([^/.]+?)\.git', repo.remotes[0].url).groups()[0]
    except:
        logging.warning("Deploying from non-upstreamed repository")
        project = 'local'

    branch = repo.active_branch.name

    return (project, branch)
