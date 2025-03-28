```python
"""
This transformation takes a 10x10 input grid and produces a 5x5 output grid.
The 10x10 input grid is treated as four 5x5 quadrants: Top-Left (TL), 
Top-Right (TR), Bottom-Left (BL), and Bottom-Right (BR).

Each pixel in the 5x5 output grid at coordinate (r, c) is determined by 
checking the corresponding pixel locations in the input grid's quadrants 
in a specific priority order: BL, BR, TL, TR.

The rule is:
1. Look at the pixel in the BL quadrant at (r + 5, c). If it's not white (0), 
   use its color for the output pixel (r, c).
2. If the BL pixel is white, look at the pixel in the BR quadrant at 
   (r + 5, c + 5). If it's not white (0), use its color for the output pixel (r, c).
3. If the BR pixel is also white, look at the pixel in the TL quadrant at 
   (r, c). If it's not white (0), use its color for the output pixel (r, c).
4. If the TL pixel is also white, use the color of the pixel in the TR 
   quadrant at (r, c + 5) for the output pixel (r, c), regardless of its color.
5. If all corresponding pixels in BL, BR, and TL are white, the TR pixel's 
   color (which might also be white) is used.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 10x10 input grid into a 5x5 output grid based on quadrant priority.
    
    Args:
        input_grid (list of lists or np.ndarray): The 10x10 input grid.

    Returns:
        np.ndarray: The 5x5 transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape
    
    # Validate input dimensions (optional but good practice)
    if input_height != 10 or input_width != 10:
        raise ValueError("Input grid must be 10x10")
        
    output_height = 5
    output_width = 5
    
    # Initialize the output grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the 5x5 output grid
    for r in range(output_height):
        for c in range(output_width):
            # Coordinates in the input grid quadrants
            bl_r, bl_c = r + 5, c
            br_r, br_c = r + 5, c + 5
            tl_r, tl_c = r, c
            tr_r, tr_c = r, c + 5

            # 1. Check Bottom-Left (BL) quadrant
            pixel_bl = input_np[bl_r, bl_c]
            if pixel_bl != 0:
                output_grid[r, c] = pixel_bl
                continue  # Move to the next output pixel

            # 2. Check Bottom-Right (BR) quadrant
            pixel_br = input_np[br_r, br_c]
            if pixel_br != 0:
                output_grid[r, c] = pixel_br
                continue  # Move to the next output pixel

            # 3. Check Top-Left (TL) quadrant
            pixel_tl = input_np[tl_r, tl_c]
            if pixel_tl != 0:
                output_grid[r, c] = pixel_tl
                continue  # Move to the next output pixel

            # 4. Use Top-Right (TR) quadrant value (even if it's 0)
            pixel_tr = input_np[tr_r, tr_c]
            output_grid[r, c] = pixel_tr

    return output_grid.tolist() # Return as list of lists per ARC standard

```