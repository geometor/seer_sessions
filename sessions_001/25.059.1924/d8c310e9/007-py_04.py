import numpy as np

def find_repeating_pattern(grid):
    """Finds a two-row repeating pattern in the grid."""
    height, width = grid.shape
    for i in range(height - 1):
        for j in range(i + 2, height):
            # Check if rows i and j are different, and if they form a repeating pattern up to the start of j
            if not np.array_equal(grid[i], grid[j]) and (j - i) * 2 <= height:
                pattern = grid[i:i+2]
                valid_pattern = True
                for k in range(i + 2, j, 2):  # check up to j
                    if k + 1 < height: # make sure we don't go over boundary
                      if not np.array_equal(grid[k:k+2], pattern):
                        valid_pattern = False
                        break
                    else:
                      if not np.array_equal(grid[k], pattern[0]):
                        valid_pattern = False
                        break
                if valid_pattern:
                    return pattern, i, j
    return None, -1, -1

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    grid_height, grid_width = input_grid.shape

    # Find the repeating pattern and its starting position
    pattern, start_row, next_pattern_row = find_repeating_pattern(input_grid)

    # Initialize the output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)

    # Copy input to output
    output_grid[:] = input_grid[:]

    if pattern is not None:
      # determine height of pattern fill
      pattern_height = next_pattern_row - start_row
      # Fill the identified region with the pattern
      for row_start in range(0, pattern_height):  # start fill from top
          for col_start in range(0, grid_width, pattern.shape[1]):
              col_end = min(col_start + pattern.shape[1], grid_width)
              output_grid[row_start::pattern_height, col_start:col_end] = pattern[row_start % 2, :col_end-col_start]

    return output_grid.tolist()

task = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
            ],
            "output": [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
            ],
            "output": [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        },
        {
            "input": [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
            ],
            "output": [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
            ]
        }
    ]
}

results = []
for example in task["train"]:
  input_grid = example['input']
  expected_output = example['output']
  actual_output = transform(input_grid)
  pattern, start, next_pat = find_repeating_pattern(np.array(input_grid))
  results.append({
      'input': input_grid,
      'expected': expected_output,
      'actual': actual_output,
      'pattern': pattern.tolist() if pattern is not None else None,
      'pattern_start': start,
      'next_pattern_row': next_pat,
      'correct': actual_output == expected_output
  })

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Correct: {result['correct']}")
    print(f"  Pattern: {result['pattern']}")
    print(f"  Pattern Start: {result['pattern_start']}")
    print(f"  Next Pattern Row: {result['next_pattern_row']}")
    if not result['correct']:
        print(f"  Differences: {np.array(result['expected']) - np.array(result['actual'])}")
