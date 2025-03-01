import numpy as np

def analyze_example(input_grid, output_grid):
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)
    print(f"Input shape: {input_array.shape}")
    print(f"Output shape: {output_array.shape}")
    print(f"Input:\n{input_array}")
    print(f"Output:\n{output_array}")

    rows, cols = input_array.shape

    corners = [
        input_array[0,0],
        input_array[0,cols-1],
        input_array[rows-1, cols-1],
        input_array[rows-1, 0]
    ]
    print(f"Corners: {corners}")

example_pairs = [
    ([[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]], [[5, 5], [5, 5]]),
    ([[8, 1, 8, 8, 8, 8], [8, 1, 8, 8, 8, 8], [8, 1, 8, 8, 8, 8], [8, 1, 8, 8, 8, 8]], [[8, 8], [8, 8]]),
    ([[6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6]], [[6, 6], [6, 6]]),
    ([[2, 8, 3, 8, 2], [2, 8, 3, 8, 2], [2, 8, 3, 8, 2], [2, 8, 3, 8, 2], [2, 8, 3, 8, 2]], [[2, 2], [2, 2]]),
     ([[9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9]], [[9, 9], [9, 9]])
]

for i, (input_grid, output_grid) in enumerate(example_pairs):
    print(f"--- Example {i+1} ---")
    analyze_example(input_grid, output_grid)
