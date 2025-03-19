import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid highlighting the differences."""
    return (grid1 != grid2).astype(int)

def analyze_results(task):
  print(f"Task: {task['name']}")
  for i, example in enumerate(task['train']):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output = transform(input_grid)  # Assuming 'transform' is the function
    diff_grid_expected = compare_grids(output_grid, predicted_output)
    diff_grid_input = compare_grids(input_grid, predicted_output)
    print(f"  Example {i+1}:")
    print(f"    Input:\n{input_grid}")
    print(f"    Expected Output:\n{output_grid}")
    print(f"    Predicted Output:\n{predicted_output}")
    print(f"    Differences vs Expected:\n{diff_grid_expected}")
    print(f"    Differences vs Input: \n {diff_grid_input}")

# Example usage with a hypothetical task structure (replace with the actual task data)
# Assuming the 'transform' function is defined elsewhere and accessible

task = {
 'name': "Example Task",
 'train': [
   {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 3, 4, 3, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]},
   {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 4, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 4, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]},
   {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 3, 3, 4, 3, 3, 0, 0, 0], [0, 0, 3, 3, 4, 3, 3, 0, 0, 0], [0, 0, 3, 3, 4, 3, 3, 0, 0, 0], [0, 0, 0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}
 ]
}

analyze_results(task)