from db import db


class Center(db.Model):
    __tablename__ = "centers"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    # types of materials
    glass = db.Column(db.Boolean)
    plastic = db.Column(db.Boolean)
    paper = db.Column(db.Boolean)

    def __repr__(self):
        return f"Center: {self.address}"

    @staticmethod
    def find_by_address(address):
        center = Center.query.filter_by(address).first()
        return center if center else None