Chatapp Built on Django and DRF

## Backend

To manually create a virtualenv on MacOS and Linux:

```
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following step to activate your virtualenv.

```
source .venv/bin/activate
```

### requirements

Once the virtualenv is activated, you can install the required dependencies.

```
python3 -m pip install --upgrade -r requirements.txt
```

After Installing the dependencies you can run server using

```
python3 manage.py runserver 8080
```

You can generate the requirement file using your virtualenv using

```
pip3 freeze > requirements.txt
```

#### Shell

The `shell` command is useful for development. It drops you into an python shell with the database connection.

```bash
> python manage.py shell
```

#### APIS

# Authentication Endpoints

- api/register - register a user.
- payload = {
  "name": "tester 1",
  "age": 22,
  "password": "password",
  "interests": {
  "cooking": 21,
  "computers": 66,
  "cars": 53
  }
  }

- api/login - when a user log in online is set to true and it will remain for 1 hour after than user should log in again return a token use it in header as Authorization: Token <str:token>.

- I have made all the users that was in the json list and made password as password only.

- payload = {
  "name": "tester 1",
  "password": "password"
  }

## Chat Management Endpoints

- api/online-users - Get all the online users (Open to all).
- api/suggested-friends/<str:user_id> - Give you a list of top 5 suggested users(Open to all).
- api/start-chat - Start a chat with a user, auhtorization should be provided as it will identify which user is requesting and should prode a name as which user you want to add, users should be online and should be a part of chat return a room_name use it in websocket.

# WebSocket Chat Endpoint

- api/chat/send/<str:room_name> - connect to the chat room and start chatting, users should be online and should be a part of chat room and authorization : Token <str:token> is required to indentify as a user
