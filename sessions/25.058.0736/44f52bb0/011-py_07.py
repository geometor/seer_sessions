import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    """Analyzes a single example and returns relevant metrics."""
    input_shape = input_grid.shape
    expected_output_shape = expected_output.shape
    red_count = np.sum(input_grid == 2)
    blue_count = np.sum(input_grid == 1)
    #find the number of objects
    objects = []
    visited = np.zeros_like(input_grid, dtype=bool)

    def dfs(row, col, color):
      if (row < 0 or row >= input_grid.shape[0] or col < 0 or col >= input_grid.shape[1]
                  or visited[row, col] or input_grid[row, col] != color):
        return 0
      visited[row,col] = True
      return (1 + dfs(row + 1, col, color) + dfs(row - 1, col, color) +
                  dfs(row, col + 1, color) + dfs(row, col - 1, color))

    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            if not visited[row, col]:
                color = input_grid[row, col]
                object_size = dfs(row, col, color)
                if object_size > 0:
                  objects.append((color,object_size))

    result = {
        "input_shape": input_shape,
        "expected_output_shape": expected_output_shape,
        "expected_output_value": expected_output.tolist(),
        "actual_output_value": actual_output.tolist(),
        "red_count": int(red_count), # cast to native int
        "blue_count": int(blue_count), # cast to native int
        "objects": objects,
    }
    return result

# Load the example data (replace with your actual data loading)
# example_data is expected to be [(input_grid1, output_grid1), (input_grid2, output_grid2), ...]
# For demonstration, I am using a simpler way to construct example_data
import json
with open('data/training/d512799b.json', 'r') as f:
    task_data = json.load(f)
example_data = []
for example in task_data['train']:
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    example_data.append((input_grid, output_grid))

#the transform function
def transform(input_grid):
    """
    Transforms a grid by counting red pixels, dividing by two, and outputting the result.
    """
    # Count the red pixels (value 2).
    red_count = np.sum(input_grid == 2)

    # Divide by two
    output_value = red_count // 2

    # Create the 1x1 output grid.
    output_grid = np.array([[output_value]])

    return output_grid

# Analyze each example
analysis_results = []
for input_grid, output_grid in example_data:
    actual_output = transform(input_grid)
    analysis = analyze_example(input_grid, output_grid, actual_output)
    analysis_results.append(analysis)

# Print the analysis for each example
for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    print("-" * 20)