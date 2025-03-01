import numpy as np

def analyze_example(input_grid, output_grid, predicted_output_grid):
    """Analyzes a single example and returns relevant metrics."""

    def get_region_bounds(grid, color):
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            return None  # Handle cases where the color isn't present
        min_y, min_x = np.min(coords, axis=0)
        max_y, max_x = np.max(coords, axis=0)
        return {
            'min_x': int(min_x), 'max_x': int(max_x),
            'min_y': int(min_y), 'max_y': int(max_y),
            'width': int(max_x - min_x + 1),
            'height': int(max_y - min_y + 1),
            'count' : int(coords.shape[0])
        }
    
    green_bounds_input = get_region_bounds(input_grid, 3)
    green_bounds_output = get_region_bounds(output_grid, 3)
    orange_bounds_input = get_region_bounds(input_grid, 7)
    magenta_bounds_input = get_region_bounds(input_grid, 6)

    metrics = {
        'green_input': green_bounds_input,
        'green_output': green_bounds_output,
        'orange_input': orange_bounds_input,
        'magenta_input': magenta_bounds_input,        
        'output_shape': output_grid.shape,
        'predicted_output_shape': predicted_output_grid.shape,
        'output_equals_predicted': np.array_equal(output_grid, predicted_output_grid)
    }
    return metrics

def test_transform_on_examples(task_examples, transform_func):
  results = []
  for example in task_examples:
     input_grid = np.array(example['input'])
     output_grid = np.array(example['output'])
     predicted_output_grid = transform_func(input_grid)
     analysis = analyze_example(input_grid, output_grid, predicted_output_grid)
     results.append(analysis)
  return results
     

task_examples = [
    {
        "input": [
            [6, 6, 3, 3, 3, 3, 3, 3],
            [6, 6, 3, 3, 3, 3, 3, 3],
            [7, 7, 3, 3, 3, 3, 3, 3],
            [7, 7, 3, 3, 3, 3, 3, 3],
            [7, 7, 3, 3, 3, 3, 3, 3],
            [7, 7, 3, 3, 3, 3, 3, 3],
            [7, 7, 3, 3, 3, 3, 3, 3],
            [7, 7, 3, 3, 3, 3, 3, 3],
        ],
        "output": [
            [0, 0, 7, 6, 7, 6, 7, 6],
            [0, 0, 6, 7, 6, 7, 6, 7],
            [0, 0, 7, 6, 7, 6, 7, 6],
            [0, 0, 6, 7, 6, 7, 6, 7],
            [0, 0, 7, 6, 7, 6, 7, 6],
            [0, 0, 6, 7, 6, 7, 6, 7],
            [0, 0, 7, 6, 7, 6, 7, 6],
            [0, 0, 6, 7, 6, 7, 6, 7],
        ],
    },
    {
        "input": [
            [6, 6, 6, 6, 3, 3, 3, 7, 7, 7],
            [6, 6, 6, 6, 3, 3, 3, 7, 7, 7],
            [6, 6, 6, 6, 3, 3, 3, 7, 7, 7],
            [6, 6, 6, 6, 3, 3, 3, 7, 7, 7],
            [6, 6, 6, 6, 3, 3, 3, 7, 7, 7],
        ],
        "output": [
            [0, 0, 0, 0, 7, 6, 7, 0, 0, 0],
            [0, 0, 0, 0, 6, 7, 6, 0, 0, 0],
            [0, 0, 0, 0, 7, 6, 7, 0, 0, 0],
            [0, 0, 0, 0, 6, 7, 6, 0, 0, 0],
            [0, 0, 0, 0, 7, 6, 7, 0, 0, 0],
        ],
    },
    {
        "input": [
            [6, 6, 6, 3, 3, 7, 7, 7, 7],
            [6, 6, 6, 3, 3, 7, 7, 7, 7],
            [6, 6, 6, 3, 3, 7, 7, 7, 7],
            [6, 6, 6, 3, 3, 7, 7, 7, 7],
        ],
        "output": [
            [0, 0, 0, 7, 6, 0, 0, 0, 0],
            [0, 0, 0, 6, 7, 0, 0, 0, 0],
            [0, 0, 0, 7, 6, 0, 0, 0, 0],
            [0, 0, 0, 6, 7, 0, 0, 0, 0],
        ],
    },
]

#from previous code
import numpy as np

def get_region(grid, color):
    """Finds a region of the specified color within the grid."""
    coords = np.argwhere(grid == color)
    return coords

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    # Identify Regions
    magenta_region = get_region(input_grid, 6)
    orange_region = get_region(input_grid, 7)
    green_region = get_region(input_grid, 3)

    # Determine dimensions of combined non-green region, assuming a perfect rectangle can be made after green is removed
    min_x = min(np.min(magenta_region[:, 1]), np.min(orange_region[:, 1]))
    max_x = max(np.max(magenta_region[:, 1]), np.max(orange_region[:, 1]))
    min_y = min(np.min(magenta_region[:, 0]), np.min(orange_region[:, 0]))
    max_y = max(np.max(magenta_region[:, 0]), np.max(orange_region[:, 0]))
    
    width = input_grid.shape[1]  # Full width from green region.
    height = input_grid.shape[0] # Full height.

    # Initialize output grid
    output_grid = np.zeros((height, width), dtype=int)

    # Checkerboard Rearrangement
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                output_grid[y, x] = 7  # Orange
            else:
                output_grid[y, x] = 6  # Magenta

    return output_grid

results = test_transform_on_examples(task_examples, transform)

for i, analysis in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Green Input Bounds: {analysis['green_input']}")
    print(f"  Output Shape: {analysis['output_shape']}")
    print(f"  Predicted Output Shape: {analysis['predicted_output_shape']}")
    print(f"  Output Equals Predicted: {analysis['output_equals_predicted']}")
    print("-" * 20)