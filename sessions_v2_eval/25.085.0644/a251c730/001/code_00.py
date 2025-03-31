import numpy as np

def find_bounding_box(grid, color):
    """
    Finds the minimum bounding box containing all pixels of a specific color.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color value to find.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if color not found.
    """
    rows, cols = np.where(grid == color)
    if rows.size == 0:
        return None  # Color not found
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Identifies a rectangular region enclosed by a green (3) frame within the 
    input grid and extracts this region, including the frame, as the output grid.
    
    The process assumes there is exactly one such green frame.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Define the frame color
    frame_color = 3 # green

    # Find the coordinates of all pixels with the frame color
    # This gives us the potential extent of the frame
    bounding_box = find_bounding_box(input_grid_np, frame_color)

    if bounding_box is None:
        # Handle the case where no green pixels are found (though unlikely based on examples)
        # Returning the original grid or an empty one might be options,
        # but based on the task description, we expect a frame.
        # For now, let's raise an error or return None/empty.
        # Returning the input might be safest if unsure.
        print("Warning: Green frame color (3) not found in the input grid.")
        return input_grid # Or potentially return np.array([[]]) or raise ValueError

    min_row, max_row, min_col, max_col = bounding_box
    
    # Extract the subgrid defined by the bounding box
    # The slice includes the max_row and max_col, hence the +1
    output_grid_np = input_grid_np[min_row : max_row + 1, min_col : max_col + 1]

    # Convert back to list of lists if necessary for the environment
    # output_grid = output_grid_np.tolist() 

    # Return the numpy array as it's often more convenient
    return output_grid_np
