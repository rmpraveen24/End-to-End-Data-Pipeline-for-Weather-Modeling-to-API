# app.py
from xmlrpc.client import DateTime
from flask import Flask, request,render_template
from flask_restx import Api, Resource, fields
from models import db, Weather, WeatherStats
from config import Config



app = Flask(__name__)
app.config.from_object(Config)

app.config['RESTX_MASK_SWAGGER'] = False

# Initialize extensions
db.init_app(app)

api = Api(app,  version='1.0', title='Weather API',
          description='A simple Weather API',

          )

ns = api.namespace('API', description='Weather Operations')

weather_model = api.model('Weather_Data', {
    'RECORD_ID': fields.String(readOnly=True, description='The unique identifier'),
    'STATION_ID': fields.String(required=True, description='Station ID'),
    'DATE': fields.String(required=True, description='Date in YYYY-MM-DD'),
    'YEAR' :fields.String(required=True, description='Year in YYYY'),
    'MONTH' : fields.String(required=True, description='Month in MM'),
    'DAY' : fields.String(required=True, description='Day in DD'),
    'MAX_TEMP': fields.Float(description='Maximum Temperature'),
    'MIN_TEMP': fields.Float(description='Maximum Temperature'),
    'PRECIPITATION': fields.Float(description='Precipitation'),
})

weather_stats_model = api.model('Weather_Stats', {

    'STATION_ID': fields.String(required=True, description='Station ID'),
    'YEAR': fields.String(required=True, description='Date in YYYY'),
    'AVG_MAX_TEMP': fields.Float(description='Average MAX Temperature'),
    'AVG_MIN_TEMP': fields.Float(description='Average MIN Temperature'),
    'TOTAL_PRECIPITATION': fields.Float(description='Total Precipitation'),
})


## Weather data pagination parser
pagination_parser = api.parser()
pagination_parser.add_argument('DATE', type=str, required=True, help='Filter by date (YYYYMMDD)')
pagination_parser.add_argument('STATION_ID', type=str, required=True, help='Filter by Station ID (ex:USC00336118)')


# WeatherStats pagination parser
weather_stats_pagination_parser = api.parser()
weather_stats_pagination_parser.add_argument('YEAR', type=str, required=True, help='Filter by year (YYYY)')
weather_stats_pagination_parser.add_argument('STATION_ID', type=str, required=True, help='Filter by Station ID (ex:USC00336118)')


@ns.route('/weather')
class WeatherList(Resource):
    @ns.expect(pagination_parser)
    @ns.marshal_list_with(weather_model)
    def get(self):

        args = pagination_parser.parse_args()

        date_str = args.get('DATE')
        station_id = args.get('STATION_ID')

        query = Weather.query
        #print("query:", query)

        if date_str:
            try:

                date_con=str(date_str)
                query = query.filter(Weather.DATE == date_con)
                #print("query:", query)

            except ValueError:
                api.abort(400, "Invalid date format. Use YYYYMMDD.")

        if station_id:
            query = query.filter(Weather.STATION_ID == station_id)
            #print(Weather.STATION_ID)


        result = query.all()

        return result

@ns.route('/weather/stats')
class WeatherStatsList(Resource):
    @ns.expect(weather_stats_pagination_parser)
    @ns.marshal_list_with(weather_stats_model)
    def get(self):

        args = weather_stats_pagination_parser.parse_args()

        date_str = args.get('YEAR')
        station_id = args.get('STATION_ID')

        query = WeatherStats.query

        if date_str:
            try:
                query = query.filter(WeatherStats.YEAR == date_str)

            except ValueError:
                api.abort(400, "Invalid date format. Use YYYY.")

        if station_id:
            query = query.filter(WeatherStats.STATION_ID == station_id)

        result = query.all()
        return result

@api.route('/swagger')
class Swagger(Resource):
    def get(self):
        """Swagger UI"""
        doc = '/swagger/',  # To set the Swagger documentation endpoint


        return api.render_doc()


if __name__ == '__main__':
    app.run(debug=True)
