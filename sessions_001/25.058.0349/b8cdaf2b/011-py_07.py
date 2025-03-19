import numpy as np

def find_pixels_by_color(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find all green pixels (color 3)
    green_pixel_coords = find_pixels_by_color(input_grid, 3)

    if len(green_pixel_coords) > 0:
        for green_pixel_coord in green_pixel_coords:
            # Get the column index of the current green pixel
            green_col = green_pixel_coord[1]

            # Iterate through rows above the green pixel, changing them to green
            for row in range(green_pixel_coord[0] - 1, -1, -1):
                output_grid[row, green_col] = 3

    return output_grid
  

# Provided training examples
train_examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 5, 3, 5, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 5, 3, 5, 0, 0, 0, 0, 0, 0], [0, 5, 3, 5, 0, 0, 0, 0, 0, 0], [0, 5, 3, 5, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 5, 3, 0], [0, 0, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 5, 3, 0], [0, 0, 0, 0, 0, 5, 3, 0], [0, 0, 0, 0, 0, 5, 3, 0], [0, 0, 0, 0, 0, 5, 3, 0], [0, 0, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 5, 3, 5, 0], [0, 0, 0, 0, 0, 0, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 5, 3, 5, 0], [0, 0, 0, 0, 0, 0, 5, 3, 5, 0], [0, 0, 0, 0, 0, 0, 5, 3, 5, 0], [0, 0, 0, 0, 0, 0, 5, 3, 5, 0], [0, 0, 0, 0, 0, 0, 5, 3, 5, 0], [0, 0, 0, 0, 0, 0, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    },
    {
        "input" : [[0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 6, 0, 0],
                   [0, 0, 0, 0, 6, 0, 0],
                   [0, 0, 0, 0, 3, 0, 0],
                   [0, 0, 0, 0, 6, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 3, 0, 0],
                   [0, 0, 0, 0, 3, 0, 0],
                   [0, 0, 0, 0, 3, 0, 0],
                   [0, 0, 0, 0, 3, 0, 0],
                   [0, 0, 0, 0, 6, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0]]

    }
]

# Iterate through each example
for i, example in enumerate(train_examples):
    input_grid = np.array(example["input"])
    expected_output = np.array(example["output"])
    actual_output = transform(input_grid)
    
    print(f"Example {i+1}:")

    if np.array_equal(actual_output,expected_output):
      print("  transform successful")
    else:
      print("  transform failed")
      
    green_pixels_input = find_pixels_by_color(input_grid, 3)
    print(f"  Green Pixels (Input): {green_pixels_input}")

    if len(green_pixels_input) > 0:
        for coord in green_pixels_input:
            row, col = coord
            print(f"    examining green pixel at {row},{col}")
            if row > 0:
              above = input_grid[row-1,col]
              print(f"      pixel above: {above}")
            else:
              print(f"      pixel above: None")
              
            if row < input_grid.shape[0] - 1:    
              below = input_grid[row+1,col]
              print(f"      pixel below: {below}")
            else:
              print(f"      pixel below: None")


    print("-----")