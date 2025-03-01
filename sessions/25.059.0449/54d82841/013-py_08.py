import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    
    # Find changed pixel
    changed_pixels = np.argwhere(input_grid != output_grid)
    if len(changed_pixels) == 0:
        return None  # No change

    changed_pixel = changed_pixels[0]
    
    # Green Pixels and Bottom Row
    green_coords = np.argwhere(input_grid == 3)
    if len(green_coords) ==0:
        bottom_most_green_row = -1
        bottom_most_green_col = -1
    else:
      bottom_most_green_row = np.max(green_coords[:, 0])
      # Find the columns of the bottom-most green pixels
      green_in_bottom_row_cols = green_coords[green_coords[:, 0] == bottom_most_green_row, 1]
      # the assumption here is the lowest and left-most green pixel on the bottom-most row
      bottom_most_green_col = np.min(green_in_bottom_row_cols)

    # Find the column index of the target pixel
    target_col = changed_pixel[1]

    # calculate if directly below
    directly_below = False
    if bottom_most_green_row + 1 == changed_pixel[0]:
        directly_below = True

    return {
      'changed_pixel': changed_pixel.tolist(),
      'bottom_most_green_row': int(bottom_most_green_row),
      'bottom_most_green_col': int(bottom_most_green_col),
      'target_col': int(target_col),
      'directly_below': directly_below,
    }

examples = [
    ([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 3, 0], [0, 0, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
]

analysis_results = [analyze_example(in_grid, out_grid) for in_grid, out_grid in examples]
print(analysis_results)