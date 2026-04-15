@echo off
echo Installation des dependances...
pip install -r requirements.txt
echo.
echo Configuration de la base de donnees...
python setup_db.py
echo.
echo Lancement de Smart Management System...
python main.py
pause
