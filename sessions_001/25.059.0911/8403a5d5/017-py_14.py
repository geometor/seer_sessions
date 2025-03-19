import numpy as np

def find_seed(grid):
    # Find the coordinates of the yellow (4) pixel.
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 4:
                return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # find seed pixel
    seed_row, seed_col = find_seed(input_grid)

    # create the yellow cross
    for r in range(rows):
      output_grid[r, seed_col] = 4
    for c in range(cols):
      output_grid[seed_row, c] = 4

    # alternating fill
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 0:
                if (abs(r - seed_row) + abs(c - seed_col)) % 2 == 0:
                  output_grid[r,c] = 4


    # corner replacement
    if output_grid[0, 0] == 0:
      output_grid[0, 0] = 5
    if output_grid[0, cols-1] == 0:
      output_grid[0, cols-1] = 5
    if output_grid[rows-1, 0] == 0:
      output_grid[rows-1, 0] = 5
    if output_grid[rows-1, cols-1] == 0:
      output_grid[rows-1, cols-1] = 5

    return output_grid

# Example data (replace with your actual task data)

# input_output_pairs is expected as list of dicts with 'input' and 'output'
# keys holding 2d arrays
input_output_pairs = [
    {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0]],
        "output": [[5, 0, 0, 4, 0, 0], [0, 0, 4, 4, 4, 0], [0, 0, 0, 4, 0, 5]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[5, 0, 0, 0, 4, 0, 0, 5], [0, 0, 0, 4, 4, 4, 0, 0], [0, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0, 5]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[5, 0, 0, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 4, 4, 4, 0], [0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0, 5]],
    }
]

results = []
for i, pair in enumerate(input_output_pairs):
    input_grid = np.array(pair['input'])
    expected_output_grid = np.array(pair['output'])
    predicted_output_grid = transform(input_grid)
    seed_location = find_seed(input_grid)
    is_correct = np.array_equal(predicted_output_grid, expected_output_grid)
    results.append(
        {
            "example_index": i,
            "seed_location": seed_location,
            "is_correct": is_correct,
            "predicted_output": predicted_output_grid.tolist(),
            "expected_output": expected_output_grid.tolist(),
        }
    )

print(results)
