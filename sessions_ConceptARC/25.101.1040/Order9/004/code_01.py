import collections # Not strictly needed here, but good practice

def analyze_required_actions(input_grid, expected_output, description):
    print(f"\n--- Analysis for {description} ---")
    height = len(input_grid)
    results = []
    color_map = {0: 'W', 3: 'G'}

    for i in range(height):
        # Basic validation for row existence and content
        if i >= len(input_grid) or not input_grid[i] or \
           i >= len(expected_output) or not expected_output[i]:
            print(f"Warning: Skipping row {i} due to missing/empty data in input or expected output.")
            continue

        input_color = input_grid[i][0]
        expected_color = expected_output[i][0]
        required_action = "Keep" if input_color == expected_color else "Flip"

        # Determine base action (explicitly handle i=0,1 override)
        if i == 0 or i == 1:
            base_action_desc = "Keep (Override i=0,1)"
            base_action = "Keep"
        elif i % 4 == 0 or i % 4 == 1:
            base_action_desc = "Flip (Base i%4=0,1)"
            base_action = "Flip"
        else: # i%4 == 2 or i%4 == 3
            base_action_desc = "Keep (Base i%4=2,3)"
            base_action = "Keep"

        is_override = False
        # Override detection only applies for i >= 2, as i=0,1 have their own fixed rule
        if i >= 2:
             if base_action != required_action:
                 is_override = True

        results.append({
            "row": i,
            "i%4": i % 4,
            "input": color_map.get(input_color, '?'),
            "expected": color_map.get(expected_color, '?'),
            "required": required_action,
            "base_action": base_action, # Just Flip/Keep
            "is_override": is_override
        })

    print(f"Input Colors:    {' '.join([color_map.get(row[0], '?') for row in input_grid if row])}")
    print(f"Expected Colors: {' '.join([color_map.get(row[0], '?') for row in expected_output if row])}")
    print("\nRow Analysis (Required Action vs Base Rule for i>=2):")
    print("Row | i%4 | In | Exp | Required | Base Act | Override?")
    print("----|-----|----|-----|----------|----------|----------")
    for r in results:
        # For i=0,1, base action is fixed Keep, so no override check needed vs i%4 base
        override_display = 'YES' if r['is_override'] else ('n/a' if r['row']<2 else 'No')
        print(f"{r['row']:<3} | {r['i%4']:<3} | {r['input']:<2} | {r['expected']:<3} | {r['required']:<8} | {r['base_action']:<8} | {override_display}")

    overrides = [r for r in results if r['is_override']]
    print("\nOverrides identified (for i >= 2):")
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