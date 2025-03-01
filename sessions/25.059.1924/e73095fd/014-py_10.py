import numpy as np

def analyze_results(train_examples, transform_func):
    results = []
    for i, (input_grid, expected_output) in enumerate(train_examples):
        transformed_grid = transform_func(input_grid)
        comparison_result = np.array_equal(transformed_grid, expected_output)
        
        # Find differences
        diff = np.where(transformed_grid != expected_output)
        num_diffs = diff[0].size #length of the differences
        
        results.append({
            "example": i + 1,
            "correct": comparison_result,
            "num_differences": num_diffs,
            "differences": diff
        })
    return results

# re-use the function and training data from the prompt
# Previous Code:
def find_gray_shape(grid):
    # Find all gray pixels (value 5)
    gray_pixels = np.argwhere(grid == 5)
    return gray_pixels

def is_corner(grid, row, col):
    # Check if a gray pixel is part of a "corner-like" structure
    gray = 5

    if grid[row,col] != gray:
      return False

    neighbors = 0
    if row > 0 and grid[row-1, col] == gray:
      neighbors +=1
    if row < grid.shape[0] -1 and grid[row + 1, col] == gray:
      neighbors += 1
    if col > 0 and grid[row, col - 1] == gray:
      neighbors += 1
    if col < grid.shape[1] - 1 and grid[row, col + 1] == gray:
        neighbors += 1

    # diagonals
    if row > 0 and col > 0 and grid[row - 1, col - 1] == gray:
        neighbors +=1
    if row > 0 and col < grid.shape[1] - 1 and grid[row - 1, col+1] == gray:
        neighbors += 1
    if row < grid.shape[0] -1 and col > 0 and grid[row+1, col-1] == gray:
        neighbors += 1
    if row < grid.shape[0] - 1 and col < grid.shape[1] - 1 and grid[row + 1, col+1] == gray:
        neighbors += 1

    if neighbors >= 4 and neighbors <= 6:
        return True

    return False

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find gray shape pixels
    gray_pixels = find_gray_shape(input_grid)

    # iterate and find approximate locations, selectively replace them with yellow
    for row, col in gray_pixels:
      if is_corner(output_grid, row, col):
        output_grid[row,col] = 4

    return output_grid

task_id = "6b869486"
train_examples = [
  (
        np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),

        np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    ),
    (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),

        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 4, 4, 4, 5, 5, 5, 4, 4, 4, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 4, 4, 4, 5, 5, 5, 4, 4, 4, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    ),
    (
       np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),

        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 4, 4, 4, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 4, 4, 4, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 4, 4, 4, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    ),
]

analysis = analyze_results(train_examples, transform)
print(analysis)