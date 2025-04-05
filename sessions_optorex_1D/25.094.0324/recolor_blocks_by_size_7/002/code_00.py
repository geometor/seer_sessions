# Helper function logic (adapted for list input)
def find_groups_of_3(numbers):
    groups = []
    in_group = False
    start_index = -1
    for i, num in enumerate(numbers):
        if num == 3 and not in_group:
            in_group = True
            start_index = i
        elif num != 3 and in_group:
            groups.append({'start': start_index, 'end': i - 1, 'length': i - start_index})
            in_group = False
            start_index = -1
    if in_group:
        groups.append({'start': start_index, 'end': len(numbers) - 1, 'length': len(numbers) - start_index})
    return groups

# Data for analysis
examples = [
    {"input": [0, 3, 3, 3, 3, 0, 3, 3, 3, 0, 0, 0], "output": [0, 1, 1, 1, 1, 0, 2, 2, 2, 0, 0, 0]},
    {"input": [0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3], "output": [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 2]},
    {"input": [3, 3, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0], "output": [2, 2, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0]},
    {"input": [0, 0, 0, 3, 3, 3, 0, 3, 3, 0, 0, 0], "output": [0, 0, 0, 1, 1, 1, 0, 2, 2, 0, 0, 0]},
    {"input": [3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3], "output": [2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1]},
    {"input": [0, 0, 0, 3, 3, 3, 0, 3, 3, 3, 3, 3], "output": [0, 0, 0, 2, 2, 2, 0, 1, 1, 1, 1, 1]},
    {"input": [0, 0, 0, 3, 3, 0, 0, 3, 3, 3, 3, 0], "output": [0, 0, 0, 2, 2, 0, 0, 1, 1, 1, 1, 0]},
]

print("Example | Groups Found | G1 Len | G2 Len | Initial Val | Logic Matches Output")
print("--------|--------------|--------|--------|-------------|--------------------")
for i, ex in enumerate(examples):
    input_list = ex["input"]
    output_list = ex["output"]
    groups = find_groups_of_3(input_list)

    if not groups:
        initial_value = 'N/A'
        g1_len = 'N/A'
        g2_len = 'N/A'
        logic_result = list(input_list) # If no groups, output is same as input
    else:
        g1_len = groups[0]['length']
        if len(groups) == 1:
            initial_value = 1
            g2_len = 'N/A'
        else:
            g2_len = groups[1]['length']
            if g1_len > g2_len:
                initial_value = 1
            else: # g1_len <= g2_len
                initial_value = 2

        # Simulate transformation
        logic_result = list(input_list)
        current_value = initial_value
        for group in groups:
            for j in range(group['start'], group['end'] + 1):
                logic_result[j] = current_value
            current_value = 3 - current_value # Alternate

    match = (logic_result == output_list)
    print(f"   {i+1}    | {len(groups):<12} | {str(g1_len):<6} | {str(g2_len):<6} | {str(initial_value):<11} | {match}")
