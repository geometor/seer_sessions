import numpy as np

"""
Identifies a gray (5) frame structure located at fixed rows 3 and 7, and columns 3 and 7 (0-indexed), which divides the grid into nine 3x3 subgrids (cells).
Determines the single "active" color present within these 3x3 subgrids in the input grid. The active color is the first color encountered that is neither white (0) nor gray (5).
Calculates a fill threshold based on the active color: threshold = max(2, active_color_value).
Creates an output grid, initially white (0).
Iterates through each of the nine 3x3 cell locations.
For each input cell, counts the number of pixels matching the active color.
If the count meets or exceeds the calculated threshold, the corresponding 3x3 cell in the output grid is filled entirely with the active color. Otherwise, it remains white (0).
Finally, the gray frame (rows 3, 7 and columns 3, 7) is explicitly drawn onto the output grid, overwriting any cell content at the frame's location.
"""

def find_active_color(grid: np.ndarray) -> int | None:
    """
    Finds the first non-white (0) and non-gray (5) color within the areas
    not occupied by the assumed gray frame (rows 3, 7 and cols 3, 7).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        int or None: The active color value, or None if no active color is found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            # Skip pixels assumed to be part of the gray frame
            if r == 3 or r == 7 or c == 3 or c == 7:
                continue
            
            pixel = grid[r, c]
            # Check if the pixel is neither white (0) nor gray (5)
            if pixel != 0 and pixel != 5: 
                return int(pixel) # Found the active color
                
    return None # No active color found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on a threshold count of an 'active color' 
    within 3x3 subgrids defined by a gray frame. Subgrids meeting the threshold 
    are filled with the active color; others become white. The frame is preserved.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize the output grid with white (0)
    output_np = np.zeros_like(input_np)
    
    # Define constants
    gray_color = 5
    white_color = 0
    frame_rows = [3, 7]
    frame_cols = [3, 7]

    # Find the single active color in the input grid (ignoring the frame)
    active_color = find_active_color(input_np)

    # If no active color is found, proceed to just draw the frame on the white grid
    if active_color is not None:
        # Calculate the fill threshold
        threshold = max(2, active_color)

        # Define the top-left corner coordinates of the 3x3 subgrids.
        # Assumes the standard 11x11 grid structure from examples for index calculation.
        subgrid_starts = []
        # Iterate potential row starts (0, 4, 8)
        for r_start in range(0, rows, 4): 
             # Iterate potential col starts (0, 4, 8)
             for c_start in range(0, cols, 4):
                 # Check if a 3x3 grid starting here fits within the bounds
                 # And doesn't start *on* a frame line (though frame lines are handled later)
                 if r_start + 3 <= rows and c_start + 3 <= cols:
                     subgrid_starts.append((r_start, c_start))

        # Process each 3x3 subgrid location
        for r_start, c_start in subgrid_starts:
            # Extract the corresponding 3x3 subgrid from the input grid
            subgrid_input = input_np[r_start:r_start+3, c_start:c_start+3]

            # Count the number of active pixels within this input subgrid
            pixel_count = np.count_nonzero(subgrid_input == active_color)

            # Fill the corresponding subgrid area in the output grid based on the threshold
            if pixel_count >= threshold:
                # Fill the 3x3 area with the active color
                output_np[r_start:r_start+3, c_start:c_start+3] = active_color
            else:
                # Fill the 3x3 area with white (already initialized, but explicit)
                output_np[r_start:r_start+3, c_start:c_start+3] = white_color

    # Explicitly reconstruct the gray frame in the output grid AFTER processing subgrids.
    # This ensures the frame is intact and overwrites any cell fills at frame indices.
    for r in frame_rows:
        if 0 <= r < rows:
            output_np[r, :] = gray_color
    for c in frame_cols:
        if 0 <= c < cols:
            output_np[:, c] = gray_color
        
    # Ensure frame intersection points are gray (important if frame lines are thin or grid small)
    # May be redundant if the line assignments above cover them, but safe.
    for r in frame_rows:
        for c in frame_cols:
             if 0 <= r < rows and 0 <= c < cols:
                 output_np[r, c] = gray_color

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()