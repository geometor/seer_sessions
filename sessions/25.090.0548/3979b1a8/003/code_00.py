import numpy as np
from collections import Counter
import copy

"""
Transforms the input grid based on color frequency ranks.

1.  Determine the dimensions (H, W) of the input grid.
2.  Analyze the input grid to find all unique colors and rank them by frequency.
    Let R1 be the most frequent, R2 the second most frequent, and R3 the third most frequent.
    Handle cases where there are fewer than 3 distinct colors.
3.  Create four intermediate grids (G1, G2, G3, G4), each of size HxW.
4.  G1: A direct copy of the input grid.
5.  G2: A copy of the input grid where colors R1 and R2 are swapped. If R2 does not exist, G2 is identical to G1.
6.  G3: A direct copy of G2.
7.  G4: A copy of G2 where colors R2 and R3 are swapped. 
    - If R3 does not exist, G4 is identical to G2.
    - If R2 does not exist (meaning only R1 exists), G4 is identical to G2 (which is identical to G1).
8.  Create the final output grid with dimensions 2H x 2W.
9.  Place G1 in the top-left quadrant (TL).
10. Place G2 in the top-right quadrant (TR).
11. Place G3 in the bottom-left quadrant (BL).
12. Place G4 in the bottom-right quadrant (BR).
13. Return the output grid.
"""

def swap_colors(grid: np.ndarray, color_a, color_b) -> np.ndarray:
    """Creates a new grid with two specified colors swapped."""
    if color_a is None or color_b is None or color_a == color_b:
        return grid.copy() # No swap needed if colors are missing or the same
        
    new_grid = grid.copy()
    mask_a = (grid == color_a)
    mask_b = (grid == color_b)
    new_grid[mask_a] = color_b
    new_grid[mask_b] = color_a
    return new_grid

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by creating a 2x2 tiled output grid based on color frequency swaps.
    TL = Input
    TR = Input with (Most Freq <-> 2nd Most Freq) swap
    BL = TR
    BR = TR with (2nd Most Freq <-> 3rd Most Freq) swap
    """
    input_grid = np.array(input_grid)
    H, W = input_grid.shape

    # Analyze color frequencies and determine ranks R1, R2, R3
    color_counts = Counter(input_grid.flatten())
    ranked_colors = [item[0] for item in color_counts.most_common()]
    
    R1 = ranked_colors[0] if len(ranked_colors) > 0 else None
    R2 = ranked_colors[1] if len(ranked_colors) > 1 else None
    R3 = ranked_colors[2] if len(ranked_colors) > 2 else None

    # Create G1: Input grid
    G1 = input_grid.copy()

    # Create G2: Input with R1 <-> R2 swap
    G2 = swap_colors(input_grid, R1, R2)

    # Create G3: Copy of G2
    G3 = G2.copy() # Since G2 is already a modified copy

    # Create G4: G2 with R2 <-> R3 swap
    # Note: We apply the swap to G2 using the original R2 and R3 colors.
    G4 = swap_colors(G2, R2, R3)

    # Assemble the output grid
    output_grid = np.zeros((2 * H, 2 * W), dtype=input_grid.dtype)

    output_grid[0:H, 0:W] = G1       # Top-Left
    output_grid[0:H, W:2*W] = G2    # Top-Right
    output_grid[H:2*H, 0:W] = G3    # Bottom-Left
    output_grid[H:2*H, W:2*W] = G4 # Bottom-Right
    
    return output_grid