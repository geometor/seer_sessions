import numpy as np
import math

"""
The transformation rule depends on the specific set of non-white colors present in the input grid. The rules are checked in a specific priority order:

1.  **Magenta/Orange Swap & Flip:** If both Magenta (6) and Orange (7) are present:
    *   Swap all Magenta pixels to Orange and all Orange pixels to Magenta.
    *   Horizontally flip the positions of all Red (2) and Yellow (4) pixels relative to the grid's width.
    *   All other non-white pixels (e.g., Azure 8) become white (0).
2.  **Yellow/Blue Conversion:** If both Blue (1) and Yellow (4) are present (and rule 1 didn't apply):
    *   Convert all Yellow (4) pixels to Red (2).
    *   Convert all Blue (1) pixels to Orange (7).
    *   Convert Azure (8) pixels based on row: If the row index is less than or equal to the median row index (floor((height - 1) / 2)), convert to Red (2); otherwise, convert to Orange (7).
    *   All other non-white pixels (e.g., original Red 2, Orange 7) become white (0).
3.  **Red/Yellow Swap:** If both Red (2) and Yellow (4) are present (and rules 1, 2 didn't apply):
    *   Swap all Red pixels to Yellow and all Yellow pixels to Red.
    *   All other non-white pixels become white (0).
4.  **Blue/Red Swap:** If both Blue (1) and Red (2) are present (and rules 1, 2, 3 didn't apply):
    *   Swap all Blue pixels to Red and all Red pixels to Blue.
    *   All other non-white pixels (e.g., Azure 8) become white (0).
5.  **Default:** If none of the above color combinations trigger a rule, the output grid is entirely white (0).
"""

def get_present_colors(grid_np):
    """Finds the set of unique non-zero colors in a numpy grid."""
    return set(grid_np.flatten()) - {0}

def transform(input_grid):
    """
    Applies a transformation rule based on the set of colors present in the input grid.
    Rules involve color swaps, conditional conversions, and positional flips,
    prioritized in a specific order.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    # Initialize output grid with white (0)
    output_np = np.zeros_like(input_np)
    
    # Determine the set of non-white colors present
    present_colors = get_present_colors(input_np)
    
    # Calculate median row index for Rule 2
    median_row = (height - 1) // 2

    # --- Rule Priority Check ---

    # Rule 1: Magenta(6)/Orange(7) swap + Red(2)/Yellow(4) horizontal flip
    if {6, 7}.issubset(present_colors):
        # Create a temporary grid to store flipped Red/Yellow positions
        flipped_grid = np.zeros_like(input_np)
        for r in range(height):
            for c in range(width):
                pixel = input_np[r, c]
                if pixel == 6:
                    # Swap Magenta to Orange
                    output_np[r, c] = 7
                elif pixel == 7:
                    # Swap Orange to Magenta
                    output_np[r, c] = 6
                elif pixel == 2:
                    # Store Red in horizontally flipped position
                    flipped_grid[r, width - 1 - c] = 2
                elif pixel == 4:
                    # Store Yellow in horizontally flipped position
                    flipped_grid[r, width - 1 - c] = 4
                # Other colors (like Azure 8) are ignored, remain 0 in output_np
        
        # Merge the flipped Red/Yellow pixels into the output grid
        # Only update where flipped_grid has a non-zero value
        output_np[flipped_grid != 0] = flipped_grid[flipped_grid != 0]

    # Rule 2: Yellow(4)->Red(2), Blue(1)->Orange(7), Azure(8) split by median row
    elif {1, 4}.issubset(present_colors):
        for r in range(height):
            for c in range(width):
                pixel = input_np[r, c]
                if pixel == 4:
                    # Convert Yellow to Red
                    output_np[r, c] = 2
                elif pixel == 1:
                    # Convert Blue to Orange
                    output_np[r, c] = 7
                elif pixel == 8:
                    # Convert Azure based on row position relative to median
                    if r <= median_row:
                        output_np[r, c] = 2
                    else:
                        output_np[r, c] = 7
                # Other colors (original Red 2, Orange 7) are ignored, remain 0

    # Rule 3: Red(2)/Yellow(4) swap (Hypothesized based on patterns)
    elif {2, 4}.issubset(present_colors):
         for r in range(height):
            for c in range(width):
                pixel = input_np[r, c]
                if pixel == 2:
                    # Swap Red to Yellow
                    output_np[r, c] = 4
                elif pixel == 4:
                    # Swap Yellow to Red
                    output_np[r, c] = 2
                # Other colors are ignored, remain 0

    # Rule 4: Blue(1)/Red(2) swap
    elif {1, 2}.issubset(present_colors):
        for r in range(height):
            for c in range(width):
                pixel = input_np[r, c]
                if pixel == 1:
                    # Swap Blue to Red
                    output_np[r, c] = 2
                elif pixel == 2:
                    # Swap Red to Blue
                    output_np[r, c] = 1
                # Other colors (like Azure 8) are ignored, remain 0

    # Default: If no rules matched, output_np remains all zeros (white)

    # Convert numpy array back to list of lists for the final output
    return output_np.tolist()