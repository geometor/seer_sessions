import numpy as np

def find_bounding_box(grid):
    """Find the bounding box of non-white pixels."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid case
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def find_preserve_and_fill_colors(grid, bounding_box):
    """Determine the preserve and fill colors based on the top-left non-white pixel."""
    min_row, _, min_col, _ = bounding_box
    
    # Find the top-left non-white pixel
    preserve_color = grid[min_row, min_col]

    # Find next row with a different color
    fill_color = None

    for r in range(min_row + 1, grid.shape[0]):
      if grid[r,min_col] != 0 and grid[r,min_col] != preserve_color:
        fill_color = grid[r,min_col]
        break
    if fill_color is None:
      fill_color = preserve_color

    return preserve_color, fill_color

def transform(input_grid):
    """Extracts a subgrid, preserves one color, and fills the rest with another."""
    input_grid = np.array(input_grid)  # Ensure numpy array

    # 1. Identify Region of Interest and Extract Subgrid
    bounding_box = find_bounding_box(input_grid)
    if bounding_box is None:
      return []
      
    min_row, max_row, min_col, max_col = bounding_box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1].copy()

    # 2. Identify Preserve and Fill Colors
    preserve_color, fill_color = find_preserve_and_fill_colors(input_grid, bounding_box)


    # 3. Translate and Fill (combined for efficiency)
    output_grid[output_grid != preserve_color] = fill_color
    

    return output_grid.tolist()

def calculate_metrics(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    # Check if the shapes of expected and actual outputs match
    if expected_output.shape != actual_output.shape:
        return {
            'match': False,
            'shape_match': False,
            'pixel_accuracy': 0.0,
            'input_shape': input_grid.shape,
            'expected_output_shape': expected_output.shape,
            'actual_output_shape': actual_output.shape
        }

    # Calculate pixel accuracy
    correct_pixels = np.sum(expected_output == actual_output)
    total_pixels = expected_output.size
    pixel_accuracy = correct_pixels / total_pixels

    return {
        'match': np.array_equal(expected_output, actual_output),
        'shape_match': True,
        'pixel_accuracy': pixel_accuracy,
        'input_shape': input_grid.shape,
        'expected_output_shape': expected_output.shape,
        'actual_output_shape': actual_output.shape
    }

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
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 2, 2]
            ],
            "output": [
                [1, 1],
                [2, 2]
            ]
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                [0, 0, 0, 0, 0, 0, 0, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 3, 3, 0]
            ],
            "output": [
                [3, 0],
                [0, 3],
                [3, 3],
                [3, 0]
            ]
        },
       {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 6, 6, 6, 6],
                [0, 0, 0, 0, 0, 0, 6, 6, 6, 6]
            ],
            "output": [
                [6, 6, 6, 6],
                [6, 6, 6, 6]
            ]
        },
       {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 4, 4, 0, 0],
                [0, 0, 0, 0, 0, 0, 4, 4, 0, 0]
            ],
            "output": [
                [4, 4],
                [4, 4]
            ]
        },
        {
            "input": [
              [5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
              [5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
              [5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
              [5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
              [5, 5, 5, 5],
              [5, 5, 5, 5],
              [5, 5, 5, 5],
              [5, 5, 5, 5]
            ]
        }
    ]
}

results = []
for example in task['train']:
    input_grid = example['input']
    expected_output = example['output']
    actual_output = transform(input_grid)
    metrics = calculate_metrics(input_grid, expected_output, actual_output)
    results.append({
        'input': input_grid,
        'expected_output': expected_output,
        'actual_output': actual_output,
        'metrics': metrics
    })

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Match: {result['metrics']['match']}")
    print(f"  Shape Match: {result['metrics']['shape_match']}")
    print(f"  Pixel Accuracy: {result['metrics']['pixel_accuracy']:.4f}")
    print(f"  Input Shape: {result['metrics']['input_shape']}")
    print(f"  Expected Output Shape: {result['metrics']['expected_output_shape']}")
    print(f"  Actual Output Shape: {result['metrics']['actual_output_shape']}")
    print("-" * 20)