import numpy as np

def find_objects(grid, color):
    """Finds connected regions of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_bounding_box(obj):
    """Calculates the bounding box of an object."""
    min_row = min(pixel[0] for pixel in obj)
    max_row = max(pixel[0] for pixel in obj)
    min_col = min(pixel[1] for pixel in obj)
    max_col = max(pixel[1] for pixel in obj)
    return (min_row, min_col), (max_row, max_col)

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    red_objects = find_objects(input_grid, 2)
    green_pixels = np.where(output_grid == 3)
    green_pixels = list(zip(green_pixels[0], green_pixels[1]))

    red_object_count = len(red_objects)
    bounding_boxes = [get_bounding_box(obj) for obj in red_objects]

    return {
        "red_object_count": red_object_count,
        "bounding_boxes": bounding_boxes,
        "green_pixels": green_pixels,
    }

# Example data (replace with actual grid data from the task)
example_data = [
    (np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 2, 2, 2, 0],
              [0, 0, 2, 2, 2, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 2, 2, 0, 0, 0],
              [0, 2, 2, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 3, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 3, 3, 0, 0, 0],
              [0, 3, 3, 0, 0, 0]])),

    (np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 2, 0, 0],
              [0, 0, 0, 2, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 2, 2, 0, 0, 0],
              [0, 0, 2, 2, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 3, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 3, 3, 0, 0, 0],
              [0, 0, 3, 3, 0, 0, 0]])),

    (np.array([[0, 0, 0, 0, 0, 0],
              [0, 2, 2, 2, 2, 0],
              [0, 2, 2, 2, 2, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0],
              [0, 3, 3, 3, 3, 0],
              [0, 3, 3, 3, 3, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]])),
    (np.array([[2, 2, 0, 0, 0, 0],
            [2, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]),
    np.array([[3, 3, 0, 0, 0, 0],
            [3, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]))
]

results = [analyze_example(inp, out) for inp, out in example_data]
print(results)
