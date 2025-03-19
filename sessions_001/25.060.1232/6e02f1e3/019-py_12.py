import numpy as np

def get_grid_differences(grid1, grid2):
    """
    Compares two grids and returns a dictionary of differences.

    Args:
      grid1: The first grid (NumPy array).
      grid2: The second grid (NumPy array).

    Returns:
      A dictionary where keys are coordinates (row, col) and values are tuples
      representing the values in grid1 and grid2 at those coordinates.  Only
      coordinates where the values differ are included.
    """
    differences = {}
    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                differences[(i, j)] = (grid1[i, j], grid2[i, j])
    return differences

def analyze_example(example):
    """
     Analyzes a single training example.

     Args:
       example: A dictionary containing "input" and "output" grids.

     Returns:
         Prints statements showing an analysis
    """
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    print(f"Input grid:\n{input_grid}")
    print(f"Output grid:\n{output_grid}")
    diffs = get_grid_differences(input_grid, output_grid)
    if not diffs:
      print("grids are identical")
      return
    print("Differences (input, output):")
    for coord, values in diffs.items():
      print(f"  {coord}: {values}")
    print("-----")

# the test examples
train_examples = [
    {'input': [[8, 8, 8, 8, 8, 8, 8, 8]], 'output': [[5, 5, 5, 5, 5, 5, 5, 5]]},
    {'input': [[3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3]], 'output': [[5, 5, 5, 5, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[1, 1, 1, 1, 1, 1, 1, 1], [1, 8, 8, 8, 8, 8, 8, 1], [1, 8, 8, 8, 8, 8, 8, 1], [1, 1, 1, 1, 1, 1, 1, 1]], 'output': [[5, 5, 5, 5, 5, 5, 5, 5], [0, 8, 8, 8, 8, 8, 8, 0], [0, 8, 8, 8, 8, 8, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0]]}
]

for i, example in enumerate(train_examples):
    print(f"Analyzing Example {i+1}")
    analyze_example(example)