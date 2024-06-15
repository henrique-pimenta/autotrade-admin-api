from api.settings import *


SECRET_KEY = "test_SECRET_KEY"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}
