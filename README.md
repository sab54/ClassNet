# How to Run ClassNet
## A.	Local Server

#### To run the application on local development environment, we need to separately run Django application and redis server.

#### Ensure python is installed and working. To check please run the following command in terminal:
        •  python –version

#### It is also recommended to use python virtual environment to install Django dependencies. The details are located at https://docs.python.org/3/library/venv.html.

### Redis server installation:
* On Linux, redis is installed from the package manager:
    •	sudo apt update
    •	sudo apt install redis-server
    •	sudo systemctl start redis

* Check if Redis is running:
        o	sudo systemctl status redis
* Verify if redis is still running 
        o	redis-cli

### Django application Installation and Setup Instructions
* Unzip the project classnet
* Navigate to classnet
* Install Django dependencies:
        o	pip install -r requirements.txt
* Run the development server:
        o	python manage.py runserver

### Logging into Site: Home page can be accessed through:  http://localhost:8000/

    Teacher and Student Login Credentials
    •	Teacher: teacher, password: password123
    •	Student: student, password: password123

================================================================

Note: Database is already setup in sqlitedb3 – Hence don’t have to run below commands: 

### Setting up database and creating superusers
* Set up the database:
    o	Python manage.py makemigrations 
    o	python manage.py migrate
* Create a superuser:
    o	python manage.py createsuperuser
    o	Follow the prompts to create the admin user.


## B.	AWS cloud
#### Classnet Django application is deployed to an AWS EC2 instance. 
   
#### All the necessary Django dependencies are installed and dataset is migrated.

### This classnet’s home page can be accessed using following url:
    •	http://35.179.227.81:8000/
### Application admin page can be accessed using:
    •	http://35.179.227.81:8000/admin/
            •	Username: admin
            •	Password: password
