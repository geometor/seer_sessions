import numpy as np

"""
Identifies the minimal bounding box of the contiguous azure (8) object in the 
input grid. Extracts this pattern. Counts the number of yellow (4) pixels (N) 
in the input grid. Adjusts the height of the extracted pattern to 3: if the 
original height is < 3, pad with white (0) rows at the top; if the original 
height is >= 3, take only the top 3 rows. Creates an output grid of height 3 
and width equal to the adjusted pattern's width multiplied by N. Tiles the 
adjusted pattern horizontally N times to form the output grid. If N=0, the 
output is a 3x0 grid.
"""

def find_object_bbox(grid, color):
    """
    Finds the minimal bounding box of all pixels of a given color.
    Assumes pixels of the target color form one or more potentially disconnected 
    clusters, and returns the box enclosing ALL such pixels. For this task, 
    it's expected to enclose a single contiguous object.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to find.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if color not found.
    """
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None # No object of this color found

    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    
    return min_row, min_col, max_row, max_col

def count_color(grid, color):
    """Counts the occurrences of a specific color in the grid."""
    return np.sum(grid == color)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    azure_color = 8
    yellow_color = 4
    white_color = 0
    target_height = 3

    # 1. Identify Pattern: Locate the single contiguous object of azure (8) pixels
    # 2. Determine its minimal bounding box.
    bbox = find_object_bbox(input_np, azure_color)

    # Handle case where no azure object is found (return empty 3x0 grid)
    if bbox is None:
        return [[],[],[]] 

    min_row, min_col, max_row, max_col = bbox

    # 3. Extract Pattern: Extract the subgrid defined by this bounding box
    pattern = input_np[min_row : max_row + 1, min_col : max_col + 1]
    pattern_height, pattern_width = pattern.shape

    # 4. Count Repetitions: Count the total number of yellow (4) pixels (N)
    n_repeat = count_color(input_np, yellow_color)

    # 5. Handle Zero Repetitions: If N is 0, return a 3x0 grid
    if n_repeat == 0:
         return [[], [], []] 

    # 6. Adjust Pattern Height: Create a modified_pattern grid with height 3
    # Initialize with white
    modified_pattern = np.full((target_height, pattern_width), white_color, dtype=int)

    # Determine how many rows to pad (if pattern height < target)
    # and how many rows to copy from original pattern
    pad_rows_top = max(0, target_height - pattern_height)
    copy_rows_count = min(pattern_height, target_height)
    
    # Copy the relevant part of the original pattern into the modified pattern
    # If pattern_height < 3, copy all rows, placing them at the bottom (starting from pad_rows_top)
    # If pattern_height >= 3, copy top 3 rows, placing them at the top (starting from row 0)
    rows_to_copy_from_pattern = pattern[:copy_rows_count, :]
    modified_pattern[pad_rows_top : pad_rows_top + copy_rows_count, :] = rows_to_copy_from_pattern

    # 7. Calculate Output Dimensions (already implicitly done by tiling)
    # output_height = target_height
    # output_width = pattern_width * n_repeat

    # 8. Tile Pattern: Create the output grid by tiling the adjusted pattern N times
    # np.tile repeats the array. We want to repeat along the columns (axis=1) N times.
    output_np = np.tile(modified_pattern, (1, n_repeat))
        
    # 9. Return Output: Convert back to list of lists
    return output_np.tolist()