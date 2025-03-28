"""
Transformation Rule Natural Language Description:

1.  **Define Background:** Identify the background color as orange (7).
2.  **Analyze Input:** Examine the input grid. Check if any pixel has a color different from orange.
3.  **Conditional Execution:**
    *   **If** all pixels in the input grid are orange: Return the input grid unchanged.
    *   **If** at least one pixel is *not* orange: Proceed to the pattern generation steps.
4.  **Initialize Output Grid:**
    *   Determine the input grid's height (H) and width (W).
    *   Calculate the output grid dimensions: `output_H = max(16, H)`, `output_W = W`.
    *   Create a new grid of size `output_H` x `output_W`, completely filled with the background color (orange).
5.  **Calculate Pattern Width:**
    *   Determine the width (PW) for the pattern based on the input width (W).
    *   If W is even, `PW = W - 6`.
    *   If W is odd, `PW = W - 8`.
    *   Ensure PW is at least 1 (`PW = max(1, PW)`).
6.  **Define Pattern:** The pattern to be drawn has a fixed height of 5 rows and the calculated width PW. It uses red (2) and yellow (4) colors.
7.  **Draw Pattern:**
    *   Target the bottom-left `5 x PW` region of the output grid. The top-left corner of this region is at row `output_H - 5` and column `0`.
    *   Iterate through each cell within this `5 x PW` region using relative coordinates `pr` (pattern row, 0 to 4) and `pc` (pattern column, 0 to PW-1).
    *   For each cell (`pr`, `pc`) within the pattern region:
        *   Calculate the corresponding absolute coordinates (`r`, `c`) in the output grid: `r = output_H - 5 + pr`, `c = pc`.
        *   Determine the color:
            *   Set the color to yellow (4) if `pc == 4 - pr` (diagonal from top-left) OR `pc == (PW - 1) - (4 - pr)` (diagonal from top-right relative to pattern width).
            *   Otherwise, set the color to red (2).
        *   Place the determined color at the output grid cell (`r`, `c`).
8.  **Return Output:** Return the modified output grid containing the drawn pattern.
"""

import numpy as np
from typing import List

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: if the input grid contains any non-orange (7) pixels,
    it creates an output grid (potentially resized to min height 16) and draws a 
    red/yellow pattern in the bottom-left corner whose width depends on the input width.
    Otherwise, it returns the input grid unchanged.
    """
    
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape
    
    # 1. Define Background color
    background_color = 7 

    # 2. Analyze Input & 3. Conditional Execution (Check Condition)
    # Check if any pixel is not the background color
    contains_foreground = np.any(input_np != background_color)

    if not contains_foreground:
        # If only background color exists, return the input grid as is
        return input_grid

    # --- Condition met: Proceed with pattern generation ---
    
    # 4. Initialize Output Grid
    output_H = max(16, H)
    output_W = W
    # Create a new grid filled with the background color
    output_grid = np.full((output_H, output_W), background_color, dtype=int)

    # 5. Calculate Pattern Width (PW)
    if W % 2 == 0: # Even width
        PW = W - 6
    else: # Odd width
        PW = W - 8
    
    # Ensure pattern width is at least 1
    PW = max(1, PW) 
    
    # 6. Define Pattern Properties
    pattern_H = 5
    color_red = 2
    color_yellow = 4

    # 7. Draw Pattern
    # Calculate the starting row index for the pattern in the output grid
    start_row = output_H - pattern_H 

    # Iterate through the relative rows (pr) and columns (pc) of the pattern area
    for pr in range(pattern_H):  # Relative row within the pattern (0 to 4)
        for pc in range(PW):     # Relative column within the pattern (0 to PW-1)
            
            # Calculate absolute row and column in the output grid
            r = start_row + pr
            c = pc

            # Check boundary conditions (column check mainly, row is implicitly handled by start_row calculation)
            if c < output_W: 
                 # Check condition for yellow color: 
                 # pc == 4 - pr  (diagonal from top-left of pattern)
                 # pc == (PW - 1) - (4 - pr) (diagonal from top-right of pattern)
                 # Note: (pattern_H - 1) is 4
                if pc == (pattern_H - 1) - pr or pc == (PW - 1) - ((pattern_H - 1) - pr):
                    output_grid[r, c] = color_yellow
                else:
                    # Default color within the pattern is red
                    output_grid[r, c] = color_red

    # 8. Return Output
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()