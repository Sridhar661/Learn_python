# Python Task Tracker CLI

A beginner-friendly Python project suitable for GitHub.

## Features
- Add, list, complete, and delete tasks
- Save tasks in a JSON file
- Separate modules for models, storage, business logic, and CLI
- Unit tests using Python's built-in `unittest`
- No third-party dependencies

## Requirements
Python 3.10 or newer.

## Run the project
```bash
python main.py add "Learn Python classes"
python main.py add "Push my project to GitHub"
python main.py list
python main.py done 1
python main.py list
python main.py delete 2
```

Task data is saved automatically to `data/tasks.json`.

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Push to GitHub
Create an empty repository on GitHub, then run these commands from this folder:
```bash
git init -b main
git add .
git commit -m "Add Python task tracker sample project"
git remote add origin https://github.com/YOUR-USERNAME/python-task-tracker.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username.
