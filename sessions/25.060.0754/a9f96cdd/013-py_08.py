import numpy as np

# Provided color map (for reference)
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

def find_colored_pixel(grid):
    # Find the coordinates of the non-zero pixel.
    rows, cols = np.where(grid != 0)
    if len(rows) > 0:  # Ensure a non-zero pixel was found
      return rows[0], cols[0], grid[rows[0], cols[0]] # return row, col, and color
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height = input_grid.shape[0]
    width = input_grid.shape[1]


    # Find the colored pixel in the input grid.
    colored_pixel_coords = find_colored_pixel(input_grid)

    if colored_pixel_coords:
      # change output pixels
      row, col, color = colored_pixel_coords
      new_row = (row - 1) % height # wrap rows
      new_col = (col - 1) % width # wrap cols
      new_color = {
          2: 3,  # Red to Green
          3: 4,  # Green to Yellow
          4: 2,  # Yellow to Red
      }.get(color)
      output_grid[new_row, new_col] = new_color


    return output_grid