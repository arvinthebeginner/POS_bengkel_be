from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson.objectid import ObjectId

from models.models import StokModel
from schemas.serializers import to_json_safe
from utils.jwt_utils import get_branch_id_from_jwt

stok_bp = Blueprint("stok", __name__, url_prefix="/stok")


@stok_bp.get("")
@jwt_required()
def list_stok():
    branch_id = get_branch_id_from_jwt()
    stok_list = StokModel.find_by_branch(branch_id)
    return jsonify(success=True, data=[to_json_safe(s) for s in stok_list])


@stok_bp.post("")
@jwt_required()
def create_stok():
    branch_id = get_branch_id_from_jwt()
    body = request.get_json(silent=True) or {}
    required = ["nama", "kategori", "harga", "stok"]
    if not all(k in body for k in required):
        return jsonify(success=False, message="Field tidak lengkap"), 400

    data = {
        "nama": body["nama"],
        "kategori": body["kategori"],
        "harga": int(body["harga"]),
        "stok": int(body["stok"]),
        "branch_id": ObjectId(branch_id),
    }
    StokModel.insert_stok(data)
    return jsonify(success=True), 201


@stok_bp.get("/<stok_id>")
@jwt_required()
def get_stok(stok_id):
    branch_id = get_branch_id_from_jwt()
    stok_data = StokModel.find_by_id(stok_id)
    if not stok_data or str(stok_data["branch_id"]) != branch_id:
        return jsonify(success=False, message="Anda tidak memiliki akses ke stok ini"), 403

    return jsonify(success=True, data=to_json_safe(stok_data))


@stok_bp.put("/<stok_id>")
@jwt_required()
def update_stok(stok_id):
    branch_id = get_branch_id_from_jwt()
    stok_data = StokModel.find_by_id(stok_id)
    if not stok_data or str(stok_data["branch_id"]) != branch_id:
        return jsonify(success=False, message="Anda tidak memiliki akses ke stok ini"), 403

    body = request.get_json(silent=True) or {}
    required = ["nama", "kategori", "harga", "stok"]
    if not all(k in body for k in required):
        return jsonify(success=False, message="Field tidak lengkap"), 400

    updated_data = {
        "nama": body["nama"],
        "kategori": body["kategori"],
        "harga": int(body["harga"]),
        "stok": int(body["stok"]),
    }
    StokModel.update_stok(stok_id, updated_data)
    return jsonify(success=True)


@stok_bp.delete("/<stok_id>")
@jwt_required()
def delete_stok(stok_id):
    branch_id = get_branch_id_from_jwt()
    stok_data = StokModel.find_by_id(stok_id)
    if not stok_data or str(stok_data["branch_id"]) != branch_id:
        return jsonify(success=False, message="Anda tidak memiliki akses ke stok ini"), 403

    StokModel.delete_stok(stok_id)
    return jsonify(success=True)
