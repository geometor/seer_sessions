import numpy as np

def _get_square_coords(center_row, center_col, height, width):
    """Calculates the coordinates of a 3x3 square given the center and grid dimensions."""
    coords = []
    for i in range(max(0, center_row - 1), min(height, center_row + 2)):
        for j in range(max(0, center_col - 1), min(width, center_col + 2)):
            coords.append((i, j))
    return coords

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    print(f"Input grid size: {height}x{width}")

    # 1. Identify Red and Green Pixels
    red_pixels = []
    green_pixels = []
    for i in range(height):
        for j in range(width):
            if input_grid[i, j] == 2:
                red_pixels.append((i, j))
            elif input_grid[i, j] == 3:
                green_pixels.append((i, j))

    print(f"Red pixels: {red_pixels}")
    print(f"Green pixels: {green_pixels}")

    # 2. Create Squares (Red)
    red_squares = []
    for r_row, r_col in red_pixels:
        square_coords = _get_square_coords(r_row, r_col, height, width)
        red_squares.append(square_coords)
        for r_i, r_j in square_coords:
            output_grid[r_i, r_j] = 2

    # 2. Create Squares (Green)
    green_squares = []
    for g_row, g_col in green_pixels:
        square_coords = _get_square_coords(g_row, g_col, height, width)
        green_squares.append(square_coords)
        for g_i, g_j in square_coords:
            output_grid[g_i, g_j] = 3


    # 3. Handle Overlap
    for i in range(height):
        for j in range(width):
            in_red_square = False
            in_green_square = False

            for red_square in red_squares:
                if (i, j) in red_square:
                    in_red_square = True
                    break  # Optimization: Once found, no need to check other red squares

            for green_square in green_squares:
                if (i, j) in green_square:
                    in_green_square = True
                    break  # Optimization

            if in_red_square and in_green_square:
                output_grid[i, j] = 5

    print(f"Output grid size (before resizing): {output_grid.shape}")

    return output_grid.tolist()

# Example Usage with print output for each example
task_id = "6b6f9c1b"
train_test = "train"

task = ARC_task(task_id, train_test)
for i, example in enumerate(task.examples):
  print(f'example: {i}')
  input_grid = example['input']
  output_grid = example['output']
  print(f"Expected output grid size: {np.array(output_grid).shape}")
  result = transform(input_grid)