@echo off
echo Selenne uses python 3.11
echo Selenne will create a virtual enviroment for all the modules required so it will not affect the system modules.
pause

echo Cleaning pip cache...
pip cache purge

echo Creating virtual enviroment...
python -m venv env
call .\env\Scripts\activate

echo Updating pip...
python -m pip install --upgrade pip

echo Installing modules...
pip install -r requeriments.txt

echo Cleaning pip cache...
pip cache purge

call .\env\Scripts\desactivate

echo Done.
echo Copy config.example.yaml to config.yaml and fill it in (or set SELENNE_TOKEN) so the bot can boot
echo Run Selenne.bat to launch the bot.
pause