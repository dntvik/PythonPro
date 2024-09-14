from flask import jsonify, Blueprint
from webargs.flaskparser import use_args
from webargs import fields
from ..common.database_handler import execute_query

genre_blueprint = Blueprint("stats_by_city", __name__)

query_args = {"genre": fields.Str(missing=None)}


@genre_blueprint.route("/", methods=["GET"])
@use_args(query_args, location="query")
def stats_by_city(args):
    genre = args.get("genre")
    query = """
            WITH RankedCities AS (
                SELECT c.City, COUNT(ii.InvoiceId) AS SalesCount,
                       RANK() OVER (ORDER BY COUNT(ii.InvoiceId) DESC) AS Rank
                FROM customers c
                JOIN invoices i ON c.CustomerId = i.CustomerId
                JOIN invoice_items ii ON i.InvoiceId = ii.InvoiceId
                JOIN tracks t ON ii.TrackId = t.TrackId
                JOIN genres g ON t.GenreId = g.GenreId
                WHERE LOWER(g.Name) = LOWER(?)
                GROUP BY c.City
            )
            SELECT City, SalesCount
            FROM RankedCities
            WHERE Rank = 1;
        """
    result = execute_query(query, (genre,))
    if result:
        cities = [{"city": row[0], "sales_count": row[1]} for row in result]
        return jsonify({"cities": cities, "genre": genre})
    return jsonify({"message": f"Genre '{genre}' not found"}), 404
