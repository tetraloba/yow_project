from .linguist import create_linguist
from .config import settings

repository_paths = settings.get('paths', None)
if repository_paths is None:
    repository_path = settings.get('path', None)
    print('Error. "confing.py / settings / path" not found')
    exit()
for repository_path in repository_paths:
    create_linguist(repository_path)
