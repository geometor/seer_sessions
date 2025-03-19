import numpy as np

def _find_subgrid(grid):
    """Finds the bounding box of non-zero pixels."""
    rows, cols = grid.shape
    min_row, max_row = rows, -1
    min_col, max_col = cols, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                min_row = min(min_row, r)
                max_row = max(max_row, r)
                min_col = min(min_col, c)
                max_col = max(max_col, c)

    return min_row, max_row, min_col, max_col

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_dims = input_grid.shape
    output_dims = output_grid.shape
    min_row, max_row, min_col, max_col = _find_subgrid(input_grid)
    subgrid_dims = (max_row - min_row + 1, max_col - min_col + 1)

    # store subgrid for easier processing
    subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]

    # check output grid dimensions, should match input
    dims_match = input_dims == output_dims

    # simple color transformation check - within subgrid
    color_transformed = True
    # yellow should be preserved
    # every non-zero, non-yellow color should be 1 (blue)
    for r in range(subgrid_dims[0]):
        for c in range(subgrid_dims[1]):
            i_val = subgrid[r,c]
            o_val = output_grid[min_row + r, min_col + c]
            if i_val != 0: # inside subgrid
                if i_val == 4: # yellow
                    if i_val != o_val:
                        color_transformed = False
                        break
                elif o_val != 1: # should be blue
                    color_transformed = False
                    break

    #column pattern, within subgrid
    column_pattern = True
    for r in range(subgrid_dims[0]):
      for c in range(subgrid_dims[1]):
        o_val = output_grid[min_row + r, min_col + c]
        if (c+1) % 2 == 0: #even
          if o_val != 1:
            column_pattern = False
            break
        else: #odd
          if r % 3 == 2:
              if o_val != 1:
                column_pattern = False
                break

    return {
        'input_dims': input_dims,
        'output_dims': output_dims,
        'subgrid_dims': subgrid_dims,
        'subgrid_bounds': (min_row, max_row, min_col, max_col),
        'dims_match': dims_match,
        'color_transformed': color_transformed,
        'column_pattern': column_pattern
    }

# Example Usage (replace with your actual train_pairs)
train_pairs = [
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ], [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 1, 0, 0, 0],
        [0, 0, 0, 0, 4, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]),
        ([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 4, 0, 0, 0],
        [0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 4, 5, 0, 0, 0],
        [0, 0, 0, 1, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ], [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 1, 0, 0, 0],
        [0, 0, 0, 4, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0],
        [0, 0, 0, 0, 2, 1, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 4, 5, 0, 0, 0],
        [0, 0, 0, 0, 1, 4, 1, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ], [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 1, 4, 1, 0, 0, 0],
        [0, 0, 0, 0, 4, 1, 4, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 4, 4, 0, 0, 0],
        [0, 2, 1, 2, 1, 0, 0, 0],
        [0, 4, 5, 4, 5, 0, 0, 0],
        [0, 1, 4, 1, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],[
        [0, 4, 1, 4, 1, 0, 0, 0],
        [0, 4, 1, 4, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]),
]

results = [analyze_example(inp, out) for inp, out in train_pairs]

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(res)