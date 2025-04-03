import numpy as np

# Helper functions from previous attempt (slightly adapted for clarity)
def find_colored_block(row):
    """Finds the first contiguous block of non-white, non-maroon color in a single row."""
    block_color = -1
    block_start = -1
    block_end = -1
    in_block = False
    for i, pixel in enumerate(row):
        if pixel != 0 and pixel != 9:
            if not in_block:
                block_start = i
                block_color = pixel
                in_block = True
            # Check if the block continues or ends
            if i + 1 == len(row) or row[i+1] != block_color:
                block_end = i
                break # Found the end of the block
    if block_start != -1:
        block_length = block_end - block_start + 1
        return {'color': block_color, 'start': block_start, 'end': block_end, 'length': block_length}
    else:
        return None

def find_marker_pixel(row, marker_color=9):
    """Finds the index of the first pixel with the marker_color in a single row."""
    for i, pixel in enumerate(row):
        if pixel == marker_color:
            return i
    return -1

# --- Example Data ---
train_examples = [
    {
        "input":  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]]
    },
    {
        "input":  [[0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input":  [[5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0]]
    }
]

# --- Metric Calculation ---
metrics = []
for i, ex in enumerate(train_examples):
    input_row = ex["input"][0]
    output_row = ex["output"][0]
    grid_len = len(input_row)

    block_info = find_colored_block(input_row)
    marker_index_in = find_marker_pixel(input_row)
    gap_size = -1
    if block_info and marker_index_in != -1:
         # Assumes block is before marker in input
        gap_size = marker_index_in - block_info['end'] - 1

    # Find marker index in output for verification
    marker_index_out = find_marker_pixel(output_row)

    metrics.append({
        "example": i + 1,
        "grid_length": grid_len,
        "block_info (input)": block_info,
        "marker_index (input)": marker_index_in,
        "gap_size (input)": gap_size,
        "marker_index (output)": marker_index_out,
    })

# --- Print Metrics ---
import json
print(json.dumps(metrics, indent=2))