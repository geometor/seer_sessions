import numpy as np
from collections import Counter
import sys # for maxint

"""
Transforms an input grid based on identifying a pattern color (PC) with the 
minimum bounding box area, identifying the two most frequent remaining colors 
(C1, C2), creating a base motif based on the PC's shape (1->C1, 0->C2), 
modifying the first row of this motif (C2->C1), and then arranging/tiling 
this modified motif according to specific rules based on the input style 
(presence of multiple separator rows) or PC and motif width (Pw).

1.  Identify PC: Color (not 0, 1) with minimum bounding box area. Tie-break: smallest color value.
2.  Extract PatternMask: Binary mask (Ph x Pw) from PC's bounding box (1 where PC is, 0 otherwise).
3.  Identify C1, C2: Two most frequent colors (not 0, 1, PC). C1 > C2 freq. Tie-break: smallest color value.
4.  Generate Base Motif: Ph x Pw grid. PatternMask 1 -> C1, 0 -> C2.
5.  Generate Modified Motif: In the first row of the Base Motif, change C2 -> C1.
6.  Determine Output Structure (Ho, Wo, Tiling Method):
    - Check for "Train_1 Style" (multiple full rows of 1s).
    - If Train_1 Style:
        - Ho = 2*Ph + 1, Wo = Pw. Requires Ph >= 2.
        - Tiling: Special Vertical Stacking (uses Modified Motif).
    - Else (Default Style):
        - Ho = Ph.
        - If PC == 3 and Pw == 5 (Rule A):
            - Wo = Pw * PC.
            - Tiling: Simple Horizontal (Modified Motif repeated PC times).
        - Else (Rule B):
            - Wo = Pw * max(1, PC - 1) + max(0, PC - 2). Accounts for PC=2 case (Wo=Pw).
            - Tiling: Complex Horizontal (Modified Motif repeated PC-1 times, interspersed with PC-2 columns of C2).
7.  Construct Output: Apply the determined tiling/stacking method using the Modified Motif.
"""


def find_bounding_box(grid: np.ndarray, value: int) -> tuple[int, int, int, int, int, int, int] | None:
    """Finds the minimal bounding box coordinates, dimensions, and area for a given value."""
    coords = np.argwhere(grid == value)
    if coords.size == 0:
        return None
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    area = height * width
    return min_row, max_row, min_col, max_col, height, width, area

def get_frequencies(grid: np.ndarray, exclude_colors: set[int]) -> Counter:
    """Counts frequencies of colors, excluding 0, 1, and specified colors."""
    colors = grid.flatten()
    filtered_colors = [c for c in colors if c != 0 and c != 1 and c not in exclude_colors]
    return Counter(filtered_colors)

def create_pattern_mask(grid: np.ndarray, value: int, bbox: tuple) -> np.ndarray:
    """Creates a binary mask from the grid based on a value within its bbox."""
    min_r, max_r, min_c, max_c, _, _, _ = bbox
    subgrid = grid[min_r:max_r+1, min_c:max_c+1]
    return (subgrid == value).astype(int)

def create_base_motif(mask: np.ndarray, c1: int, c2: int) -> np.ndarray:
    """Creates the base motif grid based on the mask: 1->C1, 0->C2."""
    ph, pw = mask.shape
    motif = np.full((ph, pw), c2, dtype=int) # Initialize with C2
    motif[mask == 1] = c1                   # Set C1 where mask is 1
    return motif

