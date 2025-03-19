import numpy as np

def get_objects(grid, color):
    # Find objects of a specific color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] == color:
                object_pixels = []
                queue = [(r, c)]
                visited[r, c] = True

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    object_pixels.append((curr_r, curr_c))

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if 0 <= new_r < rows and 0 <= new_c < cols and \
                           not visited[new_r, new_c] and grid[new_r, new_c] == color:
                            queue.append((new_r, new_c))
                            visited[new_r, new_c] = True

                objects.append(object_pixels)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Copy yellow pixels directly.
    # No change needed as we are copying the whole input_grid

    # 2. Transform azure pixels in the top 3 rows.
    for row_index in range(min(3, rows)):  # Iterate through the top 3 rows
        # Find the leftmost azure pixel's column in the current row
        leftmost_col = cols
        azure_pixels = []
        for c in range(cols):
            if input_grid[row_index, c] == 8:
                leftmost_col = min(leftmost_col, c)
                azure_pixels.append((row_index,c))

        # Shift azure pixels in the current row if any exist
        if azure_pixels:
            for r, c in azure_pixels:
              output_grid[r, c] = 0  # Clear original position
              new_c = c - leftmost_col
              output_grid[r, new_c] = 8  # Set new position


    return output_grid

def analyze_results(task):
    print("Analyzing Results for Task")
    for i, example in enumerate(task['train']):
      input_grid = np.array(example['input'])
      expected_output = np.array(example['output'])
      actual_output = transform(input_grid)
      
      print(f"Example {i +1}:")
      print("Input:")
      print(input_grid)
      print("Expected Output:")
      print(expected_output)
      print("Actual Output:")
      print(actual_output)
      
      diff = expected_output != actual_output
      print(f"Number of differences = {np.sum(diff)}")
      print(diff)
      if np.any(diff):
          print(f"Differences found at indices: {np.where(diff)}")
      print("-" * 20)

#this needs to be provided by the user to work
#analyze_results(task)