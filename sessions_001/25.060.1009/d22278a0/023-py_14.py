import numpy as np

def get_seed_pixels(grid):
    # Find the coordinates of all non-white pixels.
    seed_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                seed_pixels.append((r, c, grid[r, c]))
    return seed_pixels

def transform(input_grid):
    # Initialize the output grid with the same dimensions and filled with white (0).
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Get the seed pixels and their colors.
    seed_pixels = get_seed_pixels(input_grid)

    # Controlled flood fill for each seed pixel.
    for r, c, color in seed_pixels:
        output_grid[r, c] = color # original location
        if color == 1:  # Top-left blue (1)
            if c + 1 < cols:
              output_grid[r,c+1] = color
            if r + 1 < rows:
              output_grid[r+1,c] = color
            if r + 2 < rows:
              output_grid[r+2,c] = color
            if r + 1 < rows and c+1 < cols:
                output_grid[r+1,c+1] = color


        elif color == 2:  # Top-right red (2)
            if c - 1 >= 0:
                output_grid[r, c - 1] = color
            if r + 1 < rows:
                output_grid[r + 1, c] = color
            if r + 2 < rows:
                output_grid[r + 2, c] = color
            if r+1 < rows and c-1 >=0:
                output_grid[r+1, c-1] = color

        elif color == 8:  # Bottom-left azure (8)
           if c + 1 < cols:
                output_grid[r, c + 1] = color  # right
           if r - 1 >= 0:
                output_grid[r - 1, c] = color  # up
           if r - 1 >= 0 and c + 1 < cols:
                output_grid[r - 1, c + 1] = color # diagonal up-right
           if r-2 >= 0 and c+2 < cols:
                output_grid[r-2, c+2] = color

    # special handling to fill to middle
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 8:
              if r - 1 >= 0:
                output_grid[r-1,c] = 8
              if c + 1 < cols:
                output_grid[r, c+1] = 8
              if r-1 >=0 and c+1 < cols:
                output_grid[r-1,c+1] = 8

    return output_grid

def compare_grids(grid1, grid2):
    return np.array_equal(grid1, grid2)

# Example grids (replace with your actual data)
train = [
    {
        "input": np.array([[1, 0, 2], [0, 0, 0], [8, 0, 0]]),
        "output": np.array([[1, 2, 2], [1, 8, 2], [8, 8, 8]]),
    },
    {
        "input": np.array([[0, 0, 0, 2], [0, 0, 0, 0], [8, 0, 0, 0], [0, 0, 0, 0]]),
        "output": np.array([[8, 8, 8, 2], [8, 8, 8, 2], [8, 8, 8, 2], [8, 8, 8, 0]]),
    },
    {
        "input": np.array([[0, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [8, 0, 0, 0]]),
        "output": np.array([[8, 8, 2, 0], [8, 8, 2, 0], [8, 8, 0, 0], [8, 8, 0, 0]]),
    },
]

for i, example in enumerate(train):
    transformed_grid = transform(example["input"])
    print(f"Example {i+1}:")
    print("Input:")
    print(example["input"])
    print("Expected Output:")
    print(example["output"])
    print("Transformed Output:")
    print(transformed_grid)
    print("Match:", compare_grids(transformed_grid, example["output"]))
    print("---")