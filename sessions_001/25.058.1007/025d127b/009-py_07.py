import numpy as np

def get_objects(grid, color):
    """Find connected components of a specific color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col):
        """Depth-first search to find connected pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        object_pixels = [(row, col)]

        object_pixels.extend(dfs(row + 1, col))
        object_pixels.extend(dfs(row - 1, col))
        object_pixels.extend(dfs(row, col + 1))
        object_pixels.extend(dfs(row, col - 1))

        return object_pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))

    return objects
    
def report(task_name, i, input_grid, expected_grid, actual_grid):
    print(f"----- {task_name}: Example {i} -----")
    print(f"Input:\n{input_grid}")
    print(f"Expected:\n{expected_grid}")
    print(f"Actual:\n{actual_grid}")

    input_red_objects = get_objects(input_grid, 2)
    expected_red_objects = get_objects(expected_grid, 2)
    actual_red_objects = get_objects(actual_grid, 2)
    
    input_magenta_objects = get_objects(input_grid, 6)
    expected_magenta_objects = get_objects(expected_grid, 6)
    actual_magenta_objects = get_objects(actual_grid, 6)
    
    print(f"Input Red Objects: {input_red_objects}")
    print(f"Expected Red Objects: {expected_red_objects}")
    print(f"Actual Red Objects: {actual_red_objects}")
    
    print(f"Input Magenta Objects: {input_magenta_objects}")
    print(f"Expected Magenta Objects: {expected_magenta_objects}")
    print(f"Actual Magenta Objects: {actual_magenta_objects}")
    
    diff_expected_actual = np.where(expected_grid != actual_grid)
    print(f"Differences between Expected and Actual: {list(zip(diff_expected_actual[0], diff_expected_actual[1]))}")
    print()

# Example data (replace with actual data from the task)
# make sure this matches the data in the prompt
train = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     ),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 0, 0, 6, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 6, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     ),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
               [0, 0, 0, 6, 2, 2, 6, 0, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 6, 0, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 6, 0, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 6, 0, 0, 0, 0],
               [0, 0, 0, 6, 2, 2, 6, 0, 0, 0, 0],
               [0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 6, 2, 2, 2, 2, 6, 0, 0, 0],
               [0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     )
]

def transform(input_grid):
    """
    Modify the magenta shape by shifting the leftmost/rightmost pixels inwards.
    """
    output_grid = np.copy(input_grid)
    magenta_objects = get_objects(input_grid, 6)
    red_objects = get_objects(input_grid, 2)
    
    for magenta_object in magenta_objects:
        # find leftmost and rightmost pixels
        min_col = min(pixel[1] for pixel in magenta_object)
        max_col = max(pixel[1] for pixel in magenta_object)
        
        leftmost_pixels = [p for p in magenta_object if p[1] == min_col]
        rightmost_pixels = [p for p in magenta_object if p[1] == max_col]
        
        # shift leftmost pixel
        for pixel in leftmost_pixels:
          row, col = pixel
          # check if the move is valid
          if col + 1 < output_grid.shape[1] and output_grid[row, col + 1] == 0:
            # check if move breaks connectivity
            temp_object = magenta_object.copy()
            temp_object.remove(pixel)
            temp_object.append((row,col+1))
            if is_connected(temp_object):
                output_grid[row, col] = 0
                output_grid[row, col + 1] = 6

        # shift rightmost pixel
        for pixel in rightmost_pixels:
            row, col = pixel
             # check if the move is valid
            if col - 1 >= 0 and output_grid[row, col - 1] == 0:
                # check if move breaks connectivity
                temp_object = magenta_object.copy()
                temp_object.remove(pixel)
                temp_object.append((row,col-1))

                if is_connected(temp_object):
                    output_grid[row, col] = 0
                    output_grid[row, col - 1] = 6

    return output_grid

def is_connected(pixels):
    """
    Checks if a set of pixels form a connected component using a simple
    adjacency check
    """
    if not pixels:
        return True  # Empty set is considered connected

    # Create a set of pixel coordinates for quick lookup
    pixel_set = set(pixels)

    # Check if the set is connected
    # Starting from the first pixel, do a depth-first search
    visited = set()
    stack = [pixels[0]]

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        # Add unvisited neighbors to the stack
        row, col = current
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        for neighbor in neighbors:
            if neighbor in pixel_set and neighbor not in visited:
                stack.append(neighbor)

    return len(visited) == len(pixel_set)

task_name = "39e1d7f9"
for i, (input_grid, expected_grid) in enumerate(train):
  actual_grid = transform(input_grid)
  report(task_name, i, input_grid, expected_grid, actual_grid)