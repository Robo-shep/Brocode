@echo off
echo Installing required packages...
pip install flask flask-cors requests beautifulsoup4 nltk spacy praw dash plotly pandas
echo.
echo Starting the Flask server...
start cmd /k python app.py
echo.
echo Waiting for server to start...
timeout /t 5
echo.
echo Opening test frontend...
python -c "import webbrowser; webbrowser.open('file://' + os.path.abspath('test_frontend.html'))"
echo.
echo Done! The Flask server is running in a separate window.
echo Press any key to exit...
pause > nul
