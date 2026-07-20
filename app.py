from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import JWT_SECRET_KEY
from routes.auth_routes import auth_bp
from routes.stok_routes import stok_bp
from routes.transaksi_routes import transaksi_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
JWTManager(app)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(stok_bp)
app.register_blueprint(transaksi_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
