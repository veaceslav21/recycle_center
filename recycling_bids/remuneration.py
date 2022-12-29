from users.models import User
from db import db


def user_remuneration(user, material_type, capacity):
    if material_type in ("plastic", "glass"):
        if capacity <= 5:
            user.points += 5
            user.request_count += 1
            user.rating = user.points / user.request_amount
        elif 5 < capacity <= 10:
            user.points += 7
            user.request_count += 1
            user.rating = user.points / user.request_amount
        else:
            user.points += 10
            user.request_count += 1
            user.rating = user.points / user.request_amount

    if material_type == "paper":
        if capacity <= 8:
            user.points += 5
            user.request_count += 1
            user.rating = user.points / user.request_amount
        elif 8 < capacity <= 20:
            user.points += 7
            user.request_count += 1
            user.rating = user.points / user.request_amount
        else:
            user.points += 10
            user.request_count += 1
            user.rating = user.points / user.request_amount

    db.session.commit()
