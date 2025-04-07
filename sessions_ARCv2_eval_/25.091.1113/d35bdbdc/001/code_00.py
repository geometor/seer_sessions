import numpy as np
from typing import List, Tuple, Dict, Set, Optional

"""
Identify 3x3 square objects based on a uniform border color and a different center color.
These objects are processed based on rules determined by the specific border and center color pair,
and whether any 'extra' colors (different from both border and center) exist within the 3x3 square.

1. Define a 3x3 object: 8 border pixels are the same color (BorderColor), center pixel is a different color (CenterColor).
2. Categorize objects:
    - Non-standard Object: Contains at least one pixel whose color is neither BorderColor nor CenterColor.
    - Standard Object: All 9 pixels are either BorderColor or CenterColor.
3. Define transformation rules:
    - Rule 1: If an object is Non-standard, remove it (replace all 9 pixels with white (0)).
    - Rule 2: If an object is Standard, apply rules based on the (BorderColor, CenterColor) pair:
        - Removal Pairs: Certain pairs cause the entire 3x3 object to be removed (set to white (0)).
        - Modification Pairs: Certain pairs cause only the center pixel to change to a specific NewColor.
        - Other pairs: If a standard object's pair doesn't match any removal or modification rule, it remains unchanged.
4. Application Strategy:
    - Use a two-pass approach on a copy of the input grid.
    - First Pass: Identify all 3x3 areas corresponding to Non-standard objects or Standard objects matching Removal Pairs. Mark these areas for removal using a boolean mask.
    - Apply Removals: Set all pixels marked in the mask to white (0) in the output grid.
    - Second Pass: Identify all Standard objects matching Modification Pairs based on the original input grid. If the center pixel of such an object was *not* marked for removal in the first pass, change the center pixel in the output grid to the specified NewColor.
"""

# --- Constants for Rules ---

# Standard objects with these (border_color, center_color) pairs are completely removed.
REMOVAL_PAIRS: Set[Tuple[int, int]] = {
    (1, 3),  # Blue border, Green center
    (2, 6),  # Red border, Magenta center
    (3, 2),  # Green border, Red center
    (4, 8),  # Yellow border, Azure center
    (4, 3),  # Yellow border, Green center
    (3, 6),  # Green border, Magenta center
    (2, 9),  # Red border, Maroon center
}

# Standard objects with these (border_color, center_color) pairs have their center pixel modified.
# Value is the new_center_color.
MODIFICATION_RULES: Dict[Tuple[int, int], int] = {
    (3, 4): 2,  # Green border, Yellow center -> Red center
    (6, 1): 3,  # Magenta border, Blue center -> Green center
    (8, 3): 2,  # Azure border, Green center -> Red center
    (1, 4): 8,  # Blue border, Yellow center -> Azure center
    (1, 2): 9,  # Blue border, Red center -> Maroon center
    (7, 4): 3,  # Orange border, Yellow center -> Green center
}

# --- Helper Function ---

def check_3x3_object(grid: np.ndarray, r: int, c: int) -> Tuple[bool, Optional[int], Optional[int], bool]:
    """
    Checks if the 3x3 subgrid starting at (r, c) forms a valid object.

    Args:
        grid: The input numpy array.
        r: Top row index.
        c: Left column index.

    Returns:
        A tuple: (is_object, border_color, center_color, has_extra_color)
        - is_object (bool): True if it matches the 3x3 border/center structure.
        - border_color (Optional[int]): The color of the border pixels if is_object is True.
        - center_color (Optional[int]): The color of the center pixel if is_object is True.
        - has_extra_color (bool): True if any pixel in the 3x3 area is neither
                                  border_color nor center_color (only relevant if is_object is True).
    """
    rows, cols = grid.shape
    if r + 2 >= rows or c + 2 >= cols:
        return False, None, None, False  # Out of bounds

    subgrid = grid[r:r+3, c:c+3]
    center_color = subgrid[1, 1]
    
    # Collect border pixels
    border_pixels = [
        subgrid[0, 0], subgrid[0, 1], subgrid[0, 2],
        subgrid[1, 0],                 subgrid[1, 2],
        subgrid[2, 0], subgrid[2, 1], subgrid[2, 2]
    ]

    # Check if all border pixels are the same color
    border_color = border_pixels[0]
    if not all(p == border_color for p in border_pixels):
        return False, None, None, False

    # Check if center color is different from border color
    if center_color == border_color:
        return False, None, None, False

    # Now we know it's structurally a valid object. Check for "extra" colors.
    has_extra_color = False
    for i in range(3):
        for j in range(3):
            pixel_color = subgrid[i, j]
            if pixel_color != border_color and pixel_color != center_color:
                has_extra_color = True
                break
        if has_extra_color:
            break

    return True, border_color, center_color, has_extra_color

# --- Main Transformation Function ---

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rules to the input grid.
    Identifies specific 3x3 objects and either removes them or modifies their center pixel
    based on border/center colors and the presence of extra colors.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Create a mask to track which cells belong to a 3x3 area marked for removal
    removed_mask = np.zeros_like(input_np, dtype=bool)

    # --- First Pass: Identify and mark areas for removal ---
    # Iterate through all possible top-left corners of 3x3 subgrids
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check the 3x3 area based on the original input grid
            is_object, border_color, center_color, has_extra_color = check_3x3_object(input_np, r, c)

            if is_object:
                if has_extra_color:
                    # Non-standard object: mark for removal
                    removed_mask[r:r+3, c:c+3] = True
                else:
                    # Standard object: check removal rules
                    pair = (border_color, center_color)
                    if pair in REMOVAL_PAIRS:
                        # Mark for removal based on standard object removal rule
                        removed_mask[r:r+3, c:c+3] = True

    # --- Apply Removals ---
    # Set all pixels marked in the mask to white (0) in the output grid
    output_np[removed_mask] = 0

    # --- Second Pass: Identify and apply modifications ---
    # Iterate again through all possible top-left corners
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Important: Check if the center pixel of this potential object was already removed
            if removed_mask[r+1, c+1]:
                continue # Skip if center was part of a removed area

            # Check the 3x3 area again based on the original input grid
            is_object, border_color, center_color, has_extra_color = check_3x3_object(input_np, r, c)

            if is_object and not has_extra_color:
                # Standard object: check modification rules
                pair = (border_color, center_color)
                if pair in MODIFICATION_RULES:
                     # Check if the whole 3x3 area wasn't marked for removal 
                     # (this check might be slightly redundant given the center check, but safer)
                    if not removed_mask[r:r+3, c:c+3].any():
                        new_center_color = MODIFICATION_RULES[pair]
                        # Apply modification only to the center pixel in the output grid
                        output_np[r+1, c+1] = new_center_color

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()