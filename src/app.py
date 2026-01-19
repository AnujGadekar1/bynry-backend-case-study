# app.py
# Sample Flask application used to demonstrate backend design and logic
# for the Bynry Backend Engineering Intern case study.

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration (illustrative only)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sample.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------- Models --------------------

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String(100))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    sku = db.Column(db.String(50))
    low_stock_threshold = db.Column(db.Integer)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)


# -------------------- Helper Functions --------------------

def get_avg_daily_sales(product_id):
    """
    Returns average daily sales for a product.
    Assumed to be precomputed from sales history.
    """
    return 2  # placeholder value


def get_primary_supplier(product_id):
    """
    Returns supplier details for a product.
    """
    return {
        "id": 1,
        "name": "Supplier Corp",
        "contact_email": "orders@supplier.com"
    }


# -------------------- API Endpoint --------------------

@app.route("/api/companies/<int:company_id>/alerts/low-stock", methods=["GET"])
def low_stock_alerts(company_id):
    alerts = []

    # Fetch inventory records for all warehouses belonging to the company
    inventories = Inventory.query.all()

    for inv in inventories:
        # Determine product-specific low stock threshold
        product = Product.query.get(inv.product_id)
        threshold = product.low_stock_threshold

        # Skip products that are sufficiently stocked
        if inv.quantity >= threshold:
            continue

        # Calculate average daily sales to estimate stock-out timeline
        avg_daily_sales = get_avg_daily_sales(product.id)
        if avg_daily_sales == 0:
            continue  # Avoid division by zero and irrelevant alerts

        days_until_stockout = inv.quantity // avg_daily_sales
        supplier = get_primary_supplier(product.id)

        alerts.append({
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "warehouse_id": inv.warehouse_id,
            "current_stock": inv.quantity,
            "threshold": threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": supplier
        })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })


if __name__ == "__main__":
    app.run(debug=True)
