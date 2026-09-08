"""Domain models (post-census)."""


class User:
    def __init__(self, name, admin=False):
        self.name = name
        self.admin = admin
