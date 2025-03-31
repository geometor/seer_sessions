import numpy as np

"""
Applies a gravity effect to non-background pixels within each column of the grid independently.
Non-background pixels (colors 1-9) fall downwards within their column until they either 
reach the bottom row of the grid or land on top of another non-background pixel.
The original position of a pixel that falls is replaced with the background color (white, 0).
Pixels in the bottom row do not move. The process is applied column by column, and 
within each column, pixels are processed from the second-to-last row upwards to ensure 
lower pixels settle before pixels above them attempt to fall.
"""

def transform(input_grid):
    """
    Applies gravity to non-background pixels in a grid, making them fall downwards
    within their column until they hit another pixel or the bottom of the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid after gravity is applied.
    """
    # Convert input grid to a NumPy array for efficient manipulation
    output_array = np.array(input_grid, dtype=int)
    height, width = output_array.shape

    # Process each column independently
    for c in range(width):
        # Iterate through the rows of the current column from bottom-up, 
        # starting from the second-to-last row.
        # The bottom row (height - 1) acts as a floor and its pixels don't move upwards.
        for r in range(height - 2, -1, -1):
            # Get the color of the current pixel
            pixel_color = output_array[r, c]

            # Check if the pixel is non-background (should fall)
            if pixel_color != 0:
                # Start checking from the row below the current pixel
                current_r = r
                
                # Find the lowest possible row the pixel can fall to
                # Keep moving down as long as the next row is within bounds and is background (0)
                while current_r + 1 < height and output_array[current_r + 1, c] == 0:
                    current_r += 1
                
                # If the pixel moved (current_r is different from the original row r)
                if current_r != r:
                    # Move the pixel to the new position
                    output_array[current_r, c] = pixel_color
                    # Set the original position to background
                    output_array[r, c] = 0

    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
