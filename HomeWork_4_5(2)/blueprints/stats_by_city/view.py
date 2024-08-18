from flask import jsonify, Blueprint
from webargs.flaskparser import use_args
from webargs import fields
from ..common.database_handler import execute_query

genre_blueprint = Blueprint('stats_by_city', __name__)

query_args = {'genre': fields.Str(missing=None)}

@genre_blueprint.route('/', methods=['GET'])
@use_args(query_args, location='query')
def stats_by_city(args):
    genre = args.get('genre')
    query = """
            SELECT c.City, COUNT(ii.InvoiceId) AS SalesCount
            FROM customers c
            JOIN invoices i ON c.CustomerId = i.CustomerId
            JOIN invoice_items ii ON i.InvoiceId = ii.InvoiceId
            JOIN tracks t ON ii.TrackId = t.TrackId
            JOIN genres g ON t.GenreId = g.GenreId
            WHERE LOWER(g.Name) = LOWER(?)
            GROUP BY c.City
            ORDER BY SalesCount DESC
            LIMIT 1;
        """
    result = execute_query(query, (genre,))
    if result:
        city = result[0][0]
        return jsonify({"city": city, "genre": genre})
    return jsonify({"message": f"Genre '{genre}' not found"}), 404
