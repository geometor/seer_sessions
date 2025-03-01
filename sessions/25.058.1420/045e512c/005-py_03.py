import numpy as np

def describe_objects(grid):
    """
    Identifies and describes objects in a grid.
    Returns a dictionary of objects, keyed by color, with their bounding box.
    """
    objects = {}
    for color in np.unique(grid):
        rows, cols = np.where(grid == color)
        if len(rows) > 0:
            min_row, min_col = np.min(rows), np.min(cols)
            max_row, max_col = np.max(rows), np.max(cols)
            height = max_row - min_row + 1
            width = max_col - min_col + 1
            objects[color] = {
                'top_left': (min_row, min_col),
                'height': height,
                'width': width
            }
    return objects

def compare_grids(grid1, grid2):
    """Compares two grids and prints differences."""
    if grid1.shape != grid2.shape:
        print("Grids have different shapes:")
        print(f"  Grid 1: {grid1.shape}")
        print(f"  Grid 2: {grid2.shape}")
        return

    diff = grid1 != grid2
    if np.any(diff):
        print("Grids differ at the following coordinates:")
        diff_coords = np.where(diff)
        for row, col in zip(*diff_coords):
            print(f"  ({row}, {col}): Grid 1 = {grid1[row, col]}, Grid 2 = {grid2[row, col]}")
    else:
        print("Grids are identical.")
    
    print("\nGrid 1 Objects:")
    print(describe_objects(grid1))
    print("\nGrid 2 Objects:")
    print(describe_objects(grid2))


# Example Usage (replace with actual task data later)
# Assuming 'task' is loaded with training examples and 'transform' is defined

task = {
    "train": [
        {
            "input": np.array([
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 0, 3, 0],
                [0, 8, 8, 8, 8, 8, 0, 3, 0],
                [0, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]),
            "output": np.array([
                [0, 0, 0, 0, 0, 0, 0, 2, 2],
                [0, 8, 8, 8, 8, 8, 0, 2, 2],
                [0, 8, 8, 8, 8, 8, 0, 3, 2],
                [0, 8, 8, 8, 8, 8, 0, 3, 0],
                [0, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]),
        },
          {
            "input": np.array([
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 0, 3, 0],
                [0, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]),
            "output": np.array([
                [0, 0, 0, 0, 0, 0, 0, 2, 2],
                [0, 8, 8, 8, 8, 8, 0, 2, 2],
                [0, 8, 8, 8, 8, 8, 0, 3, 0],
                [0, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]),
        },
          {
            "input": np.array([
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 0, 3, 0],
                [0, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]),
            "output": np.array([
                [0, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 8, 8, 8, 8, 8, 0, 3, 0],
                [0, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]),
        },
    ]
}

for i, example in enumerate(task['train']):
    print(f"\n--- Example {i+1} ---")
    input_grid = example['input']
    expected_output_grid = example['output']
    predicted_output_grid = transform(input_grid)
    compare_grids(expected_output_grid, predicted_output_grid)
