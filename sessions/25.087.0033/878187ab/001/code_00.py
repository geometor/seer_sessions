import numpy as np
from typing import List, Tuple, Dict

# Color mapping for reference (not used directly in logic)
COLOR_MAP = {
    0: (238, 238, 238),  # white
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}

"""
Transformation Rule Natural Language Description:

1.  **Analyze Input:** Examine the input grid. Identify the background color (assumed to be orange, 7). Check if any pixels have a color different from the background color.
2.  **Check Condition:** If all pixels are the background color, return the input grid unchanged.
3.  **Prepare Output Grid:** If non-background pixels exist:
    a.  Determine input height (H) and width (W).
    b.  Calculate output height `output_H = max(16, H)` and output width `output_W = W`.
    c.  Create a new grid of size `output_H` x `output_W`, filled with the background color (7).
4.  **Determine Pattern Width (PW):** Calculate the pattern width based on the input width W. If W is even, `PW = W - 6`. If W is odd, `PW = W - 8`. Ensure PW is not negative (though unlikely given typical ARC grid sizes).
5.  **Define Pattern Properties:** The pattern has a fixed height `pattern_H = 5`. It uses red (2) and yellow (4).
6.  **Draw Pattern:** In the bottom-left corner of the output grid (rows `output_H - 5` to `output_H - 1`, columns 0 to `PW - 1`):
    a.  For each cell within these bounds, calculate its relative row `pr` (0 to 4) and relative column `pc` (0 to PW-1).
    b.  Set the cell color to yellow (4) if `pc == 4 - pr` or `pc == (PW - 1) - (4 - pr)`.
    c.  Otherwise, set the cell color to red (2).
7.  **Return Output:** Return the modified grid.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: if the input grid contains any non-orange (7) pixels,
    it creates an output grid (potentially resized to min height 16) and draws a 
    red/yellow pattern in the bottom-left corner whose width depends on the input width.
    Otherwise, it returns the input grid unchanged.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape
    background_color = 7 # Assuming orange (7) is always the background

    # 1. Analyze Input & 2. Check Condition
    # Check if any pixel is not the background color
    contains_foreground = np.any(input_np != background_color)

    if not contains_foreground:
        # If only background color exists, return the input grid as is
        return input_grid

    # 3. Prepare Output Grid
    output_H = max(16, H)
    output_W = W
    output_grid = np.full((output_H, output_W), background_color, dtype=int)

    # 4. Determine Pattern Width (PW)
    if W % 2 == 0: # Even width
        PW = W - 6
    else: # Odd width
        PW = W - 8
    
    # Ensure pattern width is not negative or zero (unlikely for ARC)
    PW = max(1, PW) 
    
    # 5. Define Pattern Properties
    pattern_H = 5
    color_red = 2
    color_yellow = 4

    # 6. Draw Pattern
    start_row = output_H - pattern_H # Row index where the pattern starts

    for pr in range(pattern_H):  # Relative row within the pattern (0 to 4)
        for pc in range(PW):     # Relative column within the pattern (0 to PW-1)
            
            # Calculate absolute row and column in the output grid
            r = start_row + pr
            c = pc

            # Boundary check (mostly for column, ensuring pc < output_W)
            if r < output_H and c < output_W:
                 # Check condition for yellow color
                 # Using (pattern_H - 1) which is 4
                if pc == (pattern_H - 1) - pr or pc == (PW - 1) - ((pattern_H - 1) - pr):
                    output_grid[r, c] = color_yellow
                else:
                    output_grid[r, c] = color_red

    # 7. Return Output
    return output_grid.tolist()