import numpy as np

"""
The transformation identifies the bounding box of the blue (1) rectangle in the input grid. 
It then creates an output grid of the same dimensions, initially filled with the background color orange (7). 
If a blue rectangle is found, the area corresponding to its bounding box is filled with red (2) in the output grid. 
Finally, all maroon (9) pixels from the original input grid are copied to their corresponding positions in the output grid, overwriting any orange (7) or red (2) pixels at those locations.
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
    preserving all original maroon pixels.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # Initialize output grid with background color (orange 7)
    output_grid_np = np.full_like(input_grid_np, 7) 

    # Find the bounding box of the blue (1) rectangle
    blue_bbox = find_bounding_box(input_grid_np, 1)

    # If a blue rectangle exists, fill its area with red (2) in the output
    if blue_bbox:
        min_row, min_col, max_row, max_col = blue_bbox
        output_grid_np[min_row:max_row+1, min_col:max_col+1] = 2
        
    # Iterate through the entire input grid
    for r in range(rows):
        for c in range(cols):
            # If a maroon (9) pixel is found in the input
            if input_grid_np[r, c] == 9:
                # Copy it to the output grid, overwriting existing colors (orange or red)
                output_grid_np[r, c] = 9
                    
    # Convert back to list of lists for the expected output format
    output_grid = output_grid_np.tolist()
    return output_grid
