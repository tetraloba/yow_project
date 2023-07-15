from datetime import datetime
from os import getcwd, chdir, name, path

from yow.forSVG.mylib.calendar.calendar import Calendar

from yow.forSVG.mylib.heatmap.heatmap import create_heatpmap
from yow.forSVG.mylib.heatmap.git import get_commits_per_date
from yow.forSVG.mylib.heatmap.config import settings as heatmap_settings

from yow.forSVG.mylib.linguist.linguist import create_linguist
from yow.forSVG.mylib.linguist.config import settings as linguist_settings

from yow.forSVG.mylib.abstinence.abstinence import create_abstinence

from yow.forSVG.mylib.integrate.integrate import create_integrated

from yow.forSVG.mylib import svg2png
from yow.forSVG.mylib import change_wallpaper



chdir(path.abspath('yow/forSVG'))
work_dir = getcwd()
tmp_dir = path.abspath('tmp')
wallpaper_path = path.join(tmp_dir, 'wallpaper.png')
today = datetime.today()
date = str(today.year)[2:] + str(today.month).zfill(2) + str(today.day).zfill(2)

# .\.venv\Scripts\Activate.ps1 # python venv start


# calendar
calendar = Calendar(1920, 1080, 200, 200, 1870, 1030, 50) # regular
calendar.draw_calendar(path.join(tmp_dir, 'calendar.svg'))


# heatmap
for repository_path in heatmap_settings['paths']: # todo 例外処理
    strings = get_commits_per_date(repository_path)
    create_heatpmap(strings, path.join(tmp_dir, 'heatmap.svg'))


# linguist
repository_paths = linguist_settings.get('paths', None)
if repository_paths is None:
    print('Error. "confing.py / settings / path" not found')
    exit()
for repository_path in repository_paths:
    create_linguist(repository_path, path.join(tmp_dir, 'linguist.svg'))


# abstinence
create_abstinence(path.join(tmp_dir, 'abstinence.svg'))


# integrate
integrated_path = path.join(tmp_dir, 'integrated.svg')
create_integrated(integrated_path)

# SVG->PNG convert
svg2png.convert(integrated_path, wallpaper_path)

# change Windows wallpaper
if name == 'nt':
    change_wallpaper.change_wallpaper(wallpaper_path)

# deactivate # python venv stop

# Remove .png and .svg created more than 1 day ago
# Get-ChildItem | Where-Object {($_.Mode -eq "-a----") -and ($_.CreationTime -lt (Get-Date).AddDays(-1))} | Remove-Item -in *.png,*.svg
