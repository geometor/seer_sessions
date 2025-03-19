import numpy as np

train = [
    (np.array([[5, 8, 6], [5, 5, 8], [8, 6, 6]]), np.array([[1, 9, 2], [1, 1, 9], [9, 2, 2]])),
    (np.array([[8, 5, 5], [8, 8, 6], [5, 6, 6]]), np.array([[9, 1, 1], [9, 9, 2], [1, 2, 2]])),
    (np.array([[8, 6, 5], [6, 6, 8], [5, 8, 5]]), np.array([[9, 2, 1], [2, 2, 9], [1, 9, 1]])),
    (np.array([[6, 8, 6, 8, 5], [8, 5, 8, 5, 6], [6, 6, 5, 6, 5]]), np.array([[2, 9, 2, 9, 1], [9, 1, 9, 1, 2], [2, 2, 1, 2, 1]])),
    (np.array([[5, 5, 6, 8, 8], [5, 5, 8, 8, 6], [8, 5, 6, 5, 6]]), np.array([[1, 1, 2, 9, 9], [1, 1, 9, 9, 2], [9, 1, 2, 1, 2]]))
]

for i, (input_grid, output_grid) in enumerate(train):
    input_counts = {}
    output_counts = {}

    for value in np.unique(input_grid):
        input_counts[value] = np.sum(input_grid == value)
    for value in np.unique(output_grid):
        output_counts[value] = np.sum(output_grid == value)

    print(f"Example {i+1}:")
    print(f"  Input grid shape: {input_grid.shape}")
    print(f"  Input color counts: {input_counts}")
    print(f"  Output grid shape: {output_grid.shape}")
    print(f"  Output color counts: {output_counts}")
