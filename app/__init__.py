from flask import Flask, render_template, jsonify, request
from .core import create_default_captcha_image, generate_captcha_code, draw_captcha_on_image
import io
import base64
import hashlib
import traceback
from .limiter import api_limiter


app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Captcha image generator"
    )


@app.route("/api/example")
def api_example():
    return render_template(
        "api_examples/f1.html"
    )


@app.route("/api", methods=['POST'])
@api_limiter
def captcha_image_generator_api():
    try:
        image = create_default_captcha_image()
        captcha_code = generate_captcha_code()
        draw_captcha_on_image(captcha_code, image)

        io_bytes = io.BytesIO()
        image.save(io_bytes, "png")

    except Exception as e:
        print("="*100)
        print(traceback.format_exc())
        print("="*100)

        return {
            "status": "error"
        }, 500

    response = jsonify({
        "status": "ok",
        "image": base64.b64encode(io_bytes.getvalue()).decode("utf-8"),
        "captcha_hash": hashlib.sha256(captcha_code.encode()).hexdigest()
    })

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
