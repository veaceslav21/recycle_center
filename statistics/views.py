from flask import Blueprint
from users.models import User
from centers.models import Center
from recycling_bids.models import Application
from sqlalchemy import func
from db import db
from flask import jsonify

statistic_bp = Blueprint("statistic_bp", __name__)


@statistic_bp.route("/general", methods=["GET"])
def general_statistics():
    paper = db.session.query(func.sum(Application.capacity)).filter(Application.material_type == "paper").scalar()
    plastic = db.session.query(func.sum(Application.capacity)).filter(Application.material_type == "plastic").scalar()
    glass = db.session.query(func.sum(Application.capacity)).filter(Application.material_type == "glass").scalar()
    num_of_requests = len(Application.query.all())

    stats = {
        "paper_kg": paper,
        "plastic_kg": plastic,
        "glass_kg": glass,
        "num_of_requests": num_of_requests
    }
    return jsonify(stats)
