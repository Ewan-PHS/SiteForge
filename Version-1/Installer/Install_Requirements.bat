:: winget install -e --id Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements

cd %1

:: python-3.12.3-amd64_Installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

pip install -r requirements.txt