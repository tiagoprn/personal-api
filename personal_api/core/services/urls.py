# Here is business logic code.
# It must NOT have any reference to models, to ease unit testing.


def clean_url(url: str) -> str:
    # TODO: return the original URL, stripping tracking information
    return url


def shorten_url(url: str, uuid: str) -> str:
    # TODO: return the shortened URL.
    # Try to use something related to the django model's UUID.
    return url
