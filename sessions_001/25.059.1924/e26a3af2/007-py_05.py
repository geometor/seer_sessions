import numpy as np

def get_columns_of_interest(grid):
    # identify columns of interest - with colors 8, 3, 2
    cols_of_interest = []
    for j in range(grid.shape[1]):
        unique_colors = np.unique(grid[:, j])
        if any(color in unique_colors for color in [8, 3, 2]):
            cols_of_interest.append(j)
    return cols_of_interest

def analyze_example(input_grid, output_grid):
    print(f"Input Grid Shape: {input_grid.shape}")
    print(f"Output Grid Shape: {output_grid.shape}")
    cols = get_columns_of_interest(input_grid)
    print(f"Columns of Interest: {cols}")
    for col in cols:
        print(f"Input Column {col}: {input_grid[:, col]}")
        print(f"Output Column {col}: {output_grid[:, col]}")

# Example usage with the provided training data
# (replace with actual input/output arrays from the task)
example_pairs = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 8, 0, 0, 0, 0],
               [0, 0, 0, 3, 0, 0, 0, 0],
               [0, 0, 0, 2, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 8, 0, 0, 0, 0],
               [0, 0, 0, 3, 0, 0, 0, 0],
               [0, 0, 0, 2, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]])),

    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 8, 0, 0, 0, 8, 0],
               [0, 0, 0, 3, 0, 0, 0, 3, 0],
               [0, 0, 0, 2, 0, 0, 0, 2, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[1, 1, 1, 8, 1, 1, 1, 8, 1],
               [1, 1, 1, 3, 1, 1, 1, 3, 1],
               [1, 1, 1, 2, 1, 1, 1, 2, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[1, 1, 1, 1, 8, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 3, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])),
     (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 8, 0, 0, 8, 0, 0],
               [0, 0, 0, 3, 0, 0, 3, 0, 0],
               [0, 0, 0, 2, 0, 0, 2, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[1, 1, 1, 8, 1, 1, 8, 1, 1],
               [1, 1, 1, 3, 1, 1, 3, 1, 1],
               [1, 1, 1, 2, 1, 1, 2, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1]])
     )
]

for i, (input_grid, output_grid) in enumerate(example_pairs):
    print(f"--- Example {i+1} ---")
    analyze_example(input_grid, output_grid)