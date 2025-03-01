import numpy as np

def find_vertical_line(grid, color):
    """Finds the starting row and column index of a vertical line of the specified color."""
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == color:
                # Check if it's a vertical line
                if i + 1 < rows and grid[i + 1, j] == color:
                    return i, j
    return None, None

def get_vertical_line_pixels(grid, col, color):
     """Extracts the pixels of vertical line"""
     rows = grid.shape[0]
     pixels = []
     for i in range(rows):
        if grid[i, col] == color:
            pixels.append((i, col))
     return pixels
    

def find_red_pixels(grid):
    """Finds all red pixels in the grid."""
    rows, cols = grid.shape
    red_pixels = []
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 2:
                red_pixels.append((i, j))
    return red_pixels

def transform(input_grid):
    # Find the green line
    green_start_row, green_col = find_vertical_line(input_grid, 3)
    green_pixels = get_vertical_line_pixels(input_grid, green_col, 3)

    # Find the azure line
    azure_start_row, azure_col = find_vertical_line(input_grid, 8)
    azure_pixels = get_vertical_line_pixels(input_grid, azure_col, 8)

    # Find red pixels
    red_pixels = find_red_pixels(input_grid)

    # Select red pixels to the *right* of the azure line
    selected_red_pixels = [p for p in red_pixels if p[1] > azure_col]
    
    # Determine the output grid dimensions based on selected pixels only
    min_row = min(min(p[0] for p in green_pixels), min(p[0] for p in azure_pixels), min(p[0] for p in selected_red_pixels if p))
    max_row = max(max(p[0] for p in green_pixels), max(p[0] for p in azure_pixels), max(p[0] for p in selected_red_pixels if p))

    output_height = max_row - min_row + 1
    output_width = 2  # Initialize with width for green and azure lines

    # Initialize the output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place the green line in the first column
    for i in range(len(green_pixels)):
        row_in_grid = green_pixels[i][0]
        output_grid[row_in_grid - min_row, 0] = 3

    # Place the azure line in the last column
    for i in range(len(azure_pixels)):
      row_in_grid = azure_pixels[i][0]
      output_grid[row_in_grid - min_row, output_width - 1] = 8

    # If there are red pixels *right of the azure line, add columns and fill them*
    if len(selected_red_pixels) > 0:
        #resize, adding columns for each red pixel
        output_width += len(set([p[1] for p in selected_red_pixels]))
        output_grid = np.zeros((output_height, output_width), dtype=int)

        #re-add green line
        for i in range(len(green_pixels)):
          row_in_grid = green_pixels[i][0]
          output_grid[row_in_grid - min_row, 0] = 3

        #re-add azure
        for i in range(len(azure_pixels)):
          row_in_grid = azure_pixels[i][0]
          output_grid[row_in_grid - min_row, output_width - 1] = 8

        #fill red, starting at column 1
        red_col_offset = 1
        red_cols = sorted(list(set([p[1] for p in selected_red_pixels])))

        for col in red_cols:
          for pixel in selected_red_pixels:
            if pixel[1] == col:
               output_grid[pixel[0] - min_row, red_col_offset] = 2
          red_col_offset+=1 #increment each time a column of reds has been added

    return output_grid

# Load the task data (replace with actual path)
task_data = {
 "train": [
  {"input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 8, 0, 0], [0, 0, 0, 0, 3, 0, 0, 8, 0, 0], [0, 0, 0, 0, 3, 0, 0, 8, 0, 2], [0, 0, 0, 0, 3, 0, 0, 8, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]), "output": np.array([[3, 0, 8], [3, 0, 8], [3, 0, 8], [3, 2, 8], [3, 0, 8]])},
  {"input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 8, 0, 0, 2], [0, 0, 0, 0, 0, 3, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]), "output": np.array([[3, 0, 8], [3, 0, 8], [3, 2, 8], [3, 0, 8]])},
  {"input": np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 8, 2, 2, 0], [0, 0, 0, 0, 3, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]), "output": np.array([[3, 0, 8], [3, 0, 8], [3, 0, 8], [3, 2, 8], [3, 0, 8]])},
 ],
 "test": [
  {"input": np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 8, 0, 2], [0, 0, 0, 0, 3, 0, 0, 8, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])}
 ]
}

for i, example in enumerate(task_data["train"]):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"Input:\n{input_grid}")
    print(f"Expected Output:\n{expected_output}")
    print(f"Predicted Output:\n{predicted_output}")
    print(f"Equal: {np.array_equal(expected_output, predicted_output)}")
    print("-" * 20)
