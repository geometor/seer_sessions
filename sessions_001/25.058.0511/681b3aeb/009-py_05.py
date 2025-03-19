import numpy as np

def get_objects(grid):
    """
    Identifies and returns a list of distinct colored objects in the grid.
    Each object is represented as a list of (row, col) coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(rows):
        for col in range(cols):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                obj = []
                dfs(row, col, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects

def get_object_bounding_box(obj):
    """Calculates the bounding box for a single object."""
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')
    for row, col in obj:
        min_row = min(min_row, row)
        min_col = min(min_col, col)
        max_row = max(max_row, row)
        max_col = max(max_col, col)
    return min_row, min_col, max_row, max_col

def analyze_example(input_grid, expected_output, actual_output):
    """Analyzes a single example and prints relevant information."""
    print("Input Grid:")
    print(input_grid)
    print("\nExpected Output:")
    print(expected_output)
    print("\nActual Output:")
    print(actual_output)

    objects = get_objects(input_grid)
    print("\nObjects and Bounding Boxes:")
    sorted_objects = []
    for color, obj_list in objects.items():
        for obj in obj_list:
           ob_min_row, ob_min_col, ob_max_row, ob_max_col = get_object_bounding_box(obj)
           sorted_objects.append((color, obj, (ob_min_row, ob_min_col, ob_max_row, ob_max_col) ))
           print(f"  Color: {color}, Bounding Box: ({ob_min_row}, {ob_min_col}, {ob_max_row}, {ob_max_col})")

    sorted_objects.sort(key=lambda x: (x[3][0], x[3][1])) # sort by topleft corner of each object's bounding box
    print("\nSorted Objects:")
    for color, obj, bb in sorted_objects:
        print(f"  Color: {color}, Top-Left: ({bb[0]}, {bb[1]})")
    print("-" * 20)

# Example data (replace with actual data from the task)
example_data = [
    (
        np.array([[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 1, 1, 1, 0],
                  [0, 0, 1, 1, 1, 0],
                  [0, 0, 0, 0, 0, 0]]),
        np.array([[1, 1, 1],
                  [1, 1, 1]]),
        np.array([[1, 1, 1],
                  [1, 1, 1]])
    ),
     (
        np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 5, 5, 5, 5, 0],
                  [0, 0, 5, 5, 5, 5, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]),
        np.array([[5, 5, 5, 5],
                  [5, 5, 5, 5]]),
        np.array([[5, 5, 5, 5],
                  [5, 5, 5, 5]])
    ),
    (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 8, 8, 0],
                  [0, 0, 0, 0, 0, 8, 8, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 2, 2, 0, 0, 0, 0, 0],
                  [0, 2, 2, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[8, 8],
                  [8, 8],
                  [2, 2],
                  [2, 2]]),
        np.array([[8, 8],
                  [8, 8]]) # actual output need to be updated each iteration.
    ),
        (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 6, 0, 0, 0, 0],
                  [0, 0, 6, 6, 6, 0, 0, 0],
                  [0, 0, 0, 6, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 3, 3, 0, 0, 0, 0, 0],
                  [0, 3, 3, 0, 0, 0, 5, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[6, 6, 6],
                  [3, 3, 5]]),
        np.array([[6, 6, 6]])
    )
]

for input_grid, expected_output, actual_output in example_data:
    analyze_example(input_grid, expected_output, actual_output)