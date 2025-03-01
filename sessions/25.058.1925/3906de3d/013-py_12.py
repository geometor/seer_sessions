# Example data (replace with actual data from the task)
example_grids = [
    { # example 1
        'input': np.array([[0, 0, 0, 0],
                           [0, 1, 1, 0],
                           [0, 1, 1, 0],
                           [0, 2, 2, 0]]),
        'output': np.array([[0, 1, 1, 0],
                            [0, 1, 1, 0],
                            [0, 2, 2, 0],
                            [0, 2, 2, 0]])
    },
        { # example 2
        'input': np.array([[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 2, 2, 0]]),
        'output': np.array([[0, 2, 2, 0],
                            [0, 2, 2, 0],
                            [0, 2, 2, 0],
                            [0, 2, 2, 0]])
    },
        { # example 3
        'input': np.array([[0, 0, 0, 0],
                           [0, 1, 0, 1],
                           [0, 2, 0, 2],
                           [0, 2, 0, 2]]),
        'output': np.array([[0, 1, 0, 1],
                            [0, 2, 0, 2],
                            [0, 2, 0, 2],
                            [0, 2, 0, 2]])
    },
        { # example 4 - disconnected red regions
        'input': np.array([[0, 0, 0, 0],
                           [0, 1, 1, 0],
                           [0, 0, 0, 0],
                           [2, 0, 0, 2]]),
        'output': np.array([[2, 1, 1, 2],
                           [2, 1, 1, 2],
                           [2, 0, 0, 2],
                           [2, 0, 0, 2]])
    }
]

def find_pixels(grid, color):
    """Finds the coordinates of pixels of a specific color."""
    return np.argwhere(grid == color)

def fill_upwards(grid, start_coords, boundary_color):
    """Fills the grid upwards from given start coordinates with red (2) until a boundary color or top edge is reached."""
    output_grid = np.copy(grid)
    for row, col in start_coords:
        current_row = row
        while current_row >= 0 and output_grid[current_row, col] != boundary_color:
            output_grid[current_row, col] = 2
            current_row -= 1
    return output_grid

def transform(input_grid):
    """Transforms the input grid by filling upwards from red pixels, bounded by blue."""
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find blue and red pixels
    blue_pixels = find_pixels(input_grid, 1)
    red_pixels = find_pixels(input_grid, 2)

    # Fill upwards from red pixels, bounded by blue
    output_grid = fill_upwards(output_grid, red_pixels, 1)

    return output_grid

# verify transform function against examples:
for i, example in enumerate(example_grids):
  transformed_grid = transform(example['input'])
  print(f"Example {i + 1}:")
  print(f"  Correct Result:   {np.array_equal(transformed_grid, example['output'])}")
