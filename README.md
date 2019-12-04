[![Build Status](https://travis-ci.org/mwinel/koffie-time-api.svg?branch=develop)](https://travis-ci.org/mwinel/koffie-time-api)   [![Maintainability](https://api.codeclimate.com/v1/badges/53834ee596cb847f6923/maintainability)](https://codeclimate.com/github/mwinel/koffie-time-api/maintainability)

# koffie-time-api

Online blog publishing RESTful API.

### Technologies

- [Python3](https://www.python.org/download/releases/3.0/)
- [Django](https://www.djangoproject.com/)
- [Django restframework](https://www.django-rest-framework.org/)
- [Postgres](https://www.postgresql.org/)

### Pre-requirements.

- Install [python](https://www.python.org/downloads/)
- install [Postgresql](https://www.postgresql.org/download/)

### Installation

- Clone the [repository](https://github.com/mwinel/koffie-time-api.git)
- Create a `.env` file. See the `.env_example` in the root directory.
- Install a [virtual environment](https://virtualenv.pypa.io/en/latest/installation/).
- Activate the virtual environment and export the environment variables.
- Run `$ pip3 install -r requirements.txt` to install dependencies.
- Run `$ python3 manage.py makemigrations` to generate migrations.
- Run `$ python3 manage.py migrate` to add database tables.
- Run `$ python3 manage.py runserver` to start the local server.

### Testing

Use the following command to run unit tests.

```
coverage run manage.py test koffietime/apps/
```

Use the following command to check for test coverage.

```
coverage report
```

### Changes

See [CHANGELOG.md]() for detailed list of changes between releases.

### Release

See [RELEASE.md]() for information about how to make a new release.

### Bug Tracker

Browse open issues and submit new ones in [Github Issues]().

We are dedicating the Github Issue only for bugs in our codebase. For general questions, start a new thread in the [Community forum]() instead of opening a new Issue.

After you have opened a new issue, the team will handle it according to these instructions: [How to handle Github Issues]()

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

### License

[MIT](https://choosealicense.com/licenses/mit/)
