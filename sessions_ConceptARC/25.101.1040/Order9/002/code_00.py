import collections

def analyze_example(input_grid, expected_output, description):
    print(f"\n--- Analysis for {description} ---")
    height = len(input_grid)
    base_rule_output = []
    discrepancies = []

    for i in range(height):
        input_color = input_grid[i][0]
        # Base rule: Flip if i%4=0 or 1, Keep if i%4=2 or 3
        if i % 4 == 0 or i % 4 == 1:
            predicted_color = 3 - input_color # Flip
            action = "Flip"
        else:
            predicted_color = input_color # Keep
            action = "Keep"

        base_rule_output.append([predicted_color] * 3) # Assuming width 3
        expected_color = expected_output[i][0]

        if predicted_color != expected_color:
            discrepancies.append({
                "row": i,
                "i%4": i % 4,
                "input": input_color,
                "base_rule_action": action,
                "predicted_color": predicted_color,
                "expected_color": expected_color,
                "actual_action": "Keep" if input_color == expected_color else "Flip"
            })

    print(f"Input Colors:  {[row[0] for row in input_grid]}")
    print(f"Expected Colors: {[row[0] for row in expected_output]}")
    print(f"Base Rule Pred:  {[row[0] for row in base_rule_output]}")
    print("\nDiscrepancies (Base Rule vs Expected):")
    if not discrepancies:
        print("None")
    else:
        for d in discrepancies:
            print(f"  Row {d['row']} (i%4={d['i%4']}, In:{d['input']}): Base rule predicted {d['base_rule_action']} -> {d['predicted_color']}, but Expected is {d['expected_color']} (Actual Action: {d['actual_action']})")
    return discrepancies

# Example 1 Data
input_1 = [[0]*3, [0]*3, [0]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [3]*3]
output_1 = [[0]*3, [0]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [0]*3, [3]*3]

# Example 2 Data
input_2 = [[0]*3, [0]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3]
output_2 = [[0]*3, [0]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [0]*3, [0]*3, [0]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [0]*3, [0]*3]

disc1 = analyze_example(input_1, output_1, "Example 1")
disc2 = analyze_example(input_2, output_2, "Example 2")
