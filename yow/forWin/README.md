## for Windows
### 導入手順
- `git clone https://github.com/tetraloba/yow_project`
- `cd yow_project`
- `git checkout -b Win origin/Win`
- `Python -m venv yow\forWin\.venv`
- `.\yow\forWin\.venv\Scripts\Activate.ps1`
- `Python -m pip install -r .\yow\forWin\requirements.txt`
- requirements.txtのpkg_resources==0.0.0をコメントアウトした方が良いかも
- `Python -m yow.forWin`
