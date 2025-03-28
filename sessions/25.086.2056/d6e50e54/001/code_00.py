import numpy as np

"""
The transformation identifies the bounding box of the blue (1) rectangle in the input grid. 
It then creates an output grid of the same dimensions, initially filled with the background color orange (7). 
The area corresponding to the blue rectangle's bounding box is filled with red (2) in the output grid. 
Finally, any maroon (9) pixels that were located within the original blue rectangle's bounding box in the input grid are copied to their corresponding positions in the output grid, overwriting the red (2) pixels if necessary. Maroon (9) pixels outside the blue rectangle's area are removed (replaced with orange 7).
"""

def find_bounding_box(grid, color):
    """Finds the bounding box (min_row, min_col, max_row, max_col) of the first object of a given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Transforms the input grid by replacing a blue rectangle with a red one,
    preserving only the maroon pixels originally inside the blue rectangle.
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    
    # Initialize output grid with background color (orange 7)
    output_grid_np = np.full_like(input_grid_np, 7) 

    # Find the bounding box of the blue (1) rectangle
    blue_bbox = find_bounding_box(input_grid_np, 1)

    if blue_bbox:
        min_row, min_col, max_row, max_col = blue_bbox
        
        # Fill the area of the blue rectangle with red (2) in the output
        output_grid_np[min_row:max_row+1, min_col:max_col+1] = 2
        
        # Iterate through the area of the original blue rectangle in the input
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                # If a maroon (9) pixel is found in the input within this area
                if input_grid_np[r, c] == 9:
                    # Copy it to the output grid
                    output_grid_np[r, c] = 9
                    
    # Convert back to list of lists for the expected output format
    output_grid = output_grid_np.tolist()
    return output_grid
