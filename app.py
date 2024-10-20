from flask import Flask
from api.get_profile import get_profile_bp
from api.process_image_bottle import process_image_bottle_bp
from api.process_image_can import process_image_can_bp
from api.calculate_bottle_points import calculate_bottle_points_bp
from api.calculate_can_points import calculate_can_points_bp
from api.accumulate_points import accumulate_points_bp
from api.donate import donate_bp
from api.activate import activate_bp
from api.heartbeat import heartbeat_bp

app = Flask(__name__)

# Register each API's blueprint
app.register_blueprint(get_profile_bp)
# app.register_blueprint(process_image_bottle_bp)
# app.register_blueprint(process_image_can_bp)
app.register_blueprint(calculate_bottle_points_bp)
app.register_blueprint(calculate_can_points_bp)
app.register_blueprint(accumulate_points_bp)
app.register_blueprint(donate_bp)
app.register_blueprint(activate_bp)
app.register_blueprint(heartbeat_bp)

if __name__ == '__main__':
    app.run(port=5005)
