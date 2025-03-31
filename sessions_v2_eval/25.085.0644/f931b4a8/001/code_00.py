import numpy as np
from collections import Counter

"""
The transformation rule operates based on the content of the bottom-left (BL) and bottom-right (BR) quadrants of the input grid.

1.  Divide the input grid into four equal quadrants: Top-Left (TL), Top-Right (TR), Bottom-Left (BL), and Bottom-Right (BR). Let the dimensions of each quadrant be `h` rows and `w` columns.
2.  Examine the Bottom-Right (BR) quadrant:
    a.  If the BR quadrant consists entirely of white (0) pixels:
        The output grid is an exact copy of the Bottom-Left (BL) quadrant.
    b.  Else if the BR quadrant consists entirely of a single non-white color (`Color_BR`) AND the BL quadrant also consists entirely of a single non-white color (`Color_BL`):
        Create a new grid with 3 rows and `w` columns. Fill the first row with `Color_BR`, the second with `Color_BL`, and the third with `Color_BR`.
    c.  Else (the BR quadrant contains a pattern mixing white (0) and other colors):
        i.  Determine the `Replacement_Color` by finding the most frequent non-white color in the BL quadrant.
        ii. Create a temporary `Pattern_Grid` of size `h` x `w` by copying the BR quadrant and replacing every white (0) pixel with the `Replacement_Color`.
        iii. Check the quadrant height `h`:
            1.  If `h` is 4: Tile the `Pattern_Grid` 4x4 times to create a 16x16 output.
            2.  If `h` is 8: Create a 10x10 output grid filled with `Replacement_Color`, then place the `Pattern_Grid` in the top-left 8x8 area.
"""

def get_quadrants(grid):
    """Divides a grid into four equal quadrants."""
    h, w = grid.shape
    h_half, w_half = h // 2, w // 2
    tl = grid[0:h_half, 0:w_half]
    tr = grid[0:h_half, w_half:w]
    bl = grid[h_half:h, 0:w_half]
    br = grid[h_half:h, w_half:w]
    return tl, tr, bl, br

def is_solid_color(grid):
    """Checks if a grid consists of a single color. Returns (True, color) or (False, None)."""
    unique_colors = np.unique(grid)
    if len(unique_colors) == 1:
        return True, unique_colors[0]
    else:
        return False, None

def get_most_frequent_non_white(grid):
    """Finds the most frequent non-white color in a grid."""
    colors, counts = np.unique(grid, return_counts=True)
    non_white_colors = []
    non_white_counts = []
    for color, count in zip(colors, counts):
        if color != 0:
            non_white_colors.append(color)
            non_white_counts.append(count)

    if not non_white_colors:
        # Handle cases where BL might be all white (though not seen in examples for this path)
        # Defaulting to a common color like black (5) or blue (1) might be needed,
        # but based on examples, BL should have non-white colors in this case.
        # For now, assume at least one non-white exists if this function is called.
        # Or perhaps return a sentinel value? Let's raise an error if no non-white found.
         raise ValueError("Bottom-Left quadrant has no non-white colors when expected.")


    # Find the index of the max count among non-white colors
    max_count_index = np.argmax(non_white_counts)
    return non_white_colors[max_count_index]


def transform(input_grid):
    """Applies the transformation rule based on quadrant analysis."""
    input_np = np.array(input_grid, dtype=int)
    h, w = input_np.shape
    h_half, w_half = h // 2, w // 2

    # 1. Divide into quadrants
    tl, tr, bl, br = get_quadrants(input_np)

    # 2. Examine the BR quadrant
    br_is_solid, br_color = is_solid_color(br)

    # 2a. Case 1: BR is solid white
    if br_is_solid and br_color == 0:
        output_grid = bl.copy()

    # 2b. Case 2: BR is solid non-white and BL is solid non-white
    elif br_is_solid and br_color != 0:
        bl_is_solid, bl_color = is_solid_color(bl)
        if bl_is_solid and bl_color != 0:
             # Create 3xw grid
             output_grid = np.zeros((3, w_half), dtype=int)
             output_grid[0, :] = br_color # Use br_color (the solid color of BR)
             output_grid[1, :] = bl_color # Use bl_color (the solid color of BL)
             output_grid[2, :] = br_color # Use br_color again
        else:
             # This specific sub-case (BR solid non-white, BL not solid) isn't covered by examples.
             # Assuming the main 'else' case (pattern logic) should handle patterned BL.
             # We fall through to the pattern logic. If BL *was* solid white, get_most_frequent would fail.
             # Re-evaluating logic based on example 5: BR is 1111, BL is 6666. Output is 1,6,1 rows.
             # Correcting the logic for Case 2b:
             # It seems this case applies even if BL isn't solid, if BR *is* solid non-white.
             # Let's stick to the precise condition from analysis: BR solid non-white AND BL solid non-white.
             # Example 5 fits this: BR=solid(1), BL=solid(6). Output=3x4 of [row(1), row(6), row(1)]. Code is correct for this.
             # What if BL was patterned? Need to default to Case 2c. Let's refine the flow.

             # Refined flow: Check Case 1, then Case 2c (pattern), then Case 2b.
             # This prioritizes the pattern rule if BR isn't solid white.
             # Let's stick to the original flow but ensure Case 2b is strictly checked.
             # If BL isn't solid non-white, this condition fails, and we proceed to Case 2c.
             pass # Allow falling through to Case 2c


    # 2c. Case 3: BR contains a pattern (not solid white, and not covered by Case 2b)
    # This 'else' block catches:
    # - BR is patterned (contains 0 and other colors)
    # - BR is solid non-white, but BL is NOT solid non-white (patterned or solid white)
    if 'output_grid' not in locals(): # If neither Case 1 nor Case 2b was fully met
        # i. Determine Replacement_Color from BL
        replacement_color = get_most_frequent_non_white(bl)

        # ii. Create Pattern_Grid by replacing white in BR
        pattern_grid = br.copy()
        pattern_grid[pattern_grid == 0] = replacement_color

        # iii. Resize based on quadrant height h_half
        if h_half == 4:
            # Tile 4x4 -> 16x16
            output_grid = np.tile(pattern_grid, (4, 4))
        elif h_half == 8:
            # Pad to 10x10
            output_grid = np.full((h_half + 2, w_half + 2), replacement_color, dtype=int)
            output_grid[0:h_half, 0:w_half] = pattern_grid
        else:
            # Should not happen based on examples, but good practice
            raise ValueError(f"Unexpected quadrant height: {h_half}")


    return output_grid.tolist() # Convert back to list of lists if required by framework