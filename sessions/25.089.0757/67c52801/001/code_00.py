import numpy as np

"""
Apply gravity to non-background pixels within each column of the grid.
Non-background pixels fall downwards until they encounter another 
non-background pixel below them or reach the bottom row of the grid.
The original positions of the fallen pixels become the background color (white, 0).
The process happens independently for each column. The bottom row acts as a floor;
its initial state effectively determines the lowest point pixels can fall to in 
each column, and pixels within the bottom row itself do not move.
"""

def transform(input_grid):
    """
    Applies gravity to non-background pixels in a grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize the output grid with the background color (0)
    output_array = np.zeros_like(input_array)
    
    # Process each column independently
    for c in range(width):
        # 'landing_row' tracks the next available row index from the bottom where a pixel can land
        landing_row = height - 1 
        
        # Iterate through the rows of the input column from bottom to top
        for r in range(height - 1, -1, -1):
            # Get the pixel color from the input grid
            pixel_color = input_array[r, c]
            
            # If the pixel is not the background color
            if pixel_color != 0:
                # Place this pixel at the current landing spot in the output grid
                output_array[landing_row, c] = pixel_color
                # Move the landing spot one row up for the next pixel in this column
                landing_row -= 1
                
    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
