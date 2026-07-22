from flask import Blueprint, jsonify

from models.models import BranchModel
from schemas.serializers import to_json_safe

branch_bp = Blueprint("branch", __name__)


@branch_bp.get("/branches")
def list_branches():
    branches = BranchModel.get_active()
    return jsonify(success=True, data=[to_json_safe(b) for b in branches])
