import numpy as np

# Define the input and output grids for each example
train_examples = [
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [4],
            [4],
            [8]
        ])
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [8, 8]
        ])
    },
    {
      "input": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ]),
      "output": np.array([[8, 8, 8, 8, 8]])
    },
    {
      "input": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
      ]),
      "output": np.array([
        [4],
        [0],
        [0],
        [0],
        [4]
      ])
    }
]

def find_objects(grid):
    """Finds distinct colored rectangular blocks in the grid."""
    objects = {}
    visited = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and (r, c) not in visited:
                if color not in objects:
                    objects[color] = []
                obj_coords = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and (curr_r, curr_c) not in visited:
                        visited.add((curr_r, curr_c))
                        obj_coords.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects[color].append(obj_coords)
    return objects

def get_bounding_box(coords):
    """Calculates the bounding box of a list of coordinates."""
    min_r = min(c[0] for c in coords)
    max_r = max(c[0] for c in coords)
    min_c = min(c[1] for c in coords)
    max_c = max(c[1] for c in coords)
    return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Determine the output grid size and initialize
    if 4 in objects:  # Yellow exists, use for bookends
      yellow_coords = []
      for obj in objects[4]: # account for multiple objects
        yellow_coords.extend(obj)
        
      (min_r, min_c), (max_r, max_c) = get_bounding_box(yellow_coords)
      output_height = max_r - min_r + 1
      output_width = max_c - min_c + 1
      output_grid = np.zeros((output_height, output_width), dtype=int)
      
      # adjust coordinates based on position of yellow objects
      row_offset = min_r
      col_offset = min_c

    else:  # No yellow, base size on other objects
      all_coords = []
      for color in [2, 3, 8]:  # Consider only red, green, and azure
          if color in objects:
              for obj in objects[color]:
                all_coords.extend(obj)
      if all_coords:
        (min_r, min_c), (max_r, max_c) = get_bounding_box(all_coords)
        output_height = max_r - min_r + 1
        output_width = max_c - min_c + 1
        output_grid = np.zeros((output_height, output_width), dtype=int)
        row_offset = min_r
        col_offset = min_c
      else:
        return np.zeros((1,1), dtype=int) # nothing to draw

    # Place objects with color priority
    for color in [4, 2, 3, 8]:  # Iterate in priority order
        if color in objects:
            for obj_coords in objects[color]:
                for r, c in obj_coords:
                    # adjust the input grid coords to the output grid
                    output_r = r - row_offset
                    output_c = c - col_offset
                    # check that adjusted coords are in bounds
                    if 0 <= output_r < output_height and 0 <= output_c < output_width:
                      output_grid[output_r, output_c] = color
    
    return output_grid

# calculate and report results
for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)

    print(f"Example {i+1}:")

    # basic grid info
    print(f"  Input shape: {input_grid.shape}, Output shape: {expected_output.shape}, Predicted shape: {predicted_output.shape}")

    # Check if the predicted output matches the expected output
    match = np.array_equal(predicted_output, expected_output)
    print(f"  Prediction Matches Expected: {match}")

    # object metrics
    input_objects = find_objects(input_grid)
    output_objects = find_objects(expected_output)
    print(f"  Input objects: {input_objects}")
    print(f"  Output objects: {output_objects}")

    if not match:
      print(f"  Predicted output:\n{predicted_output}")
      print(f"  Expected output:\n{expected_output}")
    