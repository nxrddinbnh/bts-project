@echo off
echo Installation de CAN Sniffer - Moniteur Serie
echo ========================================

:: Verification si Python est installe
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installe sur ce systeme.
    echo Veuillez installer Python 3.8 ou superieur depuis https://www.python.org/downloads/
    echo Assurez-vous de cocher "Add Python to PATH" lors de l'installation.
    pause
    exit /b 1
)

echo Python est correctement installe.
echo Installation des dependances requises...

:: Creation d'un environnement virtuel (optionnel mais recommande)
echo Creation d'un environnement virtuel...
python -m venv venv
call venv\Scripts\activate.bat

:: Installation des dependances
echo Installation de PyQt6 et pyserial...
python -m pip install --upgrade pip
python -m pip install PyQt6>=6.9.0 pyserial>=3.5

:: Verification de l'installation
echo Verification de l'installation...
python -c "import PyQt6; import serial" > nul 2>&1
if %errorlevel% neq 0 (
    echo Une erreur est survenue lors de l'installation des dependances.
    pause
    exit /b 1
)

:: Creation du lanceur
echo @echo off > lancer_can_sniffer.bat
echo call venv\Scripts\activate.bat >> lancer_can_sniffer.bat
echo python serial_monitor.py >> lancer_can_sniffer.bat
echo pause >> lancer_can_sniffer.bat

:: Nettoyage des fichiers inutiles
echo Nettoyage des fichiers inutiles...
if exist theme_manager.py del theme_manager.py
if exist can_utils.py del can_utils.py
if exist ui_components.py del ui_components.py
if exist serial_thread.py del serial_thread.py
if exist lancer_moniteur_serie.bat del lancer_moniteur_serie.bat
if exist run_app.bat del run_app.bat

echo ========================================
echo Installation terminee avec succes!
echo Pour lancer l'application, executez "lancer_can_sniffer.bat"
echo ========================================
pause
