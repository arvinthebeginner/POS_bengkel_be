from flask_jwt_extended import get_jwt


def get_branch_id_from_jwt() -> str:
    return get_jwt()["branch_id"]
