from .heatmap import create_heatpmap

from ..common.git import get_commits_per_date
from ..common.config import settings

strings = get_commits_per_date()
create_heatpmap(strings)
