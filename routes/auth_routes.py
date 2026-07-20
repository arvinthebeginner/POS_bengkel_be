from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson.objectid import ObjectId
import bcrypt

from models.models import UserModel, BranchModel
from schemas.serializers import to_json_safe

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    username = body.get("username")
    password = body.get("password")
    if not username or not password:
        return jsonify(success=False, message="username & password wajib diisi"), 400

    user = UserModel.find_by_username(username)
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return jsonify(success=False, message="Username atau password salah"), 401

    token = create_access_token(identity=str(user["_id"]), additional_claims={
        "username": user["username"],
        "branch_id": str(user["branch"]),
    })
    return jsonify(success=True, data={"access_token": token})


@auth_bp.post("/register")
def register():
    body = request.get_json(silent=True) or {}
    required = ["username", "password", "email", "alamat", "notelp", "branch"]
    if not all(body.get(k) for k in required):
        return jsonify(success=False, message="Field tidak lengkap"), 400

    if UserModel.find_by_username(body["username"]):
        return jsonify(success=False, message="Username sudah ada"), 400

    hashed_password = bcrypt.hashpw(body["password"].encode("utf-8"), bcrypt.gensalt())
    data = {
        "username": body["username"],
        "password": hashed_password,
        "email": body["email"],
        "alamat": body["alamat"],
        "notelp": body["notelp"],
        "branch": ObjectId(body["branch"]),
    }
    UserModel.insert_user(data)
    return jsonify(success=True), 201


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = UserModel.find_by_id(user_id)
    if not user:
        return jsonify(success=False, message="User tidak ditemukan"), 404

    user_safe = to_json_safe(user)
    user_safe.pop("password", None)
    return jsonify(success=True, data=user_safe)


@auth_bp.post("/logout")
@jwt_required()
def logout():
    # JWT stateless: client cukup hapus token lokal.
    return jsonify(success=True, message="Logout berhasil, hapus token di client")
