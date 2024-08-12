from flask import Flask
from blueprints.sales_by_country.view import country_blueprint
from blueprints.track_info.view import track_blueprint
from blueprints.track_info.view import tracks_blueprint
app = Flask(__name__)


app.register_blueprint(country_blueprint, url_prefix='/sales_by_country')
app.register_blueprint(track_blueprint, url_prefix='/track_info')
app.register_blueprint(tracks_blueprint, url_prefix='/all_tracks_duration')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
