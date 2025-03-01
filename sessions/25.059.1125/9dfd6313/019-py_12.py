import numpy as np

def describe_grid(grid):
    desc = {
        'shape': grid.shape,
        'colors': {}
    }
    for color in np.unique(grid):
        desc['colors'][int(color)] = np.sum(grid == color)
    return desc

def compare_grids(grid1, grid2):
    if grid1.shape != grid2.shape:
        return "Shapes are different"
    else:
        return np.array_equal(grid1, grid2)
    
examples = task["train"]

for idx, example in enumerate(examples):
  input_grid = np.array(example['input'])
  output_grid = np.array(example['output'])  
  predicted_output = transform(input_grid)
  print(f"Example {idx + 1}:")
  print(f"  Input: {describe_grid(input_grid)}")
  print(f"  Expected Output: {describe_grid(output_grid)}")
  print(f"  Predicted Output: {describe_grid(predicted_output)}")
  print(f"  Correct Prediction: {compare_grids(output_grid, predicted_output)}")
  print("-" * 20)