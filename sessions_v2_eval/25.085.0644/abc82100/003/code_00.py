import numpy as np
import math

"""
The transformation rule depends on the specific set of non-white colors present in the input grid, checked in a specific priority order:

1.  **Magenta/Orange Swap & Flip (Trigger: {6, 7} present):**
    *   Swap Magenta (6) pixels to Orange (7) and Orange (7) pixels to Magenta (6) in place.
    *   For Red (2) pixels at (r, c), place Yellow (4) at the horizontally flipped position (r, width - 1 - c) in the output.
    *   For Yellow (4) pixels at (r, c), place Red (2) at the horizontally flipped position (r, width - 1 - c) in the output.
    *   All other non-white pixels (e.g., Azure 8) become white (0).

2.  **Blue/Yellow Conditional Conversion (Trigger: {1, 4} present, and Rule 1 did not apply):**
    *   Convert Yellow (4) pixels to Red (2).
    *   Convert Blue (1) pixels to Orange (7).
    *   Convert Azure (8) pixels based on row: If the row index `r` is less than or equal to the median row index (floor((height - 1) / 2)), convert to Red (2); otherwise, convert to Orange (7).
    *   All other non-white pixels (e.g., original Red 2, Orange 7, Magenta 6) become white (0).
    *   Note: This rule primarily addresses color transformation; the spatial placement in the output might require more complex logic based on observed patterns in Example 3.

3.  **Red/Yellow Swap (Trigger: {2, 4} present, and Rules 1, 2 did not apply):**
    *   Swap Red (2) pixels to Yellow (4) and Yellow (4) pixels to Red (2).
    *   All other non-white pixels become white (0).

4.  **Blue/Red Swap (+ Azure Handling) (Trigger: {1, 2} present, and Rules 1, 2, 3 did not apply):**
    *   Check if Azure (8) is also present.
    *   **Case 4a (Azure present: {1, 2, 8}):**
        *   Swap Blue (1) pixels to Red (2).
        *   Swap Red (2) pixels to Blue (1).
        *   Convert Azure (8) pixels to Blue (1).
        *   All other non-white pixels become white (0). (Derived from Ex 4, but known to be inconsistent with Ex 1).
    *   **Case 4b (Azure absent: {1, 2} only):**
        *   Swap Blue (1) pixels to Red (2).
        *   Swap Red (2) pixels to Blue (1).
        *   All other non-white pixels become white (0).

5.  **Default (No specific trigger matched):**
    *   The output grid is entirely white (0).
"""

def get_present_colors(grid_np):
    """Finds the set of unique non-zero colors in a numpy grid."""
    return set(grid_np.flatten()) - {0}

def transform(input_grid):
    """
    Applies a transformation rule based on the prioritized set of colors present.
    Rules involve color swaps, conditional conversions, positional flips,
    and handling based on the presence/absence of specific colors like Azure.
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

    # Rule 1: Magenta(6)/Orange(7) present
    if {6, 7}.issubset(present_colors):
        # Use a temporary grid to store the results of the Red/Yellow flip+swap
        # This prevents overwriting a pixel at (r, c) before its value is used
        # to determine the output at (r, width - 1 - c), especially if c = width - 1 - c.
        temp_flip = np.zeros_like(input_np)
        for r in range(height):
            for c in range(width):
                pixel = input_np[r, c]
                flipped_c = width - 1 - c
                # Check bounds for flipped column index
                is_flipped_c_valid = 0 <= flipped_c < width

                if pixel == 6:
                    output_np[r, c] = 7 # Magenta -> Orange
                elif pixel == 7:
                    output_np[r, c] = 6 # Orange -> Magenta
                elif pixel == 2:
                    # Red at (r, c) becomes Yellow at (r, flipped_c)
                    if is_flipped_c_valid:
                         temp_flip[r, flipped_c] = 4
                elif pixel == 4:
                    # Yellow at (r, c) becomes Red at (r, flipped_c)
                    if is_flipped_c_valid:
                        temp_flip[r, flipped_c] = 2
                # Other colors (like Azure 8) are ignored by default, remain 0 in output_np

        # Merge the flipped Red/Yellow pixels into the output grid.
        # Only update where temp_flip has a non-zero value.
        output_np[temp_flip != 0] = temp_flip[temp_flip != 0]

    # Rule 2: Blue(1)/Yellow(4) present (and Rule 1 didn't apply)
    elif {1, 4}.issubset(present_colors):
        for r in range(height):
            for c in range(width):
                pixel = input_np[r, c]
                if pixel == 4:
                    output_np[r, c] = 2 # Yellow -> Red
                elif pixel == 1:
                    output_np[r, c] = 7 # Blue -> Orange
                elif pixel == 8:
                    # Azure -> Red (top) / Orange (bottom) based on median row
                    if r <= median_row:
                        output_np[r, c] = 2
                    else:
                        output_np[r, c] = 7
                # Other original colors (Red 2, Orange 7, Magenta 6, etc.) become White(0)

    # Rule 3: Red(2)/Yellow(4) present (and Rules 1, 2 didn't apply)
    elif {2, 4}.issubset(present_colors):
         for r in range(height):
            for c in range(width):
                pixel = input_np[r, c]
                if pixel == 2:
                    output_np[r, c] = 4 # Red -> Yellow
                elif pixel == 4:
                    output_np[r, c] = 2 # Yellow -> Red
                # Other colors become White(0)

    # Rule 4: Blue(1)/Red(2) present (and Rules 1, 2, 3 didn't apply)
    elif {1, 2}.issubset(present_colors):
        has_azure = 8 in present_colors # Check if Azure is present for sub-casing
        for r in range(height):
            for c in range(width):
                pixel = input_np[r, c]
                if pixel == 1:
                    output_np[r, c] = 2 # Blue -> Red
                elif pixel == 2:
                    output_np[r, c] = 1 # Red -> Blue
                elif pixel == 8 and has_azure:
                     # Case 4a: {1, 2, 8} are present
                     output_np[r, c] = 1 # Azure -> Blue
                # Else (pixel is not 1, 2, or (8 when azure is present)):
                # - If pixel was 8 but azure is not present (Case 4b): Remains 0.
                # - If pixel was any other color: Remains 0.
                # -> Correctly handled by default initialization.

    # Default: If no specific trigger combination matched, output_np remains all zeros (white)

    # Convert numpy array back to list of lists for the final output
    return output_np.tolist()