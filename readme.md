# College Portal

## Software required to run
Python 3.9.5  
Django 3.2  
Bootstrap3 app for Django  

## How to run
Navigate inside nmit folder and run these in command prompt
### First time run
Install the bootstrap3 app

` $ pip install django-bootstrap3`
### For Every other time
` $ python manage.py runserver`
### To create super user
` $ python manage.py createsuperuser`

## Login details to use software
### Student
Username: 1NT19IS176  
Password : 1NT19IS176  
### Teacher
Username : Akash  
Password : ABC123!  
### HOD
Username : Sanjay  
Password : madhu1234  

## Using student creation script
Students profile can be created using student creation script
Add the student details into student.json file
In command prompt run

` $ python manage.py shell`

` $ exec(open("studentCreationScript.py").read())`
