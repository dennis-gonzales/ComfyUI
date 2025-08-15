@echo off
echo Starting ComfyUI...

REM Pull latest changes from upstream master
echo Pulling latest changes...
git pull upstream master

REM Check if conda is available
where conda >nul 2>&1
if errorlevel 1 (
    echo Error: Conda is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if the conda environment exists
if not exist "comfy_env" (
    echo Error: Conda environment 'comfy_env' not found
    echo Please create the environment first
    pause
    exit /b 1
)

REM Activate the conda environment
echo Activating conda environment...
call conda activate ./comfy_env
if errorlevel 1 (
    echo Error: Failed to activate conda environment
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found
    pause
    exit /b 1
)

REM Run the main script
echo Starting ComfyUI application...
python ./main.py

REM Keep the window open if there's an error
if errorlevel 1 (
    echo ComfyUI exited with an error
    pause
)