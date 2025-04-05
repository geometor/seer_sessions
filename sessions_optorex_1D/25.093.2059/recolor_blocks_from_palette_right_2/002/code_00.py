# Common function to find blocks
def find_contiguous_blocks(sequence: list[int], target_value: int) -> list[tuple[int, int]]:
    blocks = []
    n = len(sequence)
    i = 0
    while i < n:
        if sequence[i] == target_value:
            start_index = i
            length = 0
            while i < n and sequence[i] == target_value:
                length += 1
                i += 1
            blocks.append((start_index, length))
        else:
            i += 1
    return blocks

# Example Data
examples = [
    {"id": 1, "input": [9, 7, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0], "output": [9, 7, 0, 0, 9, 9, 9, 0, 7, 7, 7, 0]},
    {"id": 2, "input": [6, 7, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5], "output": [6, 7, 0, 0, 0, 6, 6, 6, 0, 7, 7, 7]},
    {"id": 3, "input": [2, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0], "output": [2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0]},
    {"id": 4, "input": [1, 3, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0], "output": [1, 3, 0, 1, 1, 0, 0, 3, 3, 0, 0, 0]},
    {"id": 5, "input": [3, 2, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0], "output": [3, 2, 0, 0, 0, 0, 3, 3, 0, 2, 2, 0]},
    {"id": 6, "input": [2, 7, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5], "output": [2, 7, 0, 0, 0, 2, 2, 2, 0, 7, 7, 7]},
    {"id": 7, "input": [3, 7, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5], "output": [3, 7, 0, 0, 0, 3, 3, 3, 0, 7, 7, 7]},
]

target_digit = 5
metrics = []

for ex in examples:
    input_list = ex["input"]
    key1 = input_list[0] if len(input_list) > 0 else None
    key2 = input_list[1] if len(input_list) > 1 else None
    blocks = find_contiguous_blocks(input_list, target_digit)
    
    simulated_output = list(input_list) # Start with a copy
    
    if len(blocks) >= 1:
        start_index, length = blocks[0]
        for i in range(start_index, start_index + length):
            if i < len(simulated_output):
                simulated_output[i] = key1
                
    if len(blocks) >= 2:
        start_index, length = blocks[1]
        for i in range(start_index, start_index + length):
            if i < len(simulated_output):
                simulated_output[i] = key2
                
    metrics.append({
        "id": ex["id"],
        "key1": key1,
        "key2": key2,
        "target_blocks": blocks,
        "block_count": len(blocks),
        "simulated_output_matches_expected": simulated_output == ex["output"]
    })

# Print the collected metrics
import json
print(json.dumps(metrics, indent=2))