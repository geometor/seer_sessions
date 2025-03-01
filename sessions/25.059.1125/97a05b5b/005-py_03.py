import numpy as np

# Provided data (replace with actual data from the prompt)
train_examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 0, 0],
                           [0, 5, 5, 5, 0, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[2, 2, 2, 2, 2, 2],
                            [2, 5, 5, 5, 2, 2],
                            [2, 5, 5, 5, 2, 2],
                            [2, 2, 2, 2, 2, 2]])
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 7, 7, 7, 7, 0, 0],
                           [0, 0, 7, 7, 7, 7, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 7, 7, 7, 7, 2, 2],
                            [2, 2, 7, 7, 7, 7, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 1, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 1, 1, 1, 1, 1, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 8, 8, 8, 0, 0],
                           [0, 8, 8, 8, 0, 0],
                           [0, 8, 8, 8, 0, 0],
                           [0, 8, 8, 8, 0, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[2, 2, 2, 2, 2, 2],
                            [2, 8, 8, 8, 2, 2],
                            [2, 8, 8, 8, 2, 2],
                            [2, 8, 8, 8, 2, 2],
                            [2, 8, 8, 8, 2, 2],
                            [2, 2, 2, 2, 2, 2]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 0, 0, 6, 6],
                           [0, 5, 5, 5, 0, 0, 6, 6],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 5, 5, 5, 2, 2, 6, 6],
                            [2, 5, 5, 5, 2, 2, 6, 6],
                            [2, 2, 2, 2, 2, 2, 2, 2]])
    }
]

def find_objects(grid, ignore_colors):
    """Finds contiguous objects of non-ignored colors."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, obj_coords):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col] and grid[row, col] not in ignore_colors:
                obj_coords = []
                dfs(row, col, grid[row, col], obj_coords)
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Initialize output_grid as a copy of the input, then change it all to red.
    output_grid = np.full_like(input_grid, 2)

    # Identify Sub-Objects in the *original* input grid
    ignore_colors = [0, 2]  # Ignore white and red
    sub_objects = find_objects(input_grid, ignore_colors)

    # Preserve Sub-Object Colors
    for obj_coords in sub_objects:
        for row, col in obj_coords:
            # Copy the original color from the input to the output
            output_grid[row, col] = input_grid[row, col]
            
    return output_grid

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    
    # Find objects in input
    input_objects = find_objects(input_grid, [0])
    input_object_colors = [input_grid[obj[0][0], obj[0][1]] for obj in input_objects]

    # Find object in output
    output_objects = find_objects(expected_output, [0, 2])
    output_object_colors = [expected_output[obj[0][0], obj[0][1]] for obj in output_objects if expected_output[obj[0][0], obj[0][1]] != 2]


    comparison = (predicted_output == expected_output).all()
    print(f"Example {i+1}:")
    print(f"  Correct: {comparison}")
    print(f"  Input objects count: {len(input_objects)}, colors: {np.unique(input_object_colors)}")
    print(f"  Output object count: {len(output_objects)}, colors: {np.unique(output_object_colors)}")
    print(f"  Different Pixels: {np.sum(predicted_output != expected_output)}")