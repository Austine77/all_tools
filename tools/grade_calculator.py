def calculate_grade(data):
    total = 0
    weight_sum = 0
    for item in data:
        total += item["score"] * item["weight"]
        weight_sum += item["weight"]
    final = total / weight_sum if weight_sum else 0
    return {"final_grade": round(final, 2)}
