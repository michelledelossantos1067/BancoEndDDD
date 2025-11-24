from flask import Flask
from flask_cors import CORS
from app.database.config import init_db
from app.controllers.account_controller import account_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(account_bp, url_prefix='/api')

@app.route('/')
def home():
    return {"message": "Bank System API", "version": "0.2.0"}, 200

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)