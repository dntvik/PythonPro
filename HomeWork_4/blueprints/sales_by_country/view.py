from flask import jsonify, request, Blueprint
from ..common.database_handler import execute_query

country_blueprint = Blueprint('sales_by_country', __name__)


@country_blueprint.route('/', methods=['GET'])
def sales_by_country():
    country = request.args.get('country')
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
