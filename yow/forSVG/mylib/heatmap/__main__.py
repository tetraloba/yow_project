from .heatmap import create_heatpmap

from .git import get_commits_per_date
from .config import settings

for path in settings['paths']: # todo 例外処理
    strings = get_commits_per_date(path)
    create_heatpmap(strings)
