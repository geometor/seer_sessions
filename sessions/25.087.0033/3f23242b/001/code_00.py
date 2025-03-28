import numpy as np

def safe_set_pixel(grid, r, c, color, H, W):
    """Safely sets the color of a pixel if coordinates are within grid bounds."""
    if 0 <= r < H and 0 <= c < W:
        grid[r, c] = color

def transform(input_grid):
    """
    Transforms the input grid by finding green (3) trigger pixels and drawing a 
    predefined structure centered around each trigger.

    The structure includes gray (5), red (2), and azure (8) pixels arranged in lines 
    relative to the trigger pixel's location (r, c). Specifically:
    - A horizontal gray line 5 pixels wide at row r-2, centered at c.
    - A single gray pixel at (r-1, c).
    - Vertical red lines 4 pixels tall at columns c-2 and c+2, from row r-1 to r+2.
    - Single red pixels at (r, c-2) and (r, c+2).
    - A horizontal azure line 5 pixels wide at row r+2, centered at c.
    - Horizontal red lines extending from the ends of the azure line (at c-3 and c+3) 
      to the grid edges along row r+2.
    The original green (3) pixel at (r, c) is preserved.
    """
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    H, W = output_grid.shape

    # Find all green (3) trigger pixels
    trigger_coords = []
    for r in range(H):
        for c in range(W):
            if input_grid[r, c] == 3:
                trigger_coords.append((r, c))

    # For each trigger pixel, draw the structure
    for r, c in trigger_coords:
        
        # Define structure components relative to (r, c)
        structure_pixels = [
            # Top gray line (row r-2, cols c-2 to c+2)
            ((r-2, c-2), 5), ((r-2, c-1), 5), ((r-2, c), 5), ((r-2, c+1), 5), ((r-2, c+2), 5),
            # Center gray dot (r-1, c)
            ((r-1, c), 5),
            # Left red line (col c-2, rows r-1 to r+2)
            ((r-1, c-2), 2), ((r, c-2), 2), ((r+1, c-2), 2), ((r+2, c-2), 2),
            # Right red line (col c+2, rows r-1 to r+2)
            ((r-1, c+2), 2), ((r, c+2), 2), ((r+1, c+2), 2), ((r+2, c+2), 2),
            # Bottom azure line (row r+2, cols c-2 to c+2)
            # Note: (r+2, c-2) and (r+2, c+2) are already red from vertical lines,
            # Azure will overwrite them if drawn later, or be overwritten if drawn first.
            # Based on the examples, the corners should be Azure.
            ((r+2, c-1), 8), ((r+2, c), 8), ((r+2, c+1), 8),
            # Let's redraw the corners as Azure explicitly to match example output
            ((r+2, c-2), 8), ((r+2, c+2), 8), 
            # The original green pixel (r, c) is already there from the copy
            # ((r, c), 3) 
        ]

        # Draw the main structure pixels, checking boundaries
        for (row, col), color in structure_pixels:
            safe_set_pixel(output_grid, row, col, color, H, W)

        # Draw the bottom red extension lines (row r+2)
        # Left extension (cols 0 to c-3)
        target_row_ext = r + 2
        if 0 <= target_row_ext < H: # Check if the extension row is valid
            for col_ext in range(c - 2): # Up to c-3 inclusive
                safe_set_pixel(output_grid, target_row_ext, col_ext, 2, H, W)
            # Right extension (cols c+3 to W-1)
            for col_ext in range(c + 3, W): # From c+3 inclusive
                safe_set_pixel(output_grid, target_row_ext, col_ext, 2, H, W)

    return output_grid