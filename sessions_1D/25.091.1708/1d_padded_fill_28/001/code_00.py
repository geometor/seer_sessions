import numpy as np

def find_foreground_color(grid):
    """Finds the single non-background (non-zero) color in the grid."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    # Should not happen based on task description, but handle just in case
    return 0 

def find_bounding_box(grid, color):
    """Finds the min/max row/col for a given color."""
    rows, cols = np.where(grid == color)
    if rows.size == 0: # No pixels of this color found
        return None, None, None, None 
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Identifies the single non-white color in the input grid, determines its 
    bounding box (minimum and maximum row and column), and fills this 
    rectangular area in the output grid with that color, leaving the rest 
    of the grid white (0).
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Identify the single non-white color (C)
    foreground_color = find_foreground_color(input_array)
    
    # If no foreground color is found (e.g., all background), return the input as is
    # or an empty grid of the same size? Let's return a copy filled with background.
    if foreground_color == 0:
         return np.zeros_like(input_array).tolist()

    # 2. Find the bounding box of the foreground color
    min_row, max_row, min_col, max_col = find_bounding_box(input_array, foreground_color)

    # Handle case where bounding box wasn't found (shouldn't happen if foreground_color > 0)
    if min_row is None:
        return np.zeros_like(input_array).tolist()

    # 3. Create a new grid with the same dimensions, filled with background (0)
    output_array = np.zeros_like(input_array)

    # 4. Fill the rectangular region defined by the bounding box with the foreground color
    # Slicing is inclusive of the start index and exclusive of the end index,
    # so we add 1 to max_row and max_col.
    output_array[min_row:max_row+1, min_col:max_col+1] = foreground_color
    
    # 5. Convert the output numpy array back to a list of lists and return
    return output_array.tolist()