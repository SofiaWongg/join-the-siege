from flask import Flask, request, jsonify
from src.api.routes import api
import logging
from src.config import config


def create_app():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Starting app")
    app = Flask(__name__)

    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

    app.register_blueprint(api)
    logging.info("App created")
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
