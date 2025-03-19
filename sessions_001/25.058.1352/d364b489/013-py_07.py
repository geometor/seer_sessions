import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right) in order."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col, "Up"))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col, "Down"))  # Down
    if col > 0:
        neighbors.append((row, col - 1, "Left"))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1, "Right"))  # Right
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Find the blue pixels in input_grid
    blue_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 1:
                blue_pixels.append((r,c))
    
    # Iterate and expand based on relative position
    color_map = {
        "Up": 2,
        "Down": 6,
        "Left": 7,
        "Right": 8
    }
    
    for r, c in blue_pixels:
        neighbors = get_neighbors(input_grid, r, c)
        
        for nr, nc, direction in neighbors:
            if output_grid[nr,nc] == 0: # if the neighbor in the output grid is white
                output_grid[nr, nc] = color_map[direction]

    return output_grid

def compare_grids(grid1, grid2):
    """Checks if two grids are identical and returns details about differences."""
    if grid1.shape != grid2.shape:
        return False, "Different shapes"
    diff = grid1 != grid2
    if np.any(diff):
        num_diffs = np.sum(diff)
        diff_indices = np.where(diff)
        diff_details = []
        for i in range(num_diffs):
            row = diff_indices[0][i]
            col = diff_indices[1][i]
            diff_details.append(f"  Pixel ({row}, {col}): Expected {grid2[row, col]}, Got {grid1[row, col]}")
        return False, f"Differences:\n" + "\n".join(diff_details)
    return True, "Identical"

# Example grids and execution results (replace with your actual data)
examples = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 2, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 7, 1, 8, 0, 0, 0, 0],
               [0, 0, 0, 6, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]])),
    
    (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 2, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0],
               [0, 0, 7, 1, 8, 0, 0],
               [0, 0, 0, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]])),
    
     (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 2, 0, 0, 0, 0],
               [0, 0, 7, 1, 8, 0, 0, 0],
               [0, 0, 0, 6, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]))
]

for i, (input_grid, expected_output) in enumerate(examples):
    transformed_grid = transform(input_grid)
    grids_equal, diff_message = compare_grids(transformed_grid, expected_output)
    print(f"Example {i+1}:")
    print(f"  Comparison Result: {'Identical' if grids_equal else 'Different'}")
    if not grids_equal:
        print(f"  {diff_message}")
    print("-" * 20)