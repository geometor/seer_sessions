# tool_code
import numpy as np
import json

# Function to convert numpy types to Python types for JSON serialization
def np_converter(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    # Add other types if necessary
    #raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
    return obj # Return object itself if not a numpy type we handle

def find_contiguous_non_zero_block_bounds(arr):
    """Finds the start and end indices of the first contiguous block of non-zero numbers."""
    non_zero_indices = np.nonzero(arr)[0]
    if len(non_zero_indices) == 0:
        return -1, -1
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    return start_index, end_index

def analyze_example(input_str, output_str):
    input_list = [int(x) for x in input_str.split()]
    input_grid = np.array(input_list)
    n = len(input_list)
    start_index, end_index = find_contiguous_non_zero_block_bounds(input_grid)

    if start_index == -1:
        actual_output_start = -1 # Assume output is all zeros too
        block_len = 0
    else:
        non_zero_block = input_grid[start_index : end_index + 1]
        block_len = len(non_zero_block)
        # Determine the actual start index from the expected output
        output_list = [int(x) for x in output_str.split()]
        output_grid = np.array(output_list)
        actual_output_start, _ = find_contiguous_non_zero_block_bounds(output_grid)
        if actual_output_start == -1 and block_len > 0: # Handle case where output is unexpectedly all zeros
             pass # Or log a warning

    calculated_new_start = max(0, start_index - 3) if start_index != -1 else -1

    result_dict = {
        "input": input_str,
        "input_start_index": start_index,
        "input_end_index": end_index,
        "block_len": block_len,
        "calculated_new_start": calculated_new_start,
        "actual_output_start": actual_output_start,
        "rule_match": calculated_new_start == actual_output_start
    }
    # Convert numpy types within the dictionary
    for key, value in result_dict.items():
        result_dict[key] = np_converter(value)

    return result_dict


train_inputs = [
    "0 0 0 0 0 0 0 7 3 8 3 0",
    "0 0 0 0 0 0 0 9 9 9 6 0",
    "0 0 0 7 8 1 3 2 2 7 5 0",
    "0 0 0 4 2 8 6 7 3 5 0 0",
    "0 0 0 0 0 0 0 0 6 3 1 1",
    "0 0 0 7 4 1 9 6 3 7 0 0",
    "0 0 0 0 0 2 6 1 7 5 0 0",
]

train_outputs = [
    "0 0 0 0 7 3 8 3 0 0 0 0",
    "0 0 0 0 9 9 9 6 0 0 0 0",
    "7 8 1 3 2 2 7 5 0 0 0 0",
    "4 2 8 6 7 3 5 0 0 0 0 0",
    "0 0 0 0 0 6 3 1 1 0 0 0",
    "7 4 1 9 6 3 7 0 0 0 0 0",
    "0 0 2 6 1 7 5 0 0 0 0 0",
]

results = []
for i, input_str in enumerate(train_inputs):
    analysis = analyze_example(input_str, train_outputs[i])
    results.append(analysis)

print(json.dumps(results, indent=2))
