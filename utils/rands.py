from random import SystemRandom

from django.utils.text import slugify


def random_letters(k: int = 5):
    return "".join(
        SystemRandom().choices(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=k
        )
    )


def slugify_new(text: str, k: int) -> str:
    return slugify(text) + "-" + random_letters(k=k)
