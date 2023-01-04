from flask import Blueprint
from centers.models import Center
from recycling_bids.models import Application
from users.models import User
from sqlalchemy import func
from db import db
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

statistic_bp = Blueprint("statistic_bp", __name__)


@statistic_bp.route("/general", methods=["GET"])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def get_user_stats():
    """get statistics of a logged user"""
    user = User.query.get(get_jwt_identity())

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
