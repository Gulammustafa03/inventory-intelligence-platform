from datetime import datetime

from .extensions import db, socketio
from .models import Notification, Role, User


def format_currency(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "₹0"

    integer_part = int(abs(value))
    sign = "-" if value < 0 else ""

    s = str(integer_part)
    if len(s) <= 3:
        formatted = s
    else:
        head = s[:-3]
        tail = s[-3:]
        parts = []
        while len(head) > 2:
            parts.append(head[-2:])
            head = head[:-2]
        if head:
            parts.append(head)
        formatted = ",".join(reversed(parts)) + "," + tail

    if value != integer_part:
        fraction = int(round((abs(value) - integer_part) * 100))
        if fraction == 100:
            integer_part += 1
            fraction = 0
        formatted = f"{formatted}.{fraction:02d}"

    return f"{sign}₹{formatted}"


def create_notification(user, title, message):
    notification = Notification(user_id=user.id, title=title, message=message)
    db.session.add(notification)
    db.session.commit()
    try:
        socketio.emit("notification", broadcast=True)
    except Exception:
        pass
    return notification


def notify_roles(roles, title, message):
    users = User.query.join(Role).filter(Role.name.in_(roles)).all()
    notifications = []
    for user in users:
        notifications.append(Notification(user_id=user.id, title=title, message=message))

    if notifications:
        db.session.bulk_save_objects(notifications)
        db.session.commit()
        try:
            socketio.emit("notification", broadcast=True)
        except Exception:
            pass
    return notifications
