import numpy as np

def analyze_grid(grid):
    """Counts pixels of each color and identifies object bounds."""
    color_counts = {}
    for color in range(10):  # Assuming colors 0-9
        coords = np.argwhere(grid == color)
        if len(coords) > 0:
            color_counts[color] = len(coords)
           
    return color_counts
def compare_grids(grid1, grid2):
    """compare two grids"""
    if grid1.shape != grid2.shape:
        return "different"
    return "same" if np.array_equal(grid1, grid2) else "different"

examples = [
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 1, 0, 2, 1, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 1, 2, 2, 1, 0],
            [0, 1, 2, 2, 1, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0]
        ]),
    },
     {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 2, 0, 1, 0],
            [0, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 2, 1, 1, 0],
            [0, 1, 2, 2, 2, 1, 0],
            [0, 1, 1, 2, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 2, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 2, 2, 1, 0, 0],
            [0, 0, 1, 2, 2, 1, 0, 0],
            [0, 0, 1, 2, 2, 1, 0, 0],
            [0, 0, 1, 2, 2, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
    },
       {
        "input": np.array([
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 2, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]),
        "output": np.array([
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 2, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ])
    }

]

for i, example in enumerate(examples):
  input_grid = example["input"]
  expected_output = example["output"]
  
  #use transform function
  actual_output = transform(input_grid.copy())

  input_analysis = analyze_grid(input_grid)
  expected_output_analysis = analyze_grid(expected_output)
  actual_output_analysis = analyze_grid(actual_output)
  comparison_result = compare_grids(expected_output, actual_output)
  print(f"Example {i + 1}:")
  print(f"  Input Grid Analysis: {input_analysis}")
  print(f"  Expected Output Analysis: {expected_output_analysis}")
  print(f" Actual Output Analysis: {actual_output_analysis}")
  print(f"  Comparison with Expected: {comparison_result}")