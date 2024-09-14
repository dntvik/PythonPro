from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from webargs import fields
from ..common.database_handler import execute_query

track_blueprint = Blueprint("track_info", __name__)

tracks_blueprint = Blueprint("all_tracks_duration", __name__)


def get_all_info_about_track(track_id):
    query = """
    SELECT
        t.TrackId,
        t.Name as TrackName,
        t.Composer,
        t.Milliseconds,
        t.Bytes,
        t.UnitPrice,
        a.Title as AlbumTitle,
        ar.Name as ArtistName,
        g.Name as Genre,
        mt.Name as MediaType,
        COALESCE(SUM(ii.Quantity), 0) as TotalSales
    FROM tracks t
    JOIN albums a ON t.AlbumId = a.AlbumId
    JOIN artists ar ON a.ArtistId = ar.ArtistId
    JOIN genres g ON t.GenreId = g.GenreId
    JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId
    LEFT JOIN invoice_items ii ON t.TrackId = ii.TrackId
    WHERE t.TrackId = ?
    GROUP BY t.TrackId, t.Name, t.Composer, t.Milliseconds, t.Bytes, t.UnitPrice, a.Title, ar.Name, g.Name, mt.Name
    """
    return execute_query(query, (track_id,))


query_args = {"track_id": fields.Int(required=True)}


@track_blueprint.route("/", methods=["GET"])
@use_args(query_args, location="query")
def track_info(args):
    track_id = args.get("track_id")
    track_details = get_all_info_about_track(track_id)
    if track_details:
        track_info_dict = {
            "track_id": track_details[0][0],
            "track_name": track_details[0][1],
            "composer": track_details[0][2],
            "duration_ms": track_details[0][3],
            "size_bytes": track_details[0][4],
            "unit_price": track_details[0][5],
            "album_title": track_details[0][6],
            "artist_name": track_details[0][7],
            "genre": track_details[0][8],
            "media_type": track_details[0][9],
            "total_sales": track_details[0][10],
        }
        return jsonify(track_info_dict)
    return jsonify({"error": "Track not found"}), 404


@tracks_blueprint.route("/", methods=["GET"])
def all_track_info():
    query = """
    SELECT SUM(t.Milliseconds) as TotalDurationMs
    FROM tracks t
    """
    result = execute_query(query)
    if result and result[0]:
        total_duration_ms = result[0][0]
        total_duration_hours = total_duration_ms / (1000 * 60 * 60)
        return jsonify({"total_duration_hours": total_duration_hours})
    return jsonify({"total_duration_hours": 0})
