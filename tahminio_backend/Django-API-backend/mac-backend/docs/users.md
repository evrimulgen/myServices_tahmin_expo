## Users

### Signup

Description: Creates a new user with given data

Endpoint `POST /v1/users/signup/`

Payload:

```
{
    "username": "string",
    "password": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
```

Response: 201 and UserMe object

Every field except bio are required.

Note: `password` and `email` are going through validators. Weak passwords and invalid emails will cause errors.

### Login ###

Description: Authenticates given user

Endpoint `POST /v1/users/login/`

Payload:

```
{
    "username": "string",
    "password": "string"
}
```

Response: 200 and UserMe object

### Get Me

`Authentication token is required in this endpoint`

Description: Returns the information about authed user (current user)

Endpoint `GET /v1/users/me/`

Response: 200 and UserMe object

### Delete Me

`Authentication token is required in this endpoint`

Description: Deletes the current user

Endpoint `DELETE /v1/users/me/`

Response: 204

### Update Me

`Authentication token is required in this endpoint`

Description: Updates the current user with given data

Endpoint `PATCH /v1/users/me/`

Payload

```
{
    "username": "string",
    "password": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "profile_photo": "Base64 string"
}
```

Note: You don't need to send every field. Sending the changing fields is enough.

Response: 200 and UserMe object

### Get Another User

`Authentication token is required in this endpoint`

Description: Returns the information about requested user

Endpoint `GET /v1/users/:user_id/`

Return: 200 and UserDetail object

### Change password of the authed user

`Authentication token is required in this endpoint`

Description: Changes the password of authed user

Endpoint `PATCH /v1/users/me/password/`

Payload

```
{
    "old_password": "string",
    "new_password": "string"
}
```

Return: 200 and UserMe object

### Follow a user

`Authentication token is required in this endpoint`

Description: Follows the given user

Endpoint `POST /v1/users/:user_id/follow/`

Return: 200

### Unfollow a user

`Authentication token is required in this endpoint`

Description: Unfollows the given user

Endpoint `POST /v1/users/:user_id/unfollow/`

Return: 200

### Verifying a user

Description: Verifies the user associated with the given code

Endpoint `GET /v1/users/activate/?key=:verification_key`

Return: 200

If this endpoint fails, it will return the reason why it has failed. There are two error messages this endpoint can return:

- Not verified in time -> User failed to activate his account within 12 hours.
- Verification not found -> Verification key is not found in the database.

### Search for user ###

Description: Searchs the user by username

Endpoint `GET /v1/search/users/?query=:your_query`

Return 200 and list of SimpleUser objects


## Forgot password routine

When a user forgots his/her password, we need to complete some steps to change the user's password. These steps are in order:

1. User request a password reset email from tahmin.io client with their username or email
2. An email with password reset link referring the user to tahmin.io is being sent to the user. The email is valid for 24 hours
3. User returns to the tahmin.io client with a password reset key
4. User enters the new password and client will send the key and the new password to the backend
5. Backend verifies the code and password then changes the password

### Requesting a password reset

Endpoint `POST /v1/users/forgot_password/`

Payload:

```
{
    "user_identifier": "string"
}
```

`user_identifier` can be username or email

Response is 200 no matter what, for protecting user's privacy

After this step, an email will be send to the user, containing a link like this:

`tahmin.io/change-password/?key=ABCDE1234567`

You will use the key in the url to change the user's password

### Changing a password with a password reset key

Endpoint `POST /v1/users/change_password/`

Payload:

```
{
    "key": "string" // The key in the link above
    "password": "string"
}
```

Response:
200 for successfull password change
404 for invalid key
400 for invalid password

### Getting list of trophies of the auther user

Endpoint `GET /v1/users/me/trophies/`

Response: 200 and list of Trophy objects

### Getting list of trophies of another user

Endpoint `GET /v1/users/:user_id/trophies/`

Response: 200 and list of Trophy objects

### All time leaderboard

Endpoint `GET /v1/leaders/:page_number/`

`For total page number send a request to /v1/leaders/total_pages/`

Response 200 and list of SimpleUser objects

### Get trophy progression of the authed user

`Authentication token is required in this endpoint`

Endpoint `GET /v1/users/me/progression/`

Response: 200 and list of TrophyProgression objects

### Get user feed

Returns the predictions of the user's followed by the authed user

`Authentication token is required in this endpoint`

Endpoint `GET /v1/users/feed/`

Response: 200 and list of Prediction objects

#### UserMe object

```
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "token": "string",
    "profile_photo": "Base64 string",
    "bio": "string",
    "first_name": "string",
    "last_name": "string",
    "trophies": [
        ...,
        {
            "id": "integer",
            "user": "SimpleUser object",
            "text": "string",
            "description": "string",
            "date_created": "string",
            "image": "string" // S3 link
        },
        ...
    ]
}
```

#### UserDetail object

```
{
    "id": "integer",
    "username": "string",
    "profile_photo": "string",
    "bio": "string"
}
```

#### SimpleUser object

```
{
    "id": "integer",
    "username": "string",
    "bio": "string",
    "profile_photo": "string",
    "trophies": [
        ...,
        {
            "id": "integer",
            "user": "SimpleUser object",
            "text": "string",
            "description": "string",
            "date_created": "string",
            "image": "string" // S3 link
        },
        ...
    ]
}
```


#### Trophy object

```
{
    "id": "integer",
    "text": "string",
    "user": {
        "id": "integer",
        "username": "string",
        "profile_photo": "string",
    },
    "description": "string",
    "date_created": "string",
    "image": "string" // S3 Link
}
```


#### TrophyProgression object

```
{
    "finished": "boolean",
    "text": "string",
    "description": "string",
    "current_count": "integer",
    "finish_count": "integer",
    "image": "string"
}
```

#### Prediction object

```
{
    "id": "integer",
    "game": "string",
    "text": "string",
    "upvote": "integer",
    "user": "SimpleUser object",
    "match": "SimpleMatch object"
}
```
