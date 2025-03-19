import numpy as np

def analyze_results(examples, transform_function):
    analysis = []
    for i, (input_grid, expected_output_grid) in enumerate(examples):
        #convert to numpy arrays
        input_grid = np.array(input_grid)
        expected_output_grid = np.array(expected_output_grid)

        # Run transform function
        actual_output_grid = np.array(transform_function(input_grid.tolist()))

        # Compare actual output with expected output
        diff = actual_output_grid == expected_output_grid
        correct_pixels = np.sum(diff)
        total_pixels = diff.size
        accuracy = correct_pixels / total_pixels

        analysis.append({
            "example_index": i,
            "input_shape": input_grid.shape,
            "output_shape": expected_output_grid.shape,
            "accuracy": accuracy,
             "comments": "",
        })
    return analysis

# the provided transform function (from the prompt)
def transform(input_grid):
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()

    # Find the central blue shape.
    central_shape_coords = find_central_shape(input_grid, 1)
    if central_shape_coords is None:
        return output_grid.tolist()  # Return original if no blue shape is found

    # Expand the central blue shape.
    top_left, bottom_right = central_shape_coords
    output_grid = expand_shape(input_grid, top_left, bottom_right, 1)

    # Preserve gray pixels.
    output_grid = preserve_pixels(input_grid, output_grid, 5)

    return output_grid.tolist()

def find_central_shape(grid, color):
    # Find the bounding box of the central shape of the specified color.
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No shape of the specified color found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def expand_shape(grid, top_left, bottom_right, color):
    # Expand the shape defined by top_left and bottom_right by two layers.
    min_row, min_col = top_left
    max_row, max_col = bottom_right

    expanded_grid = grid.copy()

    # Expand by two layers
    for i in range(-2, 3):
      for j in range(-2,3):
        if abs(i) <=2 and abs(j) <=2: # this ensures its two layers of expansion at maximum
          for row in range(min_row, max_row + 1):
              expanded_grid[row + i, min_col + j] = color
              expanded_grid[row + i, max_col + j] = color
          for col in range(min_col, max_col + 1):
            expanded_grid[min_row + i, col + j] = color
            expanded_grid[max_row + i, col+j] = color


    return expanded_grid

def preserve_pixels(input_grid, output_grid, color):
    # Preserve the positions of pixels of a specific color.
    rows, cols = np.where(input_grid == color)
    for row, col in zip(rows, cols):
        output_grid[row, col] = color
    return output_grid

# dummy data for local development
train = [
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 5, 5, 5, 5, 5, 0, 0],
         [0, 0, 0, 5, 1, 1, 1, 5, 0, 0],
         [0, 0, 0, 5, 1, 1, 1, 5, 0, 0],
         [0, 0, 0, 5, 1, 1, 1, 5, 0, 0],
         [0, 0, 0, 5, 5, 5, 5, 5, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 5, 5, 5, 5, 5, 5, 5, 0],
         [0, 0, 5, 1, 1, 1, 1, 1, 5, 0],
         [0, 0, 5, 1, 1, 1, 1, 1, 5, 0],
         [0, 0, 5, 1, 1, 1, 1, 1, 5, 0],
         [0, 0, 5, 1, 1, 1, 1, 1, 5, 0],
         [0, 0, 5, 1, 1, 1, 1, 1, 5, 0],
         [0, 0, 5, 5, 5, 5, 5, 5, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    )
]

analysis_results = analyze_results(train, transform)
print(analysis_results)
