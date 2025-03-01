import numpy as np

def show(grid, msg=None):
    if msg: print(msg)
    for row in grid:
        row_str = ''.join(str(cell) for cell in row)
        print(row_str)

# Example Data (replace with actual data from the task)
train_pairs = [
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 0, 0],
            [0, 5, 5, 5, 0, 0, 0],
            [0, 5, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 5],
            [0, 0, 0, 0, 0, 5, 5],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 0, 0],
            [0, 5, 3, 5, 0, 0, 0],
            [0, 5, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 5],
            [0, 0, 0, 0, 0, 5, 9],
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 5, 5, 5, 3, 5, 5, 5, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]),
    }
]
# add the functions from the Previous Code here
# ... (find_objects, get_quadrant, find_internal_pixels, transform) ...
# NOTE - find_internal_pixels has been changed
def find_internal_pixels(object_pixels):
    if len(object_pixels) <= 2:
      return object_pixels
    
    # Find the bounding box
    min_row = min(r for r, c in object_pixels)
    max_row = max(r for r, c in object_pixels)
    min_col = min(c for r, c in object_pixels)
    max_col = max(c for r, c in object_pixels)
    
    internal_pixels = []
    for row, col in object_pixels:
        # check the 8 neighbors and see if at least 3 are the same color
        neighbor_count = 0
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if (r,c) == (row, col): continue # skip center pixel
                if (r,c) in object_pixels:
                    neighbor_count += 1
        if neighbor_count >= 3:
            internal_pixels.append((row,col))

    return internal_pixels
for i, pair in enumerate(train_pairs):
    input_grid = pair['input']
    expected_output = pair['output']
    actual_output = transform(input_grid)
    
    print(f"--- Example {i+1} ---")
    show(input_grid, "Input")
    show(expected_output, "Expected Output")
    show(actual_output, "Actual Output")

    correct_pixels = np.sum(actual_output == expected_output)
    total_pixels = actual_output.size
    accuracy = correct_pixels / total_pixels
    print(f"Pixel Accuracy: {accuracy:.4f}")
    print()