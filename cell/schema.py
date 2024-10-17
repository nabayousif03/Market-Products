from ninja import Schema

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None
    first_name: str
    last_name: str
