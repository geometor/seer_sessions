def analyze_required_actions(input_grid, expected_output, description):
    print(f"\n--- Analysis for {description} ---")
    height = len(input_grid)
    results = []
    color_map = {0: 'W', 3: 'G'}

    for i in range(height):
        if not input_grid[i] or not expected_output[i]: continue # Skip empty/invalid

        input_color = input_grid[i][0]
        expected_color = expected_output[i][0]
        required_action = "Keep" if input_color == expected_color else "Flip"

        # Determine base action (ignoring i=0,1 for now)
        if i < 2:
            base_action = "Keep (Override i=0,1)"
        elif i % 4 == 0 or i % 4 == 1:
            base_action = "Flip (Base i%4=0,1)"
        else: # i%4 == 2 or i%4 == 3
            base_action = "Keep (Base i%4=2,3)"

        is_override = False
        if i >= 2:
             if (base_action.startswith("Flip") and required_action == "Keep") or \
                (base_action.startswith("Keep") and required_action == "Flip"):
                 is_override = True

        results.append({
            "row": i,
            "i%4": i % 4,
            "input": color_map.get(input_color, '?'),
            "expected": color_map.get(expected_color, '?'),
            "required": required_action,
            "base_action": base_action.split(' ')[0], # Just Flip/Keep
            "is_override": is_override
        })

    print(f"Input Colors:    {' '.join([color_map.get(row[0], '?') for row in input_grid if row])}")
    print(f"Expected Colors: {' '.join([color_map.get(row[0], '?') for row in expected_output if row])}")
    print("\nRow Analysis (Required Action vs Base Rule):")
    print("Row | i%4 | In | Exp | Required | Base Act | Override?")
    print("----|-----|----|-----|----------|----------|----------")
    for r in results:
        print(f"{r['row']:<3} | {r['i%4']:<3} | {r['input']:<2} | {r['expected']:<3} | {r['required']:<8} | {r['base_action']:<8} | {'YES' if r['is_override'] else 'No'}")

    overrides = [r for r in results if r['is_override']]
    print("\nOverrides identified:")
    if not overrides:
        print("None")
    else:
        for o in overrides:
             print(f"  Row {o['row']} (i%4={o['i%4']}, In:{o['input']}): Required {o['required']}, Base rule was {o['base_action']}")

    return overrides

# Example 1 Data (Ground Truth)
input_1 = [[0]*3, [0]*3, [0]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [3]*3]
output_1 = [[0]*3, [0]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [0]*3, [3]*3]

# Example 2 Data (Ground Truth from initial prompt)
input_2 = [[0]*3, [0]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3]
output_2_ground_truth = [[0]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3, [3]*3, [3]*3, [0]*3, [3]*3]


print("Analyzing Example 1 (Mode 1: Input[2]=W)...")
overrides_1 = analyze_required_actions(input_1, output_1, "Example 1")

print("\nAnalyzing Example 2 (Mode 2: Input[2]=G)...")
overrides_2 = analyze_required_actions(input_2, output_2_ground_truth, "Example 2")