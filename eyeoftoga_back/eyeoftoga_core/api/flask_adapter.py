# nexshop_sdk/api/flask_adapter.py

from flask import Flask, jsonify

# Função para criar a aplicação Flask
def create_flask_app():
    app = Flask(__name__)

    @app.route("/healthcheck", methods=["GET"])
    def healthcheck():
        """
        Endpoint de verificação de saúde.
        """
        return jsonify({"status": "ok", "framework": "Flask"}), 200

    return app


# Apenas para execução local, use `python -m nexshop_sdk.api.flask_adapter`
if __name__ == "__main__":
    app = create_flask_app()
    app.run(host="0.0.0.0", port=5000)
