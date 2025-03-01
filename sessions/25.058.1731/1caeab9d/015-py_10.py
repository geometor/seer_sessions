import numpy as np

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a dictionary containing:
    - 'equal': True if the grids are identical, False otherwise.
    - 'diff': A 2D array highlighting differences (if any).
             0 means the pixels match.
             1 means different.
    """

    equal = np.array_equal(grid1, grid2)
    diff = np.zeros(grid1.shape, dtype=int)
    if not equal:
      diff = (grid1 != grid2).astype(int)
    return {
        'equal': equal,
        'diff': diff
    }

def show_grid(grid):
    rows, cols = grid.shape
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            row_str += str(grid[r,c])
        print(row_str)

def analyze_example(input, expected):
    generated = transform(input)
    comparison = compare_grids(expected,generated)
    print("Input:")
    show_grid(input)
    print("Expected:")
    show_grid(expected)
    print("Generated:")
    show_grid(generated)    
    print("Comparison:")
    print(f"  equal: {comparison['equal']}")
    if not comparison['equal']:
      print("Difference:")
      show_grid(comparison['diff'])


# Example usage (replace with actual grids):
input_grids = [
    np.array([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0],[0,2,2,0,0],[0,2,2,0,0],[0,0,0,0,0],[0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[3,3,3,3,0,0],[3,3,3,3,0,0],[0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,4,4,4,4],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
]
expected_grids = [
    np.array([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0]]),
    np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,2,2,0,0],[0,2,2,0,0],[0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[3,3,3,3,0,0],[3,3,3,3,0,0]]),
    np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,4,4,4,4],[0,0,0,0,0,0,0]])
]

for i in range(len(input_grids)):
  analyze_example(input_grids[i],expected_grids[i])

