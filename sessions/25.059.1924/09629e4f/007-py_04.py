# Simulated code execution for analysis (using numpy for demonstration)
import numpy as np

# Example data (replace with actual grid data from the task)
example1_input = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5, 5],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
])
example1_output = np.array([
    [2, 2, 2, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5, 5],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5, 5],
    [6, 6, 6, 0, 0, 0, 0, 0, 0],
    [6, 6, 6, 0, 0, 0, 0, 0, 0],
    [6, 6, 6, 0, 0, 0, 0, 0, 0],
])

example2_input = np.array([
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [5,5,5,5,5,5],
  [0,0,0,5,0,0],
  [5,5,5,5,5,5],
  [0,0,0,0,0,0]
])

example2_output = np.array([
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [5,5,5,5,5,5],
  [0,0,0,5,0,0],
  [5,5,5,5,5,5],
  [0,0,0,0,0,0]
])

example3_input = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
])
example3_output = np.array([
    [2, 2, 2, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [6, 6, 6, 0, 0, 0, 0, 0],
    [6, 6, 6, 0, 0, 0, 0, 0],
    [6, 6, 6, 0, 0, 0, 0, 0],
])

def get_grey_lines(grid):
    """Finds rows that are entirely grey (5)."""
    return np.where((grid == 5).all(axis=1))[0]

def analyze_regions(grid):
  grey_lines = get_grey_lines(grid)
  num_regions = len(grey_lines) + 1
  print(f"Number of Grey Lines: {len(grey_lines)}")
  print(f"Number of Regions: {num_regions}")
  return grey_lines, num_regions

print("Example 1 Analysis:")
analyze_regions(example1_input)
print("Example 2 Analysis:")
analyze_regions(example2_input)
print("Example 3 Analysis:")
analyze_regions(example3_input)

