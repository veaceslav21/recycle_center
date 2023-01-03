from flask import Blueprint
from centers.models import Center
from recycling_bids.models import Application
from sqlalchemy import func
from db import db
from flask import jsonify
from users.auth import get_current_user

statistic_bp = Blueprint("statistic_bp", __name__)


@statistic_bp.route("/general", methods=["GET"])
def general_statistics():
    """get general statistics of all centers"""
    paper = db.session.query(func.sum(Application.capacity)).filter(Application.material_type == "paper").scalar()
    plastic = db.session.query(func.sum(Application.capacity)).filter(Application.material_type == "plastic").scalar()
    glass = db.session.query(func.sum(Application.capacity)).filter(Application.material_type == "glass").scalar()
    num_of_requests = Application.query.count()

    stats = {
        "paper_kg": paper,
        "plastic_kg": plastic,
        "glass_kg": glass,
        "num_of_requests": num_of_requests
    }
    return jsonify(stats)


@statistic_bp.route("/center/<int:id>")
def center_statistics(id):
    """get statistics of a center by id"""
    center = Center.query.filter_by(id=id).first()
    if not center:
        raise ValueError("Center does not exists")

    paper = db.session.query(func.sum(Application.capacity)).filter(Application.center_id == center.id) \
        .filter(Application.material_type == "paper").scalar()
    plastic = db.session.query(func.sum(Application.capacity)).filter(Application.center_id == center.id) \
        .filter(Application.material_type == "plastic").scalar()
    glass = db.session.query(func.sum(Application.capacity)).filter(Application.center_id == center.id) \
        .filter(Application.material_type == "glass").scalar()
    num_of_requests = len(center.recycling_bids)

    stats = {
        "paper_kg": paper,
        "plastic_kg": plastic,
        "glass_kg": glass,
        "num_of_requests": num_of_requests
    }
    return jsonify(stats)


@statistic_bp.route("/user")
def get_user_stats():
    """get statistics of a logged user"""
    user = get_current_user()

    paper = db.session.query(func.sum(Application.capacity)).filter(Application.user_id == user.id) \
        .filter(Application.material_type == "paper").scalar()
    plastic = db.session.query(func.sum(Application.capacity)).filter(Application.user_id == user.id) \
        .filter(Application.material_type == "plastic").scalar()
    glass = db.session.query(func.sum(Application.capacity)).filter(Application.user_id == user.id) \
        .filter(Application.material_type == "glass").scalar()
    num_of_requests = len(user.recycling_bids)

    stats = {
        "paper_kg": paper,
        "plastic_kg": plastic,
        "glass_kg": glass,
        "num_of_requests": num_of_requests
    }
    return jsonify(stats)
