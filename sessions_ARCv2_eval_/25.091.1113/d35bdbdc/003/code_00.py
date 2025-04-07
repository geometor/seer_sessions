import numpy as np
from typing import List, Tuple, Dict, Set, Optional

"""
The transformation identifies specific 3x3 square patterns in the input grid and applies rules based on these patterns. 
A 3x3 pattern is considered an 'object' if its 8 border pixels all have the same color (BorderColor) and its center pixel has a different color (CenterColor).

Rules:
1. Non-Standard Object Rule: If a 3x3 object contains any pixel whose color is neither the BorderColor nor the CenterColor, the entire 9-pixel area of the object is removed (replaced with white, 0). (Note: This specific condition wasn't observed in training examples but is kept as a potential rule).
2. Standard Object Rules: If a 3x3 object contains only pixels with the BorderColor or the CenterColor ('Standard Object'), the action depends on the specific pair (BorderColor, CenterColor):
    a. Removal: If the pair matches a predefined set of 'Removal Pairs', the entire 9-pixel area is removed (replaced with white, 0).
    b. Modification: If the pair matches a predefined set of 'Modification Pairs', only the center pixel of the object is changed to a specific 'NewCenterColor'.
    c. No Change: If a Standard Object's pair matches neither Removal nor Modification rules, it remains unchanged.

Application Strategy:
A two-pass approach is used:
- First Pass: Identify all 3x3 objects that trigger a removal (either Non-Standard Objects or Standard Objects matching Removal Pairs). Mark these 9-pixel areas in a temporary boolean mask.
- Apply Removals: Update the output grid by setting all pixels marked in the mask to white (0).
- Second Pass: Identify all Standard Objects matching Modification Pairs. If the center pixel of such an object was *not* marked for removal in the first pass, update the center pixel in the output grid to the corresponding NewCenterColor.
"""

# --- Constants for Rules ---

# Standard objects with these (border_color, center_color) pairs are completely removed.
REMOVAL_PAIRS: Set[Tuple[int, int]] = {
    (4, 2),  # Yellow border, Red center   (Rule added based on analysis)
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
    Checks if the 3x3 subgrid starting at (r, c) forms a valid object based on border/center colors.

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
    # Ensure the 3x3 grid fits within bounds
    if r + 2 >= rows or c + 2 >= cols:
        return False, None, None, False

    subgrid = grid[r:r+3, c:c+3]
    center_color = subgrid[1, 1]

    # Collect border pixels (top row, bottom row, middle-sides)
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
            # Check if the pixel color is different from both border and center
            if pixel_color != border_color and pixel_color != center_color:
                has_extra_color = True
                break # Found an extra color, no need to check further
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
    output_np = np.copy(input_np) # Start with a copy of the input
    rows, cols = input_np.shape

    # Create a mask to track which 3x3 areas should be completely removed (set to white 0)
    removed_mask = np.zeros_like(input_np, dtype=bool)

    # --- First Pass: Identify and mark areas for removal ---
    # Iterate through all possible top-left corners (r, c) of 3x3 subgrids
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check the 3x3 area based on the original input grid
            is_object, border_color, center_color, has_extra_color = check_3x3_object(input_np, r, c)

            if is_object:
                # Rule 1: Remove if it's a Non-standard object (has extra colors)
                if has_extra_color:
                    removed_mask[r:r+3, c:c+3] = True
                else:
                    # Standard object: Check Rule 2a (Removal Pairs)
                    pair = (border_color, center_color)
                    if pair in REMOVAL_PAIRS:
                        removed_mask[r:r+3, c:c+3] = True

    # --- Apply Removals ---
    # Set all pixels marked in the mask to white (0) in the output grid
    output_np[removed_mask] = 0

    # --- Second Pass: Identify and apply modifications ---
    # Iterate again through all possible top-left corners
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check the 3x3 area again based on the original input grid
            is_object, border_color, center_color, has_extra_color = check_3x3_object(input_np, r, c)

            # Check if it's a Standard object (no extra colors)
            if is_object and not has_extra_color:
                # Check Rule 2b (Modification Pairs)
                pair = (border_color, center_color)
                if pair in MODIFICATION_RULES:
                    # Crucially, only modify if the center pixel WASN'T part of a removed area
                    if not removed_mask[r+1, c+1]:
                        new_center_color = MODIFICATION_RULES[pair]
                        # Apply modification only to the center pixel in the output grid
                        output_np[r+1, c+1] = new_center_color

    # Convert the final numpy array back to a list of lists for the required output format
    return output_np.tolist()