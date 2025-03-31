```python
import numpy as np

"""
Transforms the input grid based on the observed pattern:
1. Identifies the two primary colors (Color1, Color2) of the checkerboard pattern starting at the top-left of the input grid. Color1 is the color at input cell (0,0).
2. Determines the dimensions (Height H, Width W) of the input grid.
3. Creates an output grid of the same dimensions (H, W).
4. Fills the output grid with a checkerboard pattern using Color1 and Color2, but swaps the starting colors compared to the input. Specifically, the color at the output's top-left cell (0,0) is Color2 (the color *not* originally at input's (0,0)).
5. The color at any output cell (r, c) is determined by the parity of the sum of its coordinates (r + c):
   - If (r + c) is even, the color is Color2.
   - If (r + c) is odd, the color is Color1.
The border/padding color present in the input is ignored and does not influence the output pattern, other than potentially defining the extent of the original pattern area (which isn't directly used, as the output fills the whole grid).
"""

def transform(input_grid):
    """
    Applies a color-swapped checkerboard transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed output grid.
    
    Raises:
        ValueError: If the grid dimensions are too small (e.g., 1x1) or if two distinct 
                    checkerboard colors cannot be identified near the top-left corner.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    h, w = input_np.shape

    # Check for minimal dimensions needed to define a checkerboard pattern
    if h < 1 or w < 1:
         raise ValueError("Input grid must have at least one cell.")
    if h == 1 and w == 1:
         # Cannot determine two colors or swap pattern for a 1x1 grid.
         # The task definition implies a checkerboard, so this is likely invalid input.
         raise ValueError("Cannot apply checkerboard swap to a 1x1 grid.")

    # Identify the first color (assumed to be at the top-left corner)
    color1 = input_np[0, 0]
    
    # Identify the second color by checking adjacent cells
    color2 = -1 # Initialize with a sentinel value
    if w > 1 and input_np[0, 1] != color1:
        # Check the cell to the right
        color2 = input_np[0, 1]
    elif h > 1 and input_np[1, 0] != color1:
        # Check the cell below (if right cell was same color or grid is 1 column wide)
        color2 = input_np[1, 0]
    # Add check for diagonal if necessary, although unlikely for standard checkerboard start
    elif h > 1 and w > 1 and input_np[1, 1] == color1: 
         # If (0,0) and (1,1) are color1, then (0,1) or (1,0) *must* be color2 if it's a checkerboard.
         # This case is covered by the first two checks unless the grid is only 1xN or Nx1 starting with the same color.
         # If we reach here, it means (0,1) and (1,0) were either same as color1 or out of bounds.
         pass # Let the error handle it if color2 remains -1
         
    # Validate that two distinct colors were found
    if color2 == -1:
        # This could happen if the top-left area is monochromatic or grid structure is unusual.
        # Based on examples, we expect two colors to be readily identifiable.
        raise ValueError("Could not determine the two distinct checkerboard colors near the origin. Check input format.")

    # Initialize the output grid with the same dimensions
    output_np = np.zeros_like(input_np)

    # Fill the output grid with the swapped checkerboard pattern
    # The output pattern starts with color2 at (0,0)
    for r in range(h):
        for c in range(w):
            # Check the parity of the sum of coordinates
            if (r + c) % 2 == 0:
                # Even sum: Use the color that was NOT at input's (0,0) -> color2
                output_np[r, c] = color2
            else:
                # Odd sum: Use the color that WAS at input's (0,0) -> color1
                output_np[r, c] = color1

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```