AUTHORS = [{
                "first_name": "Leo",
                "last_name": "Tolstoy",
                "birth_year": 1828,
                "death_year": 1910,
                "country": "Russia",
                "slug": "leo-tolstoy"
            },
            {
                "first_name": "Stephen",
                "last_name": "King",
                "birth_year": 1947,
                "death_year": None,
                "country": "US",
                "slug": "stephen-king"
            }
        ]

GENRES = [{
                "name": "Horror fiction",
                "description": "Horror is a genre of fiction ...",
                "slug": "horror-fiction"
            },
{
                "name": "Fiction",
                "description": "Fiction is any creative work...",
                "slug": "fiction"
            }
]

BOOKS = [
        {
        "name": "Anna Karenina",
        "slug": "anna-karenina",
        "publish_year": 1978,
        "country": "Russia",
        "description": "The novel deals with themes of betrayal..."
        },
        {
        "name": "Hamlet",
        "slug": "hamlet",
        "publish_year": 1600,
        "country": "England",
        "description": "The Tragedy of Hamlet, Prince of Denmark..."
        },
]

USERS = [{
        "email": "admin@gmail.ru",
        "first_name": "admin",
        "last_name": "admin",
        "is_admin": True,
        "is_active": True,
        "password": "pbkdf2_sha256$600000$bZzyak22wNH4sQ0vc4sPxy$zeNypimx7LpsJMV13mMWHjW8sLxX7F8U5wvz/V7s6GI=",
        "country": "USA",
        "phone": "+1 (23432)"
        },
        {
        "email": "user@gmail.ru",
        "first_name": "user",
        "last_name": "user",
        "is_admin": False,
        "is_active": True,
        "password": "pbkdf2_sha256$600000$ce183vzjlFyO9nZ8wwvcGz$V2K/IjtdAsBw/pSqyjYBQf3zstldJsQeu2hn56ZH9Mc=",
        "country": "France",
        "phone": "+4 (23432)"
        },
        {
        "email": "unknown@gmail.ru",
        "first_name": "unknown",
        "last_name": "unknown",
        "is_admin": False,
        "is_active": False,
        "password": "pbkdf2_sha256$600000$dLKXUOAztPjrsQQu1lcRMV$tA53flAEsUZaW4eiqau7PzecpCCDQKHrIPy2MPg5ClE=",
        "country": "Russia",
        "phone": "+7 (23432)"
        },
]
from apps.books.models import *
from apps.users.models import User
class SetUP():
    authors = (Author.objects.create(**author) for author in AUTHORS)
    genres = (Genre.objects.create(**genre) for genre in GENRES)
    books = (Book.objects.create(**book) for book in BOOKS)
    users = (User.objects.create(**user) for user in USERS)