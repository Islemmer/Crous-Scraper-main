@echo off

:: Étape 1 : Créer et activer l'environnement virtuel s'il n'existe pas
if exist "venv" (
    call "venv\Scripts\activate.bat"
) else (
    py -m venv venv
    call "venv\Scripts\activate.bat"
    pip install -r REQUIREMENTS.txt
)

:: Étape 2 : Lire ou demander le token Telegram
if exist "token.txt" (
    set /p BOT_TOKEN=<token.txt
) else (
    set /p BOT_TOKEN=Veuillez entrer votre token :
    echo %BOT_TOKEN%>token.txt
)

:: Nettoyer l'écran
cls

:: Étape 3 : Lancer le script principal
py main.py

pause

