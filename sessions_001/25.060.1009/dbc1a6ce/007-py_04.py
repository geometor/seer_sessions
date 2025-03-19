import numpy as np
def get_grid_dimensions(grid):
    return grid.shape

def count_pixels_by_color(grid):
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

def check_cross_center(input_grid, output_grid, color_map):
    """Checks if azure crosses are centered on blue pixels, accounts for different arm lengths."""
    blue_pixels = np.argwhere(input_grid == 1)
    cross_centers = []
    for r, c in blue_pixels:
       
        #check directly adjacent
        up = input_grid[r-1,c] if r-1 >= 0 else -1
        down = input_grid[r+1,c] if r+1 < input_grid.shape[0] else -1
        left = input_grid[r,c-1] if c-1 >= 0 else -1
        right = input_grid[r,c+1] if c+1 < input_grid.shape[1] else -1

        if (
            (up == 0 or up == 8) and
            (down == 0 or down == 8) and
            (left == 0 or left == 8) and
            (right == 0 or right == 8)
           ):
            cross_centers.append((r,c))

    valid = True
    for r, c in cross_centers:
        #check if the cross center is azure in the output
        if output_grid[r,c] != 1:
            valid = False

    return valid, cross_centers

# Example grids (replace with actual grids from the task)
example_inputs = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 5, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[6, 0, 0, 0, 0, 6],
              [0, 0, 1, 0, 0, 0],
              [6, 0, 0, 0, 0, 6]]),
    np.array([[6, 0, 6, 0, 0, 6],
             [0, 1, 0, 0, 0, 0],
            [6, 0, 0, 6, 0, 6]]),
    np.array([[0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0]])
]

example_outputs = [
    np.array([[0, 0, 8, 0, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 8, 0, 0, 0]]),
    np.array([[0, 0, 8, 0, 5, 0],
              [0, 0, 1, 0, 5, 0],
              [0, 0, 8, 0, 0, 0]]),
    np.array([[6, 0, 8, 0, 0, 6],
              [0, 0, 1, 0, 0, 0],
              [6, 0, 8, 0, 0, 6]]),
    np.array([[6, 8, 6, 0, 0, 6],
             [0, 1, 8, 0, 0, 0],
            [6, 8, 6, 6, 0, 6]]),
    np.array([[8, 8, 8, 1, 8, 8],
              [0, 0, 0, 8, 0, 0],
              [8, 1, 8, 8, 8, 8],
              [0, 8, 0, 0, 0, 0],
              [8, 8, 8, 1, 8, 8]])
]

COLOR_MAP = {
    0: (238, 238, 238),  # white
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}
results = []

for i, (input_grid, output_grid) in enumerate(zip(example_inputs, example_outputs)):
    dimensions = get_grid_dimensions(input_grid)
    input_colors = count_pixels_by_color(input_grid)
    output_colors = count_pixels_by_color(output_grid)
    cross_check_valid, cross_centers = check_cross_center(input_grid, output_grid, COLOR_MAP)

    results.append({
        "example": i + 1,
        "dimensions": dimensions,
        "input_colors": input_colors,
        "output_colors": output_colors,
        "cross_check_valid": cross_check_valid,
        "cross_centers_found": cross_centers
    })
    
for r in results:
    print(r)