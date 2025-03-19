import numpy as np

# Provided find_objects and transform functions (copied here for completeness)
def find_objects(grid):
    """
    Finds contiguous regions of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    # Find all objects in the input grid
    objects = find_objects(np.array(input_grid))

    # Find the red objects (color 2)
    red_objects = [obj for obj in objects if input_grid[obj[0][0]][obj[0][1]] == 2]
    
    # Count the number of red objects
    count = len(red_objects)

    # Create an output grid of the determined height, filled with red (2)
    output_grid = np.full((count, 1), 2)

    return output_grid

# Example data (replace with your actual task data)
train_examples = [
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ], [
    [2],
    ]),    
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 3, 3, 0, 0, 0, 4, 0],
    [0, 0, 3, 3, 3, 0, 0, 0, 4, 0],
    [0, 0, 3, 3, 3, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ], [
    [3],
    [4]
    ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 7, 7, 7, 7, 7, 0, 0, 0],
    [0, 0, 7, 7, 7, 7, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ], [
    [7]
    ]),
  ([
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 5, 5, 5, 0, 0, 6, 6, 6, 0],
     [0, 5, 5, 5, 0, 0, 6, 6, 6, 0],
     [0, 5, 5, 5, 0, 0, 6, 6, 6, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ], [
      [5],
      [6]
    ])
]

for i, (input_grid, expected_output) in enumerate(train_examples):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    predicted_output = transform(input_grid.tolist())
    objects = find_objects(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input Objects: {len(objects)}")
    for obj in objects:
        color = input_grid[obj[0][0]][obj[0][1]]
        print(f"    Object Color: {color}, Size: {len(obj)}")
    print(f"  Predicted Output Shape: {predicted_output.shape}")
    print(f"  Expected Output Shape: {expected_output.shape}")
    print(f"  Match: {np.array_equal(predicted_output, expected_output)}")
    print("-" * 20)