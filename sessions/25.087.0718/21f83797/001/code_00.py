import numpy as np

def find_marker_pixels(grid):
    """
    Finds the coordinates and color of the two non-background pixels.
    """
    marker_coords = []
    marker_color = None
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:  # 0 is the background color (white)
                if marker_color is None:
                    marker_color = grid[r, c]
                elif grid[r, c] != marker_color:
                    # Assuming marker pixels always have the same color based on examples
                    raise ValueError("Found marker pixels with different colors.")
                marker_coords.append((r, c))

    if len(marker_coords) != 2:
        raise ValueError(f"Expected 2 marker pixels, but found {len(marker_coords)}.")
        
    return marker_coords, marker_color

def transform(input_grid):
    """
    Draws a frame based on the coordinates of two marker pixels found in the input grid
    and fills the interior of the frame with blue (1).

    1. Finds the coordinates (r1, c1), (r2, c2) and color (marker_color) of the two non-white pixels.
    2. Determines the min/max rows and columns (min_row, max_row, min_col, max_col).
    3. Creates an output grid initialized to white (0).
    4. Draws horizontal lines with marker_color at min_row and max_row.
    5. Draws vertical lines with marker_color at min_col and max_col.
    6. Fills the rectangular area strictly inside the frame lines with blue (1).
    """
    
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with the background color (white = 0)
    output_grid = np.zeros_like(input_np)

    try:
        # 1. Find the marker pixels' coordinates and color
        marker_coords, marker_color = find_marker_pixels(input_np)
        (r1, c1), (r2, c2) = marker_coords

        # 2. Determine min/max rows and columns
        min_row = min(r1, r2)
        max_row = max(r1, r2)
        min_col = min(c1, c2)
        max_col = max(c1, c2)
        
        fill_color = 1 # Blue

        # 6. Fill the rectangular area strictly inside the frame first
        # This ensures the frame lines overwrite the fill at the boundary if needed.
        # Slicing in numpy is exclusive for the end index, so max_row and max_col work directly.
        # Check if there's actually space to fill (i.e., points are not adjacent)
        if max_row > min_row + 1 and max_col > min_col + 1:
             output_grid[min_row + 1 : max_row, min_col + 1 : max_col] = fill_color

        # 4. Draw horizontal lines with marker_color
        output_grid[min_row, :] = marker_color
        output_grid[max_row, :] = marker_color

        # 5. Draw vertical lines with marker_color
        output_grid[:, min_col] = marker_color
        output_grid[:, max_col] = marker_color

    except ValueError as e:
        # Handle cases where the input doesn't match expectations (e.g., not 2 markers)
        # For now, return the empty grid, but could add specific error handling
        print(f"Error processing grid: {e}")
        # Returning the initialized white grid might be safer than raising an error
        # depending on how the caller handles exceptions.

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()