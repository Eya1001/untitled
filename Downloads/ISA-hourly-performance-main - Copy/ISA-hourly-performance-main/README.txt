pythonw.exe app.py
TASKKILL /F /IM pythonw.exe

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

venv\Scripts\activate
deactivate
