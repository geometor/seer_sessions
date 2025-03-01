import numpy as np

def find_objects(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    return np.argwhere(grid == color).tolist()

def find_square(grid, color):
    """Finds a 2x2 square of the specified color and returns its top-left corner coordinates."""
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == color and grid[i + 1, j] == color and
                grid[i, j + 1] == color and grid[i + 1, j + 1] == color):
                return (i, j)  # Top-left corner
    return None
    
def report(grid, tag):
    green_square_coords = find_square(grid, 3)
    blue_pixels = find_objects(grid, 1)
    magenta_pixels = find_objects(grid, 6)

    print(f"{tag}:")
    print(f"  Green Square Coords: {green_square_coords}")
    print(f"  Blue Pixels: {blue_pixels}")
    print(f"  Magenta Pixels: {magenta_pixels}")
    print(grid)

# Example data (replace with your actual data)
example_inputs = [
    np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
              [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 6, 0, 0],
              [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
             [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
             [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 6]])
]
example_outputs = [
    np.array([[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
              [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 6, 0, 0, 6, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
             [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
             [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
             [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
]

for i in range(len(example_inputs)):
  report(example_inputs[i],f"Example {i+1} Input")
  report(example_outputs[i],f"Example {i+1} Output")