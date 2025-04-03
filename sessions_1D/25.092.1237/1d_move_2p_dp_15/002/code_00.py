import numpy as np

# --- Function definitions (find_movable_block, find_anchor_pixel, transform - modified version prioritizing anchor) ---
def find_movable_block(grid):
    start_index = -1
    color = -1
    length = 0
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 7:
            if start_index == -1:
                start_index = i
                color = pixel
                length = 1
            elif pixel == color:
                length += 1
            else: # Found a different color block, should not happen based on problem description
                break # Stop searching if block ends or changes color unexpectedly
        elif start_index != -1: # We were tracking a block, and it just ended
            break
    if start_index != -1:
        # Ensure color is a standard int, not np.int64
        return start_index, int(color), length
    else:
        return None, None, None

def find_anchor_pixel(grid):
    for i, pixel in enumerate(grid):
        if pixel == 7:
            return i
    return -1 # Should not happen based on problem description

def transform(input_grid):
    input_grid_np = np.array(input_grid)
    grid_size = len(input_grid_np)
    output_grid = np.zeros(grid_size, dtype=int) # Start with white background

    block_start, block_color, block_length = find_movable_block(input_grid_np)
    anchor_index = find_anchor_pixel(input_grid_np)

    # Calculate the new starting index for the movable block
    if block_start is not None:
        new_block_start = block_start + 2
        # Ensure the block doesn't go out of bounds
        end_index = min(new_block_start + block_length, grid_size)
        # Place the movable block in the output grid at the new position using slicing
        if new_block_start < grid_size: # Make sure start index is within bounds
            output_grid[new_block_start:end_index] = block_color

    # Place the anchor pixel in the output grid, potentially overwriting the block
    if anchor_index != -1:
        output_grid[anchor_index] = 7

    return output_grid.tolist() # Return standard list

# --- Test cases ---
train_inputs = [
    [1, 1, 1, 1, 0, 0, 7, 0, 0, 0, 0, 0],
    [8, 8, 8, 8, 8, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 5, 5, 5, 5, 0, 0, 7, 0, 0]
]

train_outputs = [
    [0, 0, 1, 1, 1, 1, 7, 0, 0, 0, 0, 0],
    [0, 0, 8, 8, 8, 8, 8, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 5, 5, 5, 7, 0, 0]
]

results_summary = []
for i, (inp, expected_out) in enumerate(zip(train_inputs, train_outputs)):
    start_index, color, length = find_movable_block(np.array(inp))
    anchor_index = find_anchor_pixel(np.array(inp))
    new_start_index = start_index + 2 if start_index is not None else None
    actual_out = transform(inp)
    is_correct = actual_out == expected_out

    results_summary.append({
        "example": i + 1,
        "input_len": len(inp),
        "output_len": len(actual_out),
        "block_start": start_index,
        "block_color": color,
        "block_length": length,
        "anchor_index": anchor_index,
        "new_block_start": new_start_index,
        "correct": is_correct
    })

print(results_summary)