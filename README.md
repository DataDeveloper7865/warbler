# Warbler

A microblogging twitter-clone web app
http://warblology.herokuapp.com/

## Tech Stack
Flask / PostgreSQL / Jinja / WTForms

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt

# seed and import database
createdb warbler
python seed.py

# start server
flask run
```

## Features
- Database relational mapping for user registration, follower/ing relationships, blocking other users, and "liking" posts.
- Posting a Warble (or < 140 character thought) and editing user profile.
- Admin privileges that override user profile editing restrictions. 
- Private accounts and custom 404 page. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
