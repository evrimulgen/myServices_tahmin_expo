## Matches

### Getting list of matches ###

Description: Returns a list of SimpleMatch objects of today

Endpoint `GET /v1/matches/`

`NOTE: If you want to get list of matches of another day, send a request like this: /v1/users/matches/?date=20-04-2018`

Response: 201 and list of SimpleMatch objects

### Making a prediction about a match

`Authentication token is required in this endpoint`

Description: Creates a prediction about the given match

Endpoint `POST /v1/matches/:match_id/predictions/`

Payload:

```
{
    "text": "string",
    "game*": "string"
}
```

`NOTE*: "game" is required and it must be from available games list`

Response 201 and Prediction object

### Getting list of predictions

Description: Returns a list of Prediction objects of today

Endpoint `GET /v1/matches/:match_id/predictions/`

Response: 200 and list of Prediction objects

### Get a prediction

Description: Returns the requested prediction

Endpoint `GET /v1/matches/:match_id/predictions/:prediction_id/`

Response: 200 and a Prediction object

### Deleting a prediction

`Authentication token is required in this endpoint`

Description: Deletes the requested prediction

Endpoint `DELETE /v1/matches/:match_id/predictions/:prediction_id/`

Response: 204 and a Prediction object

### Updating a prediction

`Authentication token is required in this endpoint`

Description: Updates the requested prediction

Endpoint `PATCH /v1/matches/:match_id/predictions/:prediction_id/`

Payload:

```
{
    "text": "string",
    "game": "string"
}
```

Response: 200 and a Prediction object

### Post a message

`Authentication token is required in this endpoint`

Description: Posts a message to the match's thread

Endpoint `POST /v1/matches/:match_id/messages/`

Payload:

```
{
    "text": "string"
}
```

Response: 201 and a message object

### Getting list of messages

Description: Returns a list of Prediction objects of today

Endpoint `GET /v1/matches/:match_id/messages/`

Response: 200 and list of Message objects

### Update a message

`Authentication token is required in this endpoint`

Description: Updates the given message to the match's thread

Endpoint `PATCH /v1/matches/:match_id/messages/:message_id/`

Payload:

```
{
    "text": "string"
}
```

Response: 200 and a message object

### Delete a message

Description: Deletes the given message

Endpoint `DELETE /v1/matches/:match_id/messages/:message_id/`

Response: 204

### Get a message

Description: Returns the requested message

Endpoint `GET /v1/matches/:match_id/messages/:message_id/`

Response: 200 and a Message object

### Upvote a prediction

Description: Upvotes the given prediction

Endpoint `POST /v1/matches/:match_id/predictions/:prediction_id/upvote/`

Response: 200

### Undo Upvote a prediction

Description: Undo upvotes the given prediction

Endpoint `POST /v1/matches/:match_id/predictions/:prediction_id/undoupvote/`

Response: 200

### Get a match

Description: Returns the match, message, predictions and the events of the match. Events are not done yet.

Endpoint `GET /v1/matches/:match_id/`

Response 200

```
{
    "match": {
        "id": "integer",
        "home_team": {
            "id": "integer",
            "name": "string",
            "logo": "string" // S3 link
        },
        "away_team": {
            "id": "integer",
            "name": "string",
            "logo": "string" // S3 link
        },
        "score": "string",
        "minute": "string",
        "league": {
            "id": "integer",
            "name": "string",
            "logo": "string" // S3 Link
        }
        "datetime": "Unix timestamp"
        "iddaa_code": "string",
        "handicap": "-1",
        "prediction_count": "integer",
        "message_count": "integer"
    },
    "predictions": [...,
        {
            "id": "integer",
            "game": "string",
            "text": "string",
            "upvote": "integer",
            "user": "SimpleUser object",
            "match": "SimpleMatch object"
        },
    ...],
    "messages": [...,
        {
            "id": "integer",
            "text": "string",
            "user": "Simple User",
            "match": "Simple Match",
            "date_created": "string" // Date time string 2018-04-19T23:07:58.286173+03:00
        },
    ...,],
    "games":
        {...,
            "Mac Sonucu": {
                "ms1": 1.4,
                "ms2": 2.4
            },
            "Karsilikli Gol": {
                "var": 1.1,
                "yok": 3.1
            },
        ...}
    "events": {
        "home_events": [...,
            {
                "event_type": "red_card",
                "time": "54",
                "text": "Volkan Demirel"
            },
        ...],
        "away_events": [...,
            {
                "event_type": "goal",
                "time": "46",
                "text": "Bafetimbi Gomis"
            },
        ...]
    }
}
```

### Get available games

Description: Returns the available game types for prediction

Endpoint `GET /v1/matches/:match_id/games/`

Response 200 and list of Game objects

### Get matchlist metadata

Description: Returns the metadata of the matchlist. For now it only contains dates.

Endpoint `GET /v1/matches/meta/`

Response 200 and

```
{
    "dates": [
        "15-08-2018",
        "24-08-2018",
        "26-08-2018",
        "25-08-2018",
        "17-08-2018",
        "18-08-2018",
        "19-08-2018",
        "20-08-2018",
        "13-08-2018",
        "14-08-2018"
    ]
}
```

#### SimpleMatch Object

```
{
    "id": "integer",
    "home_team": {
        "id": "integer",
        "name": "string",
        "logo": "string" // S3 link
    },
    "away_team": {
        "id": "integer",
        "name": "string",
        logo": "string" // S3 link
    },
    "score": "string",
    "minute": "string",
    "league": {
        "id": "integer",
        "name": "string",
        "logo": "string" // S3 Link
    },
    "datetime": "Unix timestamp",
    "prediction_count": "integer",
    "message_count": "integer"
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

#### Message object

```
{
    "id": "integer",
    "text": "string",
    "user": "Simple User",
    "match": "Simple Match",
    "date_created": "string" // Date time string 2018-04-19T23:07:58.286173+03:00
}
```

#### Game object

```
{
    "Mac Sonucu": [
        {"ms1": 1.4},
        {"ms2": 2.4},
    ],
    "Karsilikli Gol": [
        {"var": 1.1},
        {"yok": 3.1}
    ]
}
```

#### Event object

```
{
    "event_type": "string",
    "time": "string",
    "text": "string"
}
```

#### Team object

```
{
    "id": "integer",
    "name": "string",
    "logo": "string" // S3 link
}
```

##### Event Type List

- Red Card: {"event_type": "red_card", "text": "Volkan Demirel", "time": "54"}
- Yellow Card: {"event_type": "yellow_card", "text": "Dele Alli", "time": 78"}
- Goal: {"event_type": "goal", "text": "Mohamed Salah", "32"}
- Substitution {"event_type": "substitution", "text": "Gabriel Jesus - Sergio Aguero"}

#### Handicap explained

```
{
    "handicap": "-1"
}
```
means:

Away team has 1 goal advantage in handicap bets

```
{
    "handicap": "1"
}
```
means:
Home team has 1 goal advantage in handicap bets