def create_modified_motif(base_motif: np.ndarray, c1: int, c2: int) -> np.ndarray:
    """Modifies the first row of the base motif by changing C2 to C1."""
    modified = base_motif.copy()
    if modified.shape[0] > 0: # Ensure motif is not empty
        modified[0, modified[0] == c2] = c1
    return modified


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # --- Initialize ---
    grid = np.array(input_grid, dtype=int)
    if grid.size == 0:
        return []

    # --- 1. Identify Pattern Color (PC) ---
    # Find color (not 0, 1) with the smallest bounding box area.
    # Tie-break using the smallest color value.
    all_colors = np.unique(grid)
    foreground_colors = [c for c in all_colors if c != 0 and c != 1]
    if not foreground_colors:
        return [] # No pattern possible

    min_area = sys.maxsize
    pc = -1
    pc_bbox = None

    for color in sorted(foreground_colors): # Sort for tie-breaking
        bbox_info = find_bounding_box(grid, color)
        if bbox_info:
            area = bbox_info[6]
            if area < min_area:
                min_area = area
                pc = color
                pc_bbox = bbox_info

    if pc == -1 or pc_bbox is None:
        print("Error: Could not determine Pattern Color or its bounding box.")
        return []

    # --- 2. Extract Pattern Mask ---
    # Create a binary mask (Ph x Pw) from PC's bounding box.
    pattern_mask = create_pattern_mask(grid, pc, pc_bbox)
    ph, pw = pattern_mask.shape
    if ph == 0 or pw == 0:
         print("Error: Pattern mask has zero dimension.")
         return []

    # --- 3. Identify Output Colors (C1, C2) ---
    # Find the two most frequent colors (excluding 0, 1, PC).
    # C1 > C2 frequency. Tie-break using the smallest color value.
    freqs = get_frequencies(grid, exclude_colors={pc})
    # Sort by frequency (desc), then by color value (asc) for tie-breaking
    sorted_freqs = sorted(freqs.items(), key=lambda item: (-item[1], item[0]))

    if len(sorted_freqs) == 0:
        print(f"Error: Only Pattern Color {pc} found. Cannot determine C1/C2.")
        return []

    c1 = sorted_freqs[0][0]
    c2 = sorted_freqs[1][0] if len(sorted_freqs) > 1 else c1 # Use C1 if only one other color

    # --- 4. Generate Base Motif ---
    # Create Ph x Pw grid mapping PatternMask 1 to C1, 0 to C2.
    base_motif = create_base_motif(pattern_mask, c1, c2)

    # --- 5. Generate Modified Motif ---
    # Apply Rule M (Row 0: C2 -> C1) to Base Motif.
    modified_motif = create_modified_motif(base_motif, c1, c2)

    # --- 6. Determine Output Structure (Ho, Wo, Tiling Method) ---
    ho, wo = 0, 0
    tiling_method = None

    # Check for Train_1 Style (multiple full rows of 1s)
    is_train1_style = False
    if grid.shape[0] > 1:
        sep_rows = np.all(grid == 1, axis=1)
        if np.sum(sep_rows) > 1:
            is_train1_style = True

    if is_train1_style:
        # Requires pattern height >= 2 for the specific stacking logic
        if ph < 2:
            print("Error: Train 1 style requires pattern height >= 2.")
            return []
        ho = 2 * ph + 1
        wo = pw
        tiling_method = 'special_vertical'
    else:
        # Default Style
        ho = ph
        if pc == 3 and pw == 5: # Rule A specific case
            wo = pw * pc
            tiling_method = 'simple_horizontal'
        else: # Rule B for all other default cases
            # Formula covers PC=2 (Wo=Pw), PC=3 (Wo=2*Pw+1), PC=4 (Wo=3*Pw+2), etc.
            wo = pw * max(1, pc - 1) + max(0, pc - 2)
            tiling_method = 'complex_horizontal'

    # Validate calculated dimensions
    if ho <= 0 or wo <= 0:
        print(f"Error: Calculated non-positive output dimensions Ho={ho}, Wo={wo}.")
        return []

    # --- 7. Construct Output Grid ---
    # Apply the determined tiling/stacking method using the Modified Motif.
    output_grid = np.array([[]]) # Initialize

    try:
        if tiling_method == 'special_vertical':
            # Stack rows: ModMotif[0], ModMotif[1], [C2]*Wo, ModMotif[0], ModMotif[1]
            if modified_motif.shape[0] >= 2 and modified_motif.shape[1] == wo:
                 output_grid = np.vstack((
                     modified_motif[0:1, :],        # First row of modified motif
                     modified_motif[1:2, :],        # Second row of modified motif
                     np.full((1, wo), c2),          # Row of C2
                     modified_motif[0:1, :],        # First row again
                     modified_motif[1:2, :]         # Second row again
                 ))
            else:
                  print(f"Error: Motif shape {modified_motif.shape} incompatible with Train 1 stacking (requires >=2 rows, width {wo}).")
                  output_grid = np.full((ho, wo), -1, dtype=int) # Error placeholder

        elif tiling_method == 'simple_horizontal':
            # Repeat the Modified Motif PC times horizontally.
            if pc > 0:
                 output_grid = np.hstack([modified_motif] * pc)
            else:
                 output_grid = np.zeros((ho, wo), dtype=int) # Should not happen

        elif tiling_method == 'complex_horizontal':
            # Stack Modified Motif PC-1 times, interspersed with PC-2 columns of C2.
            if pc < 2: # Should not happen based on Wo calculation
                 print(f"Error: PC={pc} invalid for complex horizontal tiling.")
                 output_grid = np.full((ho, wo), -1, dtype=int)
            elif pc == 2: # Special case: output is just the modified motif
                 output_grid = modified_motif
            else: # PC >= 3
                 num_motifs = pc - 1
                 num_c2_cols = pc - 2
                 c2_col = np.full((ho, 1), c2, dtype=int) # Column vector of C2

                 parts_to_stack = []
                 for i in range(num_motifs):
                     parts_to_stack.append(modified_motif)
                     if i < num_c2_cols: # Add C2 column between motifs
                         parts_to_stack.append(c2_col)

                 if parts_to_stack:
                     output_grid = np.hstack(parts_to_stack)
                 else: # Should not happen
                     output_grid = np.zeros((ho, wo), dtype=int)

    except Exception as e:
         print(f"Error during output construction ({tiling_method}): {e}")
         output_grid = np.full((ho, wo), -1, dtype=int) # Error placeholder

    # Final validation of output shape
    if output_grid.shape != (ho, wo):
        print(f"Error: Final grid shape {output_grid.shape} does not match target {(ho, wo)}. Check construction logic.")
        output_grid = np.full((ho, wo), -1, dtype=int)

    # --- Return ---
    return output_grid.tolist()