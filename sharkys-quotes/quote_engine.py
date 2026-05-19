CART_BASE = {
    "2": 4500,
    "4": 6500,
    "6": 9000
}

PARTS = {
    "lift_kit": {"price": 800, "hours": 2},
    "wheels": {"price": 600, "hours": 1},
    "leds": {"price": 300, "hours": 1}
}

LABOR_RATE = 100


def calculate_quote(cart_type, selected_parts):
    base = CART_BASE[cart_type]

    parts_total = 0
    labor_hours = 0

    breakdown = []

    for part in selected_parts:
        parts_total += PARTS[part]["price"]
        labor_hours += PARTS[part]["hours"]

        breakdown.append({
            "item": part,
            "price": PARTS[part]["price"]
        })

    labor_cost = labor_hours * LABOR_RATE

    total = base + parts_total + labor_cost

    return {
        "base": base,
        "parts_total": parts_total,
        "labor_cost": labor_cost,
        "total": total,
        "breakdown": breakdown
    }