import numpy as np

def find_all_pixels(grid, color):
    coords = np.where(grid == color)
    return list(zip(coords[0], coords[1]))

def analyze_example(input_grid, output_grid):
    red_pixels = find_all_pixels(input_grid, 2)
    green_pixels = find_all_pixels(input_grid, 3)
    expected_azure_pixels = find_all_pixels(output_grid, 8)
    actual_azure_pixels = find_all_pixels(transform(input_grid), 8)

    print(f"Red Pixels: {red_pixels}")
    print(f"Green Pixels: {green_pixels}")
    print(f"Expected Azure Pixels: {expected_azure_pixels}")
    print(f"Actual Azure Pixels: {actual_azure_pixels}")
    print("---")
    
def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the red and green pixels
    red_pixel_pos = find_pixel(input_grid, 2)
    green_pixel_pos = find_pixel(input_grid, 3)

    if red_pixel_pos is None or green_pixel_pos is None:
        return output_grid # if not found - return the grid
    
    if red_pixel_pos[0] >= green_pixel_pos[0]:
        return output_grid # red must be above green

    # Determine the column and rows for the azure line
    column = green_pixel_pos[1]
    start_row = red_pixel_pos[0]
    end_row = green_pixel_pos[0] - 1

    # Draw the azure line
    for row in range(start_row, end_row + 1):
        output_grid[row, column] = 8

    return output_grid

def find_pixel(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]  # Return row, col
    return None

# Load the example data (replace with actual data loading)
# Assuming examples are stored in a list called 'examples'
# where each example is a tuple (input_grid, output_grid)

examples = [
    (np.array([[5, 0, 5, 5, 5, 5, 5, 5, 5],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 2, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 3],
               [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
     np.array([[5, 0, 5, 5, 5, 5, 5, 5, 5],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 8, 0, 0, 0, 0],
               [0, 0, 0, 0, 8, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 3],
               [5, 5, 5, 5, 5, 5, 5, 5, 5]])),
    (np.array([[5, 0, 5, 5, 5, 5, 5, 5, 5],
               [0, 0, 0, 0, 0, 0, 2, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 2, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 3, 0, 0, 0, 0, 0, 3],
               [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
     np.array([[5, 0, 5, 5, 5, 5, 5, 5, 5],
               [0, 0, 0, 0, 0, 0, 2, 0, 0],
               [0, 0, 8, 0, 0, 0, 0, 0, 0],
               [0, 0, 8, 0, 2, 0, 0, 0, 0],
               [0, 0, 8, 0, 0, 0, 0, 0, 0],
               [0, 0, 3, 0, 0, 0, 0, 0, 3],
               [5, 5, 5, 5, 5, 5, 5, 5, 5]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 2, 0, 0, 0, 0, 0, 2, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 3, 0, 0, 0, 0, 0, 3, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 2, 0, 0, 0, 0, 0, 2, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 3, 0, 0, 0, 0, 0, 3, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]))
]


for input_grid, output_grid in examples:
    analyze_example(input_grid, output_grid)