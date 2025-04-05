# Tool Code Snippet (Conceptual - full code run previously)
import numpy as np

def find_block_properties(grid_list):
    grid_arr = np.array(grid_list).flatten()
    non_zero_indices = np.where(grid_arr != 0)[0]
    if len(non_zero_indices) == 0: return None, -1, 0
    start_index = non_zero_indices[0]
    value = grid_arr[start_index]
    length = 0
    for i in range(len(non_zero_indices)):
        current_index = non_zero_indices[i]
        if current_index == start_index + i and grid_arr[current_index] == value:
            length += 1
        else: break
    return int(value), int(start_index), int(length)

def analyze_example(input_grid, output_grid):
    block_value, start_index, block_length = find_block_properties(input_grid)
    if block_value is None: return {"error": "No block found"}
    shift_distance = block_length
    expected_new_start = start_index + shift_distance
    output_block_value, output_start_index, output_block_length = find_block_properties(output_grid)
    actual_new_start = output_start_index if output_block_value is not None else -1
    return {
        "input_block_value": block_value, "input_block_start": start_index,
        "input_block_length": block_length, "calculated_shift": shift_distance,
        "expected_output_start": expected_new_start, "actual_output_start": actual_new_start,
        "matches_expectation": (block_value == output_block_value and
                                block_length == output_block_length and
                                expected_new_start == actual_new_start)
    }
# ... (Loop through examples) ...