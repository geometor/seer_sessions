import numpy as np

def find_target_color(grid):
  """
  Finds the unique color in the grid that is not white (0), blue (1), or yellow (4).
  Returns None if no such unique color exists.
  """
  unique_colors = np.unique(grid)
  target_candidates = [color for color in unique_colors if color not in [0, 1, 4]]
  if len(target_candidates) == 1:
    return target_candidates[0]
  else:
    # Handle cases where there isn't exactly one target color if necessary
    # Based on examples, we expect exactly one.
    # Returning None might indicate an unexpected input format.
    print(f"Warning: Expected 1 target color, found {len(target_candidates)}: {target_candidates}")
    return None # Or raise an error, depending on desired behavior


def transform(input_grid):
    """
    Transforms the input grid according to the following rules:
    1. Identifies a "target" color (unique color != 0, 1, 4) from the input grid.
    2. Divides the grid into 3x3 subgrids separated by yellow (4) lines.
    3. For each 3x3 subgrid containing blue (1) pixels:
        a. Finds the blue pixel with the minimum row index within the subgrid.
        b. If multiple blue pixels share the minimum row index, selects the one with the minimum column index.
        c. Changes the color of this selected blue pixel to the identified "target" color.
    4. All other pixels remain unchanged.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid)
    output_grid = grid_np.copy()
    height, width = grid_np.shape

    # 1. Identify the target color
    target_color = find_target_color(grid_np)
    if target_color is None:
        # If no clear target color, return the original grid or handle error
        print("Warning: No unique target color found. Returning original grid.")
        return output_grid.tolist() # return list of lists format

    # 2. Iterate through the grid, identifying the top-left corners of 3x3 subgrids
    # The subgrids start at rows 0, 4, 8, ... and columns 0, 4, 8, ...
    for r in range(0, height, 4):
        for c in range(0, width, 4):
            # Ensure we don't go out of bounds for the 3x3 subgrid
            if r + 3 > height or c + 3 > width:
                continue

            # 3. Process each 3x3 subgrid
            subgrid = grid_np[r:r+3, c:c+3]

            # a. Find all blue (1) pixels within that subgrid
            blue_pixels_coords = np.argwhere(subgrid == 1) # Gives coordinates relative to subgrid

            # b. If no blue pixels are present, proceed to the next subgrid
            if blue_pixels_coords.size == 0:
                continue

            # c. Determine the minimum row index among blue pixels (relative to subgrid)
            min_subgrid_row = np.min(blue_pixels_coords[:, 0])

            # d. Identify all blue pixels located at this minimum row index
            top_blue_pixels_coords = blue_pixels_coords[blue_pixels_coords[:, 0] == min_subgrid_row]

            # e. Among these, determine the minimum column index
            min_subgrid_col = np.min(top_blue_pixels_coords[:, 1])

            # f. Locate the single blue pixel at this min row/col index within the subgrid
            # Calculate the coordinates in the main output grid
            target_row_in_grid = r + min_subgrid_row
            target_col_in_grid = c + min_subgrid_col

            # g. Change the color of this identified blue pixel to the target color
            output_grid[target_row_in_grid, target_col_in_grid] = target_color

    # 4. Return the modified grid as a list of lists
    return output_grid.tolist()