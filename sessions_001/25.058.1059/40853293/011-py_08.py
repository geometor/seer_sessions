import numpy as np

def compare_grids(grid1, grid2):
    """Checks if two grids are identical."""
    return np.array_equal(grid1, grid2)

def grid_to_string(grid):
    """Converts a grid to a string representation."""
    return str(grid)

# Example Data (replace with actual data from the task)
train_examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 4, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 4, 0, 0],
                            [0, 0, 0, 4, 0, 0],
                            [0, 0, 0, 4, 0, 1],
                            [0, 0, 0, 4, 0, 1]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 4, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 2]]),
        "output": np.array([[0, 4, 0, 0, 0, 0, 0],
                            [0, 4, 0, 0, 0, 0, 0],
                            [0, 4, 0, 0, 0, 0, 0],
                            [1, 4, 0, 0, 0, 0, 0],
                            [1, 4, 0, 0, 0, 0, 0],
                            [1, 4, 0, 0, 0, 0, 2]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 4, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 2]]),
        "output": np.array([[0, 0, 0, 4, 0, 0, 0],
                            [0, 0, 0, 4, 0, 0, 0],
                            [0, 0, 0, 4, 0, 0, 0],
                            [0, 0, 1, 4, 0, 0, 0],
                            [0, 0, 1, 4, 0, 0, 0],
                            [0, 0, 1, 4, 0, 0, 2]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0],
                           [0, 4, 0, 0, 0],
                           [0, 4, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0],
                           [1, 0, 0, 0, 2]]),
        "output": np.array([[0, 4, 0, 0, 0],
                            [0, 4, 0, 0, 0],
                            [0, 4, 0, 0, 0],
                            [0, 4, 0, 0, 0],
                            [1, 4, 0, 0, 0],
                            [1, 4, 0, 0, 2]]),
    },
    {
      "input": np.array([[7, 0, 0, 0, 4, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 2, 0, 0]]),
      "output": np.array([[7, 7, 7, 7, 4, 0, 0],
                         [0, 0, 0, 0, 4, 0, 0],
                         [0, 0, 0, 0, 4, 0, 0],
                         [0, 1, 1, 1, 4, 0, 0]])
    }
]

def run_and_check(transform_function, train_examples):
  results = []
  for ex in train_examples:
    input_grid = ex["input"]
    output_grid = ex["output"]
    predicted_output = transform_function(np.copy(input_grid))
    correct = compare_grids(predicted_output,output_grid)
    results.append({
        "input": grid_to_string(input_grid),
        "output": grid_to_string(output_grid),
        "predicted_output": grid_to_string(predicted_output),
        "correct": correct
    })
  return results

# Previous Code (as provided)
import numpy as np

def get_yellow_pixels(grid):
    """Finds the coordinates of all yellow (4) pixels."""
    yellow_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 4:
                yellow_pixels.append((r, c))
    return yellow_pixels

def expand_vertically(grid, start_row, col):
    """Expands yellow (4) pixels downwards until another object or edge."""
    rows = grid.shape[0]
    current_row = start_row

    while current_row < rows:
        if grid[current_row,col] != 0 and grid[current_row,col] !=4:
            break
        grid[current_row, col] = 4
        current_row += 1

def expand_horizontally(grid, yellow_pixels):
    """Expands colored pixels horizontally in rows occupied by expanded yellow."""

    rows = grid.shape[0]
    cols = grid.shape[1]

    # create dictionary with row number and set of columns occupied by yellow
    rows_dict = {}
    for r in range(rows):
      rows_dict[r] = set()

    for r in range(rows):
        for c in range(cols):
          if grid[r,c] == 4:
            rows_dict[r].add(c)

    for r in range(rows):
        for c in range(cols):
            if grid[r,c] !=0 and grid[r,c] !=4:
              if len(rows_dict[r]) > 0:
                for col in rows_dict[r]:
                  grid[r,col] = grid[r,c]



def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find yellow pixel coordinates
    yellow_pixels = get_yellow_pixels(output_grid)


    # expand the yellow pixels vertically
    for r, c in yellow_pixels:
        expand_vertically(output_grid, r, c)

    # expand other colored pixels horizontally
    expand_horizontally(output_grid,yellow_pixels)

    return output_grid

results = run_and_check(transform,train_examples)

for result in results:
    print(result)