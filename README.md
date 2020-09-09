# personal-api

**DESCRIPTION:** An API for personal consumption

This project will host several APIs that can be used for personal consumption:

- URL shortener

## How to use


This project is bootstrapped with a model named `SampleModel` so that you can test your
setup. Before starting the server the first time, it is advised that you create
the models relevant to your application and change all references to it to
point to your models.  After that, create the inicial migration with:

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

## API Docs

You can access the API documentation by running the application server:

```
$ make runserver-dev
```

and accessing:

<http://localhost:8000/>

## Testing celery is working


```
$ make shell

from datetime import datetime
from random import randint

from core.tasks import check_celery_is_up

random_number = randint(1000, 9999)
check_celery_is_up.apply_async(kwargs={'random_number': random_number, 'now_timestamp': datetime.now()})

```
