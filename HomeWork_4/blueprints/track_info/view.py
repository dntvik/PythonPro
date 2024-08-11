from flask import Blueprint, request, jsonify
from ..common.database_handler import execute_query

track_blueprint = Blueprint('track_info', __name__)


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
        mt.Name as MediaType
    FROM tracks t
    JOIN albums a ON t.AlbumId = a.AlbumId
    JOIN artists ar ON a.ArtistId = ar.ArtistId
    JOIN genres g ON t.GenreId = g.GenreId
    JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId
    WHERE t.TrackId = ?
    """
    return execute_query(query, (track_id,))


@track_blueprint.route('/', methods=['GET'])
def track_info():
    track_id = request.args.get('track_id')
    if track_id:
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
                "media_type": track_details[0][9]
            }
            return jsonify(track_info_dict)
        return jsonify({"error": "Track not found"}), 404
    return jsonify({"error": "Track ID not provided"}), 400
