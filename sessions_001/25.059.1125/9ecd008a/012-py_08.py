import numpy as np

train_pairs = [
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]]), np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]])),
    (np.array([[8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [5, 5, 5, 8, 8, 8, 5, 5, 5], [5, 5, 5, 8, 8, 8, 5, 5, 5], [5, 5, 5, 8, 8, 8, 5, 5, 5]]), np.array([[8, 8, 5], [8, 8, 5], [5, 8, 5]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 1, 1, 8, 8, 8, 8, 8, 8], [8, 1, 1, 8, 8, 8, 8, 8, 8], [8, 1, 1, 8, 8, 8, 8, 8, 8]]), np.array([[8, 8, 8], [8, 8, 8], [8, 1, 8]]))
]

def get_block(grid, row, col):
    start_row = row * 3
    start_col = col * 3
    return grid[start_row:start_row+3, start_col:start_col+3]

for i, (input_grid, expected_output) in enumerate(train_pairs):
    print(f"Example {i+1}:")
    print(f"Input shape: {input_grid.shape}")
    print(f"Output shape: {expected_output.shape}")
    for row in range(3):
        for col in range(3):
            input_block = get_block(input_grid, row, col)
            output_pixel = expected_output[row, col]
            unique, counts = np.unique(input_block, return_counts=True)
            most_frequent = unique[np.argmax(counts)]
            print(f"  Block ({row}, {col}):")
            print(f"    Input block:\n{input_block}")
            print(f"    Output pixel: {output_pixel}")
            print(f"    Most frequent color in block: {most_frequent}")
            print(f"    Output pixel == Most frequent: {output_pixel == most_frequent}")
