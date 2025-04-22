# Redis application with python and flask 

The application for this project is a Flask based application in Python to demonstrate how to use redis. To run the application do the following steps. 

### Step 1: Run redis in docker

docker run --name redis-server -p 6379:6379 -d redis

### Step 2: Clone the repository 

git clone https://github.com/NatasjaVitoft/redis.git

### Step 3: Create and activate enviroment

python -m venv venv .\venv\Scripts\activate

### Step 4: Install requirements

pip install -r requirements.txt

### Step 5: Run the python application 

python app.py

## Interacting with the Application Using Postman

You can use other tools than postman but that is what we used and recommend to use. 

### Configuration 1 

If you want to create a new user with the retention policy for configuration 1, then create a new request in postman and the URL should be: http://127.0.0.1:5000/user

The body of the request should be something like this (a test user):
{
  "id": "user123",
  "name": "user123",
  "email": "user@user.com"
}

When you click send the user is created if you have done everything correct and you should see this message in JSON:
{
  "message": "User has been added and will expire after 60 seconds"
}

In the folder "app/images" there are some screenshots that shows how it should look in postman. 