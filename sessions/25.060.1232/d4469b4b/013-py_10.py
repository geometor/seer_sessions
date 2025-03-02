import numpy as np

def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def analyze_example(input_grid, output_grid, predicted_output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    bounding_box = get_bounding_box(input_grid, 1)
    if bounding_box:
      (min_row, min_col), (max_row, max_col) = bounding_box
      bb_h = max_row - min_row + 1
      bb_w = max_col - min_col + 1
    else:
       min_row, min_col, max_row, max_col, bb_h, bb_w = None, None, None, None, None, None

    white_pixels = np.where(output_grid == 0)
    white_pixel_coords = list(zip(white_pixels[0], white_pixels[1]))
    correct = np.array_equal(output_grid, predicted_output_grid)

    return {
        'input_dims': input_grid.shape,
        'bounding_box': (min_row, min_col, max_row, max_col),
        'bb_dims': (bb_h, bb_w),
        'output_dims': output_grid.shape,
        'white_pixels': white_pixel_coords,
        'correct': correct
    }

def transform(input_grid):
    input_grid = np.array(input_grid)
    # 1. Identify the Blue Region and 2. Determine Bounding Box
    bounding_box = get_bounding_box(input_grid, 1)
    if bounding_box is None:
        return [] # Return empty if there is no blue region.

    (min_row, min_col), (max_row, max_col) = bounding_box
    bb_h = max_row - min_row + 1
    bb_w = max_col - min_col + 1

    # 3. Determine Output Dimensions
    if bb_h == 3 and bb_w == 3:
        output_h, output_w = bb_h, bb_w
        output_grid = np.full((output_h, output_w), 5, dtype=int)
        output_grid[0, 0] = 0
        output_grid[0, -1] = 0
        output_grid[-1, 0] = 0
        output_grid[-1, -1] = 0
    elif bb_h == 3 and bb_w == 4:
        output_h, output_w = bb_h + 1, bb_w
        output_grid = np.full((output_h, output_w), 5, dtype=int)
        output_grid[0, 0] = 0
        output_grid[0, -1] = 0
        output_grid[-1, 0] = 0
        output_grid[-1, -1] = 0

    elif bb_h == 3 and bb_w == 5:
      output_h, output_w = bb_h + 2, bb_w + 1
      output_grid = np.full((output_h, output_w), 5, dtype=int)
      output_grid[0, 0] = 0
      output_grid[0, -1] = 0
      output_grid[-1, 0] = 0
      output_grid[-1, -1] = 0
    
    elif bb_h == 3 and bb_w == 4: # This is duplicate, need to consider other factors to decide between these two options.
        output_h, output_w = bb_h + 1, bb_w + 2
        output_grid = np.zeros((output_h, output_w), dtype=int)
        output_grid[0:2, 0:2] = 0
        output_grid[0:2, -2:] = 0
        output_grid[2:, :] = 5

    else:
        return []  # Should not happen, based on current examples

    return output_grid.tolist()

# Example Usage (replace with your actual task data)
task_data = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 5, 5, 0], [5, 5, 5, 5], [5, 5, 5, 5], [0, 5, 5, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 5, 5, 0], [5, 5, 5, 5], [5, 5, 5, 5], [0, 5, 5, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [0, 5, 5, 5, 5, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 5, 5, 0, 0], [0, 0, 5, 5, 0, 0], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5]]
    }
  ]
}

results = []
for example in task_data['train']:
  predicted_output = transform(example['input'])
  analysis = analyze_example(example['input'], example['output'], predicted_output)
  results.append(analysis)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Dims: {result['input_dims']}")
    print(f"  BB Dims: {result['bb_dims']}")
    print(f"  Output Dims: {result['output_dims']}")
    print(f"  Correct: {result['correct']}")
    print(f"  White Pixels: {result['white_pixels']}")
    print("-" * 20)