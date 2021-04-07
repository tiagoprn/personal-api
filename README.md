# personal-api

**DESCRIPTION:** An API for personal consumption

This project will host several APIs that can be used for personal consumption:

- URL shortener

## How to use


This project is bootstrapped with a model named `SampleModel` so that you can test your setup. Before starting the server the first time, it is advised that you create the models relevant to your application and change all references to it to point to your models.  After that, create the inicial migration with:

```
$ make migrations
```

Then, apply them:

```
$ make migrate
```

## Creating superuser

In order to access the Django Admin, you will need to create a super user. Execute the command below and follow instructions:

```
$ make superuser
```

## API


### Documentation

You can access the API documentation by

1) Generating the static files directory:

```
$ make static
```

2) Raising the container to serve the static files:

```
$ make runstatic-dev
```

3) running the application server:

```
$ make runserver-dev
```

and accessing:

- [redoc](<http://localhost:8000/>)
- [swagger](<http://localhost:8000/swagger/>)


### Authentication token generation

To access protected endpoints, authentication is necessary. To do that, you must submit a query to the token generation endpoint. This will return 2 tokens, one named "access" and another "refresh". You must keep both values.

The access token is the one you must submit on every request. It expires in 5 minutes. When that happens, you must submit the "refresh" token from the previous requests you were asked to keep to the refresh token endpoint. This will generate another access token you can use for another 5 minutes.

The refresh token expires after 24 hours. After that, you must submit another request to the token generation endpoint.

On the Makefile, there are some commands so that you can experiment with that functionality:

```
$ make local-get-access-token username=tiago password=12345678  # get access token for given user/password combination

$ make local-test-user-token token=XXXXXX  # test the token, submiting a request to the greetings endpoint

$ make local-refresh-access-token refresh_token=XXXXXX  # generate a new access token from the refresh token (to be used when the access token expire).
```

## Testing celery is working


```
$ make shell

from datetime import datetime
from random import randint

from core.tasks import check_celery_is_up

random_number = randint(1000, 9999)
check_celery_is_up.apply_async(kwargs={'random_number': random_number, 'now_timestamp': datetime.now()})

```
