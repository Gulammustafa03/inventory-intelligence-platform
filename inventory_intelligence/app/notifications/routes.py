from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Notification

bp = Blueprint("notifications", __name__, url_prefix="/notifications")


@bp.route("/")
@login_required
def index():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template("notifications/index.html", notifications=notifications)


@bp.route("/mark-read", methods=["POST"])
@login_required
def mark_read():
    notification_id = request.form.get("notification_id", type=int)
    if notification_id:
        notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first()
        if notification and not notification.is_read:
            notification.is_read = True
            db.session.commit()
    return redirect(request.referrer or url_for("notifications.index"))


@bp.route("/mark-all-read", methods=["POST"])
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({"is_read": True})
    db.session.commit()
    return redirect(request.referrer or url_for("notifications.index"))


@bp.route("/count")
@login_required
def count():
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({"unread_count": unread_count})


@bp.route("/latest")
@login_required
def latest():
    notifications = (
        Notification.query.filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(5)
        .all()
    )
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify(
        {
            "unread_count": unread_count,
            "notifications": [
                {
                    "id": n.id,
                    "title": n.title,
                    "message": n.message,
                    "is_read": n.is_read,
                    "created_at": n.created_at.isoformat(),
                }
                for n in notifications
            ],
        }
    )
