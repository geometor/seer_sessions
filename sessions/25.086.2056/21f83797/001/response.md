```python
import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels with a specific color."""
    coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color:
                coords.append((r, c))
    return coords

def transform(input_grid):
    """
    Transforms the input grid based on the positions of two specific pixels (color 2).

    1. Identifies the coordinates of the two pixels with color 2.
    2. Determines the bounding box defined by these two pixels (min/max row and column).
    3. Draws horizontal and vertical lines (color 2) along the bounding box edges across the grid.
    4. Fills the rectangular area strictly inside the bounding box lines with color 1.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid with background color (0)
    output_grid = np.zeros_like(input_np) 
    
    # Define colors
    background_color = 0
    frame_color = 2
    fill_color = 1

    # 1. Identify the coordinates of the two non-background pixels (color 2)
    pixel_coords = find_pixels_by_color(input_np, frame_color)

    # Ensure exactly two pixels were found
    if len(pixel_coords) != 2:
        # Handle error case or return input/empty grid if rules unclear for other counts
        # For this specific task, we assume exactly two pixels.
        # Let's return the initial empty grid or copy of input if this happens
        print(f"Warning: Expected 2 pixels of color {frame_color}, found {len(pixel_coords)}. Returning empty grid.")
        return output_grid.tolist() 
        
    (r1, c1), (r2, c2) = pixel_coords

    # 2. Determine the minimum and maximum row and column indices
    min_row = min(r1, r2)
    max_row = max(r1, r2)
    min_col = min(c1, c2)
    max_col = max(c1, c2)

    # 3. Draw the frame (horizontal and vertical lines) with frame_color (2)
    # Draw horizontal lines
    output_grid[min_row, :] = frame_color
    output_grid[max_row, :] = frame_color
    
    # Draw vertical lines
    output_grid[:, min_col] = frame_color
    output_grid[:, max_col] = frame_color

    # 4. Fill the interior rectangle with fill_color (1)
    # Iterate through rows strictly between min_row and max_row
    for r in range(min_row + 1, max_row):
        # Iterate through columns strictly between min_col and max_col
        for c in range(min_col + 1, max_col):
            output_grid[r, c] = fill_color

    # Convert back to list of lists for the expected ARC format
    return output_grid.tolist()
```