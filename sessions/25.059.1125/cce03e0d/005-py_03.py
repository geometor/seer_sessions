import numpy as np

def get_grid_info(in_grid, out_grid):
    in_h, in_w = in_grid.shape
    out_h, out_w = out_grid.shape
    
    # Find top-left corner of input within output
    top_left_row = -1
    top_left_col = -1

    for r in range(out_h - in_h + 1):
        for c in range(out_w - in_w + 1):
            if np.array_equal(out_grid[r:r+in_h, c:c+in_w], in_grid):
                top_left_row = r
                top_left_col = c
                break  # Stop after finding the first match
        if top_left_row != -1:
            break

    return {
        'input_shape': (in_h, in_w),
        'output_shape': (out_h, out_w),
        'top_left_corner': (top_left_row, top_left_col)
    }

# Example Usage with the provided data (assuming it's stored in a suitable format)
# Let's create dummy data since the exact grids are in image format, which I can't process directly.
# The structure mimics what I expect from the image-based ARC data.
train_examples = [
    (np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), np.array([[1, 2, 3, 0, 0, 0, 0, 0, 0], [4, 5, 6, 0, 0, 0, 0, 0, 0], [7, 8, 9, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])),
    (np.array([[5, 1], [8, 3]]), np.array([[0, 0, 0, 0, 0, 0], [0, 0, 5, 1, 0, 0], [0, 0, 8, 3, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])),
    (np.array([[7, 2, 7], [7, 7, 2]]), np.array([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 2, 7, 0], [0, 0, 0, 7, 7, 2, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])),
    (np.array([[1, 2, 3, 4]]), np.array([[0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 3, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])),
    (np.array([[4, 4], [4, 4], [4, 4]]), np.array([[0, 0, 0, 0, 0, 0], [0, 4, 4, 0, 0, 0], [0, 4, 4, 0, 0, 0], [0, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
]

results = [get_grid_info(in_grid, out_grid) for in_grid, out_grid in train_examples]
for i, r in enumerate(results):
    print (f"Example {i+1}: {r}")