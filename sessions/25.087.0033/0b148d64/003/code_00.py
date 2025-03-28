import numpy as np
from collections import Counter

"""
Identify the first continuous horizontal band of all-white pixels (0) spanning the grid width. This separates the grid into an Upper Region (above the band) and a Lower Region (below the band). 
Within the Upper Region, identify the widest, leftmost vertical band of all-white pixels that spans the full height of the Upper Region. This vertical band starts at column `c_start` and ends at column `c_end`.
Divide the Upper Region into a Left Side (columns 0 to `c_start`-1) and a Right Side (columns `c_end`+1 to end). Count non-white pixels in each side (`count_L`, `count_R`). Find the most frequent non-white color (`dominant_color`) in the entire Upper Region.
Select columns based on counts and dominant color: If `dominant_color` is Blue (1), choose the side (Left or Right) with the *smaller* count. Otherwise, choose the side with the *larger* count. If counts are equal, choose the wider side. If widths are also equal, choose the Right side.
The output grid consists of all rows from the Lower Region, using only the columns corresponding to the selected side (Left or Right).
"""

def find_horizontal_separator(grid):
    """
    Finds the start and end row indices of the first continuous horizontal
    band of all-white pixels (0).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple (int, int): The start and end row indices (inclusive). 
                         Returns (-1, -1) if no such band is found.
    """
    height, width = grid.shape
    r_start = -1
    r_end = -1
    in_separator = False

    for r in range(height):
        is_white_row = np.all(grid[r, :] == 0)
        if is_white_row and not in_separator:
            r_start = r
            r_end = r
            in_separator = True
        elif is_white_row and in_separator:
            r_end = r
        elif not is_white_row and in_separator:
            # Found the end of the first separator
            return r_start, r_end
        # Continue if not white row and not yet in separator
        
    # If separator goes to the bottom edge or exists
    if r_start != -1:
        return r_start, r_end
    else:
        return -1, -1

def find_vertical_separator(upper_region):
    """
    Finds the widest, leftmost, full-height vertical white band in the 
    upper region.

    Args:
        upper_region (np.ndarray): The upper portion of the grid.

    Returns:
        tuple (int, int): The start and end column indices (inclusive) of the
                          selected band. Returns (-1, -1) if none found.
    """
    if upper_region.size == 0: # Handle empty upper region
        return -1, -1
        
    upper_height, upper_width = upper_region.shape
    if upper_height == 0:
        return -1, -1

    white_cols = []
    # Identify all columns that are fully white
    for c in range(upper_width):
        if np.all(upper_region[:, c] == 0):
            white_cols.append(c)

    if not white_cols:
        return -1, -1

    # Group consecutive columns into bands
    bands = []
    current_band = [white_cols[0]]
    for i in range(1, len(white_cols)):
        if white_cols[i] == white_cols[i-1] + 1:
            current_band.append(white_cols[i])
        else:
            bands.append(current_band)
            current_band = [white_cols[i]]
    bands.append(current_band)

    # Find the widest band(s)
    max_len = 0
    for band in bands:
        if len(band) > max_len:
            max_len = len(band)

    widest_bands = [band for band in bands if len(band) == max_len]

    # If tie in width, choose the leftmost one
    best_band = min(widest_bands, key=lambda band: band[0])

    c_start = best_band[0]
    c_end = best_band[-1]
    
    return c_start, c_end

def get_dominant_color(region):
    """
    Finds the most frequent non-white color in a region.

    Args:
        region (np.ndarray): The grid region to analyze.

    Returns:
        int or None: The dominant color code, or None if the region is empty 
                     or contains only white pixels.
    """
    if region.size == 0:
        return None
        
    non_white_pixels = region[region != 0]
    if non_white_pixels.size == 0:
        return None

    color_counts = Counter(non_white_pixels)
    # Find the color with the highest count. If ties, Counter returns one arbitrarily.
    dominant_color = color_counts.most_common(1)[0][0] 
    return int(dominant_color) # Ensure it's a standard int


def transform(input_grid):
    """
    Transforms the input grid based on the specified rules involving horizontal
    and vertical separators and pixel counts/colors in the upper region.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # 1. Identify Horizontal Split
    r_start, r_end = find_horizontal_separator(grid)

    if r_start == -1 or r_end >= height - 1:
        # Cannot proceed if no separator or no lower region
        return np.array([[]], dtype=int) 

    upper_region = grid[:r_start, :]
    lower_region = grid[r_end + 1:, :]

    if upper_region.shape[0] == 0:
         # Cannot proceed if no upper region
         return np.array([[]], dtype=int) 

    # 2. Identify Vertical Split in Upper Region
    c_start, c_end = find_vertical_separator(upper_region)

    if c_start == -1:
         # Cannot proceed without a vertical separator
         return np.array([[]], dtype=int)

    # 3. Analyze Upper Sides
    upper_left = upper_region[:, :c_start]
    upper_right = upper_region[:, c_end + 1:]

    count_L = np.count_nonzero(upper_left)
    count_R = np.count_nonzero(upper_right)
    
    width_L = upper_left.shape[1]
    width_R = upper_right.shape[1]

    dominant_color = get_dominant_color(upper_region)
    
    if dominant_color is None:
         # Cannot determine rule without dominant color (e.g., upper region is all white)
         # Default behavior? Based on examples, this shouldn't happen. Return empty.
         return np.array([[]], dtype=int)

    # 4. Choose Output Columns
    selected_side = "Right" # Default for tie-breaking width

    if dominant_color == 1: # Blue Rule
        if count_L < count_R:
            selected_side = "Left"
        elif count_R < count_L:
            selected_side = "Right"
        else: # Counts equal - tie break on width
            if width_L > width_R:
                selected_side = "Left"
            # If width_R > width_L or widths equal, keep "Right" default
            
    else: # Standard Rule (Not Blue)
        if count_L > count_R:
            selected_side = "Left"
        elif count_R > count_L:
            selected_side = "Right"
        else: # Counts equal - tie break on width
            if width_L > width_R:
                selected_side = "Left"
            # If width_R > width_L or widths equal, keep "Right" default

    # 5. Extract Output from Lower Region
    if selected_side == "Left":
        # Check if left side exists (c_start > 0)
        if c_start > 0:
             output_grid = lower_region[:, :c_start]
        else:
             # No columns to the left, return empty
             output_grid = np.array([[]], dtype=int) if lower_region.shape[0] > 0 else np.array([], dtype=int).reshape(0,0)
             # Adjust empty shape based on lower_region height
             if lower_region.shape[0] > 0:
                 output_grid = np.empty((lower_region.shape[0], 0), dtype=int)
             else: # lower_region was also empty
                 output_grid = np.empty((0,0), dtype=int)

    else: # selected_side == "Right"
        # Check if right side exists (c_end < width - 1)
        if c_end < width - 1:
            output_grid = lower_region[:, c_end + 1:]
        else:
            # No columns to the right, return empty
            # Adjust empty shape based on lower_region height
             if lower_region.shape[0] > 0:
                 output_grid = np.empty((lower_region.shape[0], 0), dtype=int)
             else: # lower_region was also empty
                 output_grid = np.empty((0,0), dtype=int)


    # Ensure output is 2D, even if empty
    if output_grid.ndim == 1:
        # This might happen if lower_region had only 1 row and output is empty cols
         output_grid = output_grid.reshape(1, -1) 
    if output_grid.size == 0 and lower_region.shape[0] > 0 and output_grid.shape[1] != 0:
         # Correct shape for empty columns but existing rows
         output_grid = np.empty((lower_region.shape[0], 0), dtype=int)
    elif output_grid.size == 0 and lower_region.shape[0] == 0:
         # Correct shape for no rows, no cols
         output_grid = np.empty((0,0), dtype=int)


    return output_grid