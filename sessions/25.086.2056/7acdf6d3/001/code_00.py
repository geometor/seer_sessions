import numpy as np

def transform(input_grid):
    """
    Processes an input grid based on the following rules:
    1. Identifies all pixels with the background color (orange, 7).
    2. For each orange pixel, checks if it is positioned exactly between two red (2) pixels, either horizontally or vertically.
       - Horizontally: The pixel to the immediate left and the pixel to the immediate right are both red.
       - Vertically: The pixel immediately above and the pixel immediately below are both red.
    3. If an orange pixel meets either of these conditions, its color is changed to maroon (9) in the output grid.
    4. Any maroon (9) pixels present in the input grid are changed back to the background color (orange, 7) in the output grid.
    5. All other pixels, including the red (2) pixels, retain their original color and position.
    """

    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    output_array = input_array.copy()
    height, width = input_array.shape
    
    # Define color constants
    ORANGE = 7
    RED = 2
    MAROON = 9

    # First pass: Reset any existing maroon pixels to orange
    for r in range(height):
        for c in range(width):
            if output_array[r, c] == MAROON:
                output_array[r, c] = ORANGE

    # Second pass: Identify orange pixels between two red pixels and change them to maroon
    # Iterate through the original input array to base decisions on the initial state
    for r in range(height):
        for c in range(width):
            # Check only if the original pixel was orange
            if input_array[r, c] == ORANGE:
                is_between_red = False
                
                # Check horizontally
                if c > 0 and c < width - 1:
                    if input_array[r, c - 1] == RED and input_array[r, c + 1] == RED:
                        is_between_red = True
                        
                # Check vertically
                if r > 0 and r < height - 1:
                    if input_array[r - 1, c] == RED and input_array[r + 1, c] == RED:
                        is_between_red = True

                # If the orange pixel is between two red pixels (horizontally or vertically), change it to maroon in the output
                if is_between_red:
                    output_array[r, c] = MAROON

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid
