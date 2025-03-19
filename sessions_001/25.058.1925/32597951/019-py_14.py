import numpy as np

# Provided helper functions (get_neighbors, find_frame_color, find_inner_pixels) - assumed to be defined above.
def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def find_frame_color(grid):
    """ Assumes a rectangular, framed grid and returns the frame color.
        We'll just check the top-left pixel.
    """
    return grid[0,0]

def find_inner_pixels(grid, frame_color):
    """Finds pixels adjacent to the frame."""
    rows, cols = grid.shape
    inner_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] != frame_color:
                for nr, nc in get_neighbors(grid, r, c):
                    if grid[nr, nc] == frame_color:
                        inner_pixels.append( (r,c) )
                        break # Optimization, don't add the same pixel twice
    return inner_pixels
# --- End of helper functions

train = [
    {'input': np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 3, 3, 3, 8, 3, 3, 8], [8, 3, 3, 3, 8, 3, 3, 8], [8, 8, 8, 8, 8, 8, 8, 8]]), 'output': np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 1, 1, 1, 8, 1, 1, 8], [8, 1, 1, 1, 8, 1, 1, 8], [8, 8, 8, 8, 8, 8, 8, 8]])},
    {'input': np.array([[8, 8, 8, 8, 8, 8], [8, 5, 5, 5, 5, 8], [8, 5, 5, 5, 5, 8], [8, 8, 8, 8, 8, 8]]), 'output': np.array([[8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 8], [8, 8, 8, 8, 8, 8]])},
    {'input': np.array([[8, 8, 8, 8, 8], [8, 7, 7, 7, 8], [8, 7, 2, 7, 8], [8, 7, 7, 7, 8], [8, 8, 8, 8, 8]]), 'output': np.array([[8, 8, 8, 8, 8], [8, 0, 0, 0, 8], [8, 0, 2, 0, 8], [8, 0, 0, 0, 8], [8, 8, 8, 8, 8]])},
    {'input': np.array([[8, 8, 8, 8, 8, 8, 8], [8, 3, 3, 3, 3, 3, 8], [8, 3, 3, 3, 3, 3, 8], [8, 3, 3, 3, 3, 3, 8], [8, 8, 8, 8, 8, 8, 8]]), 'output': np.array([[8, 8, 8, 8, 8, 8, 8], [8, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 8], [8, 8, 8, 8, 8, 8, 8]])},
    {'input': np.array([[8, 8, 8, 8, 8, 8], [8, 4, 4, 8, 2, 2, 8], [8, 8, 8, 8, 8, 8]]), 'output': np.array([[8, 8, 8, 8, 8, 8], [8, 4, 4, 8, 5, 5, 8], [8, 8, 8, 8, 8, 8]])}
]


def analyze_transformations(train_data):
    """Analyzes all training examples to determine the color transformations."""
    results = []
    for example in train_data:
        input_grid = example['input']
        output_grid = example['output']
        frame_color = find_frame_color(input_grid)
        inner_pixels = find_inner_pixels(input_grid, frame_color)
        
        transformations = {}
        for r, c in inner_pixels:
            input_color = input_grid[r, c]
            output_color = output_grid[r, c]
            transformations[(r,c)] = (input_color, output_color)

        results.append(transformations)
    return results

transformation_results = analyze_transformations(train)
for i, res in enumerate(transformation_results):
    print(f"Example {i+1}:")
    print(res)