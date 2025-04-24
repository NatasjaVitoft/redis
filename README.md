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

### Configuration 1: Redis with Retention Policy 

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

In the folder "app/images" there are some screenshots that shows how it should look in postman and the code behind it is found in app/app.py file.

### Configuration 3. Redis Cluster

We tried to set up a Redis cluster consisting of 6 total instances where 3 of them acted as primaries, and 3 of them acted as "slaves", each assigned to their own "master".
We set the configuration up using 6 different docker containers all running on localhost, with an internal network configuration set up with docker-compose. 

We tried doing it as simple as possible, and spinning up the redis containers in cluster mode was never a problem, but connecting them together afterwards turned out to be a bit of a pain, because of how the redis shards communicate, and how Docker virtual networks works.

We at last found a solution with an extensive configuration of the virtual network, by assigning eah of the shards a static IPv4 adress, so they could use their default ports.

Now the shards could connect normally, and also transfer connection to the client normally.

the docker-compose configuration can be found in the `redis-cluster` directory. Because the connection of the cluster shards has to be done after container initialization. We have written a simple bash script, that runs the whole setup proces called `setup.sh`

This will only work on Linux hosts though (and Mac if bash is installed), so it also functions as setup documentation. 


### Configuration 4: Redis Security 

To set up some security features in Redis, you can use the Redis CLI to require a password before accessing data.
What we have done is that we changed the docker compose file to require a password before writing any commands. The new docker compose file is located in the folder called docker-security and not the regular docker folder.

We added the following lines to the docker-compose file:

```command: redis-server --requirepass VeryStrongPassword123```
```command: redis-server --slaveof redis1 6379 --masterauth VeryStrongPassword123 --requirepass VeryStrongPassword456```

These lines ensure that a password is required for both instances before writing any commands. 

We can test that password authentication works by running the Redis CLI in the redis1 container like this:

```docker exec -it redis1 redis-cli```

Then, if we try to run a command like this:

```SET mykey "Test"```

We get this error: "(error) NOAUTH Authentication required."

This error occurs because we haven't authenticated yet with a password.

To authenticate, we can use the following command with the password we set in the docker compose file:

``` AUTH VeryStrongPassword123 ```

After authenticating we can run all commands.
The issue with this is that it dosent specify if some users should have access to all commands or just limited access. This solution just assumes that if the user types in the password, then they should have access to all commands. 
What we can do to adress this issue is to implement some access control (ACL).

The steps we took to implement this were:

We started by running Redis CLI in the redis1 container like this:

```docker exec -it redis1 redis-cli```

Then, we wrote the password for global access as defined in the previous steps:

```AUTH VeryStrongPassword123```

After that, we used the ACL command to set an admin user with the password adminpassword123 that has access to all commands:

```ACL SETUSER admin on >adminpassword123+@all```

We authenticate with that user like this:

```AUTH admin adminpassword123```

We can also create a regular user with only read rights like this:

```ACL SETUSER regular on >regularuser123 +@read```

Then, we authenticate with the read-only user:

```AUTH regular regularuser123```

In this way we ensure that not all users have write access to the Redis database if we want to control that. 