import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    print(f"  Dimensions: {rows}x{cols}")
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print(f"  Colors: {color_counts}")
    
    #find blue lines and positions
    blue_lines = []
    for r in range(rows):
        if all(grid[r,c] == 1 for c in range(cols)):
            blue_lines.append(r)
    print(f"  Blue Lines: {blue_lines}")

def analyze_example(input_grid, output_grid, predicted_grid):
    print("Input Grid:")
    describe_grid(input_grid)
    print("\nExpected Output Grid:")
    describe_grid(output_grid)
    print("\nPredicted Output Grid:")
    describe_grid(predicted_grid)
    print("\nDifferences (Expected - Predicted):")
    diff = output_grid - predicted_grid
    describe_grid(diff)
    print("-" * 20)

# Example data (replace with actual data from the task)
examples = [
    (
        np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]]),
        np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
        np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
    ),
     (
        np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0], [2,2,2]]),
        np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1], [2,2,2]]),
        np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1], [2,2,2]]),
    ),
    (
        np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]),
        np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
    ),
      (
        np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [6, 0, 0, 6]]),
        np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [6, 0, 0, 6]]),
        np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [6, 0, 0, 6]]),
    ),
]

for i, (input_grid, output_grid, predicted_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid, predicted_grid)
