🛠 Build Information

This Django application has been packaged into a standalone '.exe' file using [PyInstaller](https://pyinstaller.org/).

💻 How to Build the Executable

To build the '.exe':

Run in bash:
pyinstaller --name CustomerDataApp --onefile --console --add-data "customerinfo;customerinfo" --add-data "staticfiles;staticfiles" --add-data "db.sqlite3;." --add-data "customerdata;customerdata" run_django.py
