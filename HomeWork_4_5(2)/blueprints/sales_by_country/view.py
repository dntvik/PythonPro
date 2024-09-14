from flask import jsonify, Blueprint
from webargs.flaskparser import use_args
from webargs import fields
from ..common.database_handler import execute_query

country_blueprint = Blueprint("sales_by_country", __name__)

query_args = {"country": fields.Str(missing=None)}


@country_blueprint.route("/", methods=["GET"])
@use_args(query_args, location="query")
def sales_by_country(args):
    country = args.get("country")
    try:
        if country:
            query = """
            SELECT i.BillingCountry, SUM(ii.UnitPrice * ii.Quantity) as TotalSales
            FROM invoices i
            INNER JOIN invoice_items ii ON i.InvoiceId = ii.InvoiceId
            WHERE UPPER(i.BillingCountry) = UPPER(?)
            GROUP BY i.BillingCountry
            ORDER BY TotalSales DESC;
            """
            sales = execute_query(query, (country,))
        else:
            query = """
            SELECT i.BillingCountry, SUM(ii.UnitPrice * ii.Quantity) as TotalSales
            FROM invoices i
            INNER JOIN invoice_items ii ON i.InvoiceId = ii.InvoiceId
            GROUP BY i.BillingCountry
            ORDER BY TotalSales DESC;
            """
            sales = execute_query(query)

        sales_list = [{"country": row[0], "total_sales": row[1]} for row in sales]
        return jsonify(sales_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
