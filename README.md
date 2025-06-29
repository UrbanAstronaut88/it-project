# IT Company Task Manager

Task management system for the IT team
Task manager for IT team: keep track of tasks, projects and members in one place.

## Check it out!
[company-task-manager.render.com](https://company-task-manager-oodl.onrender.com)
Use a test account:
* login: user
* password: user12345 


## Installation

Python3 must be already installed

```shell
git clone https://github.com/UrbanAstronaut88/it-project.git
cd portfolio-it-project
python -m venv venv
venv\Scripts\activate
pip install -requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runsever  # starts Django Server
```

## Features

It Company Task Manager is a Django application designed to manage work tasks and projects in a team. Users can create projects, assign tasks to employees, track completion and deadlines.

Essential Functions:
* CRUD for projects and tasks
* Assigning employees to tasks
* Consideration of task types and priorities
* Filtering of tasks by projects and executors
* User authorisation and registration
* Admin panel for convenient data management

## Project structure

* main/ - main application (models, views, templates)
* templates/ - HTML templates
* static/ - CSS and JS files
* tests.py - unit-tests of models
* requirements.txt - list of dependencies


## Tech Stack

* Python 3.11+
* Django 5+
* Bootstrap 5 (via templates)
* SQLite (default)
* HTML, CSS

## Testing

Use to run the tests:
* python manage.py test

Models covered: Project, TaskType, Task, Worker.
Checks creation, links, task filtering, cascading deletion and worker assignment.

## Contributing

If you have suggestions on how to improve the project, open an issue or send a pull request.

Want to customise it for your needs? Fork it and adapt it!!

[IT Company Task Manager Home Page](demo_hp.png)