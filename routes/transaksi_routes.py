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
    barang_input = body.get("barang")

    if not barang_input or not isinstance(barang_input, list):
        return jsonify(success=False, message="Field 'barang' wajib diisi dan berupa list"), 400

    items = []
    for entry in barang_input:
        stok_id = entry.get("stok_id") if isinstance(entry, dict) else None
        qty = entry.get("qty") if isinstance(entry, dict) else None

        if not stok_id or not isinstance(qty, int) or qty <= 0:
            return jsonify(
                success=False,
                message="Setiap item wajib punya 'stok_id' dan 'qty' (bilangan bulat positif)",
            ), 400

        stok_data = StokModel.find_by_id(stok_id)
        if not stok_data or str(stok_data["branch_id"]) != branch_id:
            return jsonify(success=False, message=f"Stok dengan id {stok_id} tidak ditemukan"), 404

        if stok_data["stok"] < qty:
            return jsonify(
                success=False,
                message=(
                    f"Stok '{stok_data['nama']}' tidak mencukupi "
                    f"(sisa {stok_data['stok']}, diminta {qty})"
                ),
            ), 400

        items.append({
            "stok_id": stok_id,
            "nama": stok_data["nama"],
            "harga": stok_data["harga"],
            "qty": qty,
        })

    decremented = []
    for item in items:
        success = StokModel.decrement_stok(item["stok_id"], branch_id, item["qty"])
        if not success:
            for done in decremented:
                StokModel.increment_stok(done["stok_id"], done["qty"])
            return jsonify(
                success=False,
                message=f"Stok '{item['nama']}' berubah saat transaksi diproses, silakan coba lagi",
            ), 409
        decremented.append(item)

    barang_record = [{"nama": i["nama"], "qty": i["qty"], "harga": i["harga"]} for i in items]
    total = sum(i["harga"] * i["qty"] for i in items)

    data = {
        "barang": barang_record,
        "total": total,
        "branch_id": ObjectId(branch_id),
    }
    TransaksiModel.insert_transaksi(data)
    return jsonify(success=True, data={"total": total}), 201


@transaksi_bp.get("/transaksi")
@jwt_required()
def list_transaksi():
    branch_id = get_branch_id_from_jwt()
    transaksi_list = TransaksiModel.get_by_branch(branch_id)
    return jsonify(success=True, data=[to_json_safe(t) for t in transaksi_list])
