import numpy as np

train_examples = [
    (np.array([[0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 6, 6, 6, 0],
               [0, 0, 6, 6, 6, 0],
               [0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0],
               [0, 0, 4, 4, 4, 0],
               [0, 4, 6, 6, 6, 4],
               [0, 4, 6, 6, 6, 4],
               [0, 0, 4, 4, 4, 0]])),

    (np.array([[0, 0, 0, 0, 0],
               [0, 6, 6, 6, 0],
               [0, 0, 0, 0, 0]]),
     np.array([[4, 4, 4, 4, 4],
               [4, 6, 6, 6, 4],
               [4, 4, 4, 4, 4]])),

     (np.array([[0, 0, 6, 0, 0],
                [0, 6, 6, 6, 0],
                [0, 0, 6, 0, 0]]),
      np.array([[4, 4, 6, 4, 4],
                [4, 6, 6, 6, 4],
               [4, 4, 6, 4, 4]]))
]

test_examples = [
    (np.array([[0, 0, 0, 0],
              [0, 6, 6, 0],
              [0, 6, 6, 0],
              [0, 0, 0, 0]]),
    np.array([[0, 4, 4, 0],
              [4, 6, 6, 4],
              [4, 6, 6, 4],
             [0, 4, 4, 0]]))
]


def analyze_example(input_grid, expected_output, transformed_grid):
    magenta_coords_input = np.argwhere(input_grid == 6)
    magenta_coords_expected = np.argwhere(expected_output == 6)
    yellow_coords_expected = np.argwhere(expected_output == 4)
    yellow_coords_transformed = np.argwhere(transformed_grid == 4)

    print("Magenta Shape Input Coordinates:\n", magenta_coords_input)
    print("Magenta Shape Expected Coordinates:\n", magenta_coords_expected)
    print("Yellow Pixels Expected Count:", len(yellow_coords_expected))
    print("Yellow Pixels Transformed Count:", len(yellow_coords_transformed))
    print("Yellow Pixels Difference (Expected - Transformed):\n",
          yellow_coords_expected.shape[0]- yellow_coords_transformed.shape[0])
    is_correct = np.array_equal(transformed_grid, expected_output)
    print("Correct:", is_correct)

def transform(input_grid):
    # Find the magenta shape
    magenta_coords = find_magenta_shape(input_grid)

    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Overlay Yellow Inside
    output_grid = overlay_yellow_inside(output_grid, magenta_coords)

    # Overlay Border
    output_grid = overlay_border(output_grid, magenta_coords)

    return output_grid

def find_magenta_shape(grid):
    # Find coordinates of all magenta pixels
    magenta_coords = np.argwhere(grid == 6)
    return magenta_coords

def overlay_yellow_inside(grid, magenta_coords):
    # Create a copy of the grid to modify
    new_grid = np.copy(grid)
    for r, c in magenta_coords:
        if r > 0 and grid[r-1,c] == 0:
          new_grid[r-1, c] = 4  # Set pixel above to yellow
    return new_grid

def overlay_border(grid, magenta_coords):
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    for r, c in magenta_coords:
        # Check adjacent pixels
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                new_grid[nr, nc] = 4

        #check for horizontal, and extend
        if 0 <= r-1 < rows and 0 <= c+1 < cols and grid[r-1,c+1] == 0 and grid[r,c+1] == 6:
            if 0 <= r-2 < rows and 0 <= c+1 < cols:
                new_grid[r-2,c+1] = 4
        if 0 <= r-1 < rows and 0 <= c-1 < cols and grid[r-1,c-1] == 0 and grid[r,c-1] == 6:
            if 0 <= r-2 < rows and 0<= c-1 < cols:
                new_grid[r-2,c-1] = 4

    return new_grid

# Analyze each training example
for i, (input_grid, expected_output) in enumerate(train_examples):
    print(f"\n--- Analyzing Training Example {i+1} ---")
    transformed_grid = transform(input_grid)
    analyze_example(input_grid, expected_output, transformed_grid)

# Analyze each test example
for i, (input_grid, expected_output) in enumerate(test_examples):
    print(f"\n--- Analyzing Test Example {i+1} ---")
    transformed_grid = transform(input_grid)
    analyze_example(input_grid, expected_output, transformed_grid)
