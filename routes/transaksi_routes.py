from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson.objectid import ObjectId

from models.models import StokModel, TransaksiModel
from schemas.serializers import to_json_safe
from utils.jwt_utils import get_branch_id_from_jwt

transaksi_bp = Blueprint("transaksi", __name__)


@transaksi_bp.get("/kasir/stok")
@jwt_required()
def kasir_stok():
    branch_id = get_branch_id_from_jwt()
    stok_list = StokModel.find_by_branch(branch_id)
    return jsonify(success=True, data=[to_json_safe(s) for s in stok_list])


@transaksi_bp.post("/transaksi")
@jwt_required()
def create_transaksi():
    branch_id = get_branch_id_from_jwt()
    body = request.get_json(silent=True) or {}
    barang = body.get("barang")
    total = body.get("total")
    if barang is None or total is None:
        return jsonify(success=False, message="Field 'barang' & 'total' wajib diisi"), 400

    data = {
        "barang": barang,
        "total": float(total),
        "branch_id": ObjectId(branch_id),
    }
    TransaksiModel.insert_transaksi(data)
    return jsonify(success=True), 201


@transaksi_bp.get("/transaksi")
@jwt_required()
def list_transaksi():
    branch_id = get_branch_id_from_jwt()
    transaksi_list = TransaksiModel.get_by_branch(branch_id)
    return jsonify(success=True, data=[to_json_safe(t) for t in transaksi_list])
