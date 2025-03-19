import numpy as np

# Provided code (transform, find_objects, bounding_box) - pasted here for execution
def find_objects(grid, color):
    """Finds all distinct objects of a given color."""
    visited = set()
    objects = []

    def dfs(row, col):
        """Depth-first search to find contiguous regions."""
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []
        visited.add((row, col))
        coords = [(row, col)]
        coords.extend(dfs(row + 1, col))
        coords.extend(dfs(row - 1, col))
        coords.extend(dfs(row, col + 1))
        coords.extend(dfs(row, col - 1))
        return coords

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row, col] == color:
                object_coords = dfs(row, col)
                objects.append(object_coords)
    return objects

def bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    if not coords:
        return 0, 0, 0, 0
    rows = [r for r, _ in coords]
    cols = [c for _, c in coords]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find all green objects.
    green_objects = find_objects(input_grid, 3)
    
    output_grids = []
    # Iterate through each green object.
    for obj_coords in green_objects:
        # Get the bounding box.
        min_row, max_row, min_col, max_col = bounding_box(obj_coords)

        # Extract the object.
        object_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
        output_grids.append(object_grid)

    # if no objects, return a 3x3 array
    if len(output_grids) == 0:
        return np.zeros((3,3),dtype=int)
        
    # find largest dimensions
    max_height = 0
    max_width = 0
    for grid in output_grids:
      if grid.shape[0] > max_height:
        max_height = grid.shape[0]
      if grid.shape[1] > max_width:
        max_width = grid.shape[1]

    # create output grid and place each sub grid into it
    output_grid_final = np.zeros((max_height, max_width), dtype=int)
    first_grid = output_grids[0]
    output_grid_final[:first_grid.shape[0],:first_grid.shape[1]] = first_grid

    return output_grid_final

# Example data (replace with your actual data)
train_examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 3, 0],
                           [0, 0, 0, 0, 3, 0],
                           [0, 0, 0, 0, 3, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[3, 0, 0, 0, 0, 0],
                            [3, 0, 0, 0, 0, 0],
                            [3, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 3, 3, 3, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[3, 3, 3, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 3, 3, 0, 0],
                           [0, 0, 0, 0, 3, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[3, 3, 0, 0, 0, 0, 0, 0],
                            [3, 3, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
    },
        {
        "input": np.array([[3, 3, 3, 0, 0, 0, 0, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[3, 3, 3, 0, 0, 0, 0, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]])
    },
]

# Analyze each example
for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid.copy())  # Use a copy to avoid modifying the original

    green_objects_input = find_objects(input_grid, 3)
    num_green_objects_input = len(green_objects_input)

    # Compare predicted and expected outputs
    comparison = np.array_equal(predicted_output, expected_output)

    print(f"Example {i+1}:")
    print(f"  Number of green objects in input: {num_green_objects_input}")
    print(f"  Predicted Output Matches Expected: {comparison}")
    if not comparison:
        print(f"   Predicted Output:\n{predicted_output}")
        print(f"   Expected Output:\n{expected_output}")
    print("-" * 20)