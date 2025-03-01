import numpy as np

# Provided code (transform, get_objects, is_hollow_square functions)
# ... (insert the provided code here) ...
"""
Identify the largest hollow square object composed of yellow pixels. Extract the 2x2 subgrid located at the top-left corner of this hollow square. Output this 2x2 subgrid.
"""

import numpy as np

def get_objects(grid):
    """
    Find contiguous regions of the same color and return them as a list of objects.
    Each object is a dictionary containing the color, and the set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj_coords):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_coords.add((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                if color != 0:
                  obj_coords = set()
                  dfs(row, col, color, obj_coords)
                  objects.append({"color": color, "coords": obj_coords})
    return objects

def is_hollow_square(coords, grid):
    """
    Checks if a set of coordinates forms a hollow square.
    """
    if not coords:
        return False

    rows, cols = zip(*coords)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Check if it's a square
    if (max_row - min_row) != (max_col - min_col):
        return False

    # Check if it's hollow
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if (r > min_row and r < max_row) and (c > min_col and c < max_col):
                if (r, c) in coords:
                    return False  # Inner part should be empty
            else:
                if (r, c) not in coords:
                    return False # Border should be complete
    return True

def transform(input_grid):
    """
    Extracts the top-left 2x2 subgrid of the largest yellow hollow square.
    """
    # Find objects
    objects = get_objects(input_grid)

    # Find the largest yellow hollow square
    largest_hollow_square = None
    max_size = 0
    for obj in objects:
        if obj['color'] == 4 and is_hollow_square(obj['coords'], input_grid):
            size = max(obj['coords'], key=lambda x: x[0])[0] - min(obj['coords'], key=lambda x: x[0])[0] + 1
            if size > max_size:
                max_size = size
                largest_hollow_square = obj

    # initialize with background
    output_grid = np.zeros((2, 2), dtype=int)

    if largest_hollow_square:
        # Get the top-left corner coordinates of the hollow square
        min_row = min(coord[0] for coord in largest_hollow_square['coords'])
        min_col = min(coord[1] for coord in largest_hollow_square['coords'])

        # copy the 2x2 region
        for r in range(2):
            for c in range(2):
              if min_row + r < input_grid.shape[0] and min_col + c < input_grid.shape[1]:
                output_grid[r, c] = input_grid[min_row + r, min_col + c]

    return output_grid

# Training examples (replace with actual data)
train_examples = [
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 4, 4, 4, 0, 0, 0, 0],
            [0, 0, 4, 0, 4, 0, 0, 0, 0],
            [0, 0, 4, 4, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [4, 4],
            [4, 0],
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [4, 4],
            [4, 0],
        ]),
    },
    {
        "input": np.array([
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]),
        "output": np.array([
            [4, 4],
            [4, 4],
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 2, 2, 2],
            [0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 2, 0, 2],
            [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [4, 4],
            [4, 0],
        ]),
    },
    {
      "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [4, 4],
            [4, 0],
        ]),
    }

]

def validate_output(example):
    input_grid = example['input']
    expected_output = example['output']
    actual_output = transform(input_grid)
    return np.array_equal(actual_output, expected_output), actual_output

for i, example in enumerate(train_examples):
    is_correct, actual_output = validate_output(example)
    print(f"Example {i+1}: Correct: {is_correct}")
    print(f"  Expected Output:\n{example['output']}")
    print(f"  Actual Output:\n{actual_output}")
    print("-" * 20)