```python
import numpy as np

def find_non_white_pixels(grid):
    """Finds all non-white pixels and returns their (row, col, color) sorted."""
    non_white_pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0:
                non_white_pixels.append((r, c, color))
    # Sort by row, then by column
    non_white_pixels.sort()
    return non_white_pixels

def transform(input_grid):
    """
    Draws 'L' shapes originating from non-white pixels in the input grid.
    Each 'L' shape extends horizontally to the right edge and vertically
    down from the right edge to the bottom edge. Shapes are drawn in
    top-to-bottom, left-to-right order based on the source pixel,
    with later shapes overwriting earlier ones in case of overlap.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Find and sort all non-white source pixels
    source_pixels = find_non_white_pixels(input_np)

    # Iterate through sorted source pixels and draw 'L' shapes
    for r, c, color in source_pixels:
        # Draw horizontal segment: from (r, c) to (r, width-1)
        output_grid[r, c:width] = color
        
        # Draw vertical segment: from (r, width-1) down to (height-1, width-1)
        # Note: The horizontal segment already colored (r, width-1), 
        # so the vertical segment effectively starts from (r, width-1) 
        # even if we iterate from row r.
        output_grid[r:height, width-1] = color

    # Convert back to list of lists for the standard ARC format if needed,
    # but returning a numpy array is often acceptable.
    return output_grid.tolist()

```