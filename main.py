# delivery_api.py
from flask import Flask, request, jsonify
from itertools import permutations

app = Flask(__name__)

# Each product weighs 0.5 kg
PRODUCT_WEIGHT = 0.5

WAREHOUSE_PRODUCTS = {
    "C1": ["A", "B", "C"],
    "C2": ["D", "E", "F"],
    "C3": ["G", "H", "I"]
}

COST_MATRIX = {
    "C1": {"L1": 10, "C2": 15, "C3": 20},
    "C2": {"L1": 12, "C1": 15, "C3": 18},
    "C3": {"L1": 8, "C1": 20, "C2": 18}
}

def get_centers_required(order):
    centers = set()
    for product, quantity in order.items():
        for center, items in WAREHOUSE_PRODUCTS.items():
            if product in items:
                centers.add(center)
    return list(centers)

def get_weight_for_center(center, order):
    items = WAREHOUSE_PRODUCTS[center]
    return sum(order.get(item, 0) for item in items) * PRODUCT_WEIGHT

def calculate_cost(path, order):
    cost = 0
    current = path[0]
    for next_stop in path[1:]:
        weight = get_weight_for_center(current, order)
        cost += COST_MATRIX[current][next_stop] * weight
        current = next_stop
    return cost

@app.route("/calculate-cost", methods=["POST"])
def calculate_min_cost():
    order = request.json
    centers = get_centers_required(order)
    min_cost = float("inf")

    for starting_center in centers:
        other_centers = [c for c in centers if c != starting_center]
        for perm in permutations(other_centers):
            path = [starting_center]
            for c in perm:
                path += ["L1", c]
            path.append("L1")
            cost = calculate_cost(path, order)
            min_cost = min(min_cost, cost)

    return jsonify({"minimum_cost": round(min_cost)})

if __name__ == "__main__":
    app.run(debug=True)
