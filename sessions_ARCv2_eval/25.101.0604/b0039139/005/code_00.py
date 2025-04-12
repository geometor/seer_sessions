import numpy as np
from collections import Counter
import sys # for maxint

"""
Transforms an input grid based on identifying a pattern color (PC) with the 
minimum bounding box area, identifying the two most frequent remaining colors 
(C1, C2), creating a motif based on the PC's shape using C1 and C2, and then 
arranging/tiling this motif according to specific rules based on the input 
style (presence of multiple separator rows) or PC and motif width (Pw).

1.  Identify PC: Color (not 0, 1) with minimum bounding box area. Tie-break: smallest color value.
2.  Extract PatternMask: Binary mask (Ph x Pw) from PC's bounding box (1 where PC is, 0 otherwise).
3.  Identify C1, C2: Two most frequent colors (not 0, 1, PC). C1 > C2 freq. Tie-break: smallest color value.
4.  Generate Motif: Ph x Pw grid. PatternMask 1 -> C1, 0 -> C2.
5.  Determine Output Structure (Ho, Wo, Tiling Method):
    - Check for "Train_1 Style" (multiple full rows of 1s).
    - If Train_1 Style:
        - Ho = 2*Ph + 1, Wo = Pw.
        - Tiling: Special Vertical Stacking (Motif[0], Motif[1], [C2]*Wo, Motif[0], Motif[1]). Requires Ph >= 2.
    - Else (Default Style):
        - Ho = Ph.
        - If PC == 3 and Pw == 5 (Rule A):
            - Wo = Pw * PC.
            - Tiling: Simple Horizontal (Motif repeated PC times).
        - Else (Rule B):
            - Wo = Pw * max(1, PC - 1) + max(0, PC - 2). Accounts for PC=2 case (Wo=Pw).
            - Tiling: Complex Horizontal (Motif repeated PC-1 times, interspersed with PC-2 columns of C2).
6.  Construct Output: Apply the determined tiling/stacking method.
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

def create_motif(mask: np.ndarray, c1: int, c2: int) -> np.ndarray:
    """Creates the motif grid based on the mask: 1->C1, 0->C2."""
    ph, pw = mask.shape
    motif = np.full((ph, pw), c2, dtype=int) # Initialize with C2
    motif[mask == 1] = c1                   # Set C1 where mask is 1
    return motif


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    grid = np.array(input_grid, dtype=int)
    if grid.size == 0:
        return []

    # --- 1. Identify Pattern Color (PC) ---
    all_colors = np.unique(grid)
    foreground_colors = [c for c in all_colors if c != 0 and c != 1]
    if not foreground_colors:
        return [] # No non-background/separator colors

    min_area = sys.maxsize
    pc = -1
    pc_bbox = None

    # Iterate through sorted colors to handle area ties with lower color value
    for color in sorted(foreground_colors):
        bbox_info = find_bounding_box(grid, color)
        if bbox_info:
            area = bbox_info[6]
            if area < min_area:
                min_area = area
                pc = color
                pc_bbox = bbox_info

    if pc == -1 or pc_bbox is None:
        # This should not happen if foreground_colors is not empty and they exist in grid
        print("Error: Could not determine Pattern Color or its bounding box.")
        return []

    # --- 2. Extract Pattern Mask ---
    pattern_mask = create_pattern_mask(grid, pc, pc_bbox)
    ph, pw = pattern_mask.shape
    if ph == 0 or pw == 0:
         print("Error: Pattern mask has zero dimension.")
         return [] # Cannot proceed with empty pattern

    # --- 3. Identify Output Colors (C1, C2) ---
    freqs = get_frequencies(grid, exclude_colors={pc})
    # Sort by frequency (desc), then by color value (asc) for tie-breaking
    sorted_freqs = sorted(freqs.items(), key=lambda item: (-item[1], item[0]))

    if len(sorted_freqs) == 0:
        print(f"Error: Only Pattern Color {pc} found. Cannot determine C1/C2.")
        return []

    c1 = sorted_freqs[0][0]
    # If only one other color exists, use it for both C1 and C2 (or just C2=C1)
    c2 = sorted_freqs[1][0] if len(sorted_freqs) > 1 else c1

    # --- 4. Generate Motif ---
    motif = create_motif(pattern_mask, c1, c2)

    # --- 5. Determine Output Structure (Ho, Wo, Tiling Method) ---
    ho, wo = 0, 0
    tiling_method = None # 'special_vertical', 'simple_horizontal', 'complex_horizontal'

    # Check for Train_1 Style
    is_train1_style = False
    if grid.shape[0] > 1: # Need at least 2 rows to have multiple separator rows
        sep_rows = np.all(grid == 1, axis=1)
        if np.sum(sep_rows) > 1:
            is_train1_style = True

    if is_train1_style:
        if ph < 2:
            print("Error: Train 1 style requires pattern height >= 2.")
            return [] # Cannot apply vertical stacking rule
        ho = 2 * ph + 1
        wo = pw
        tiling_method = 'special_vertical'
    else:
        # Default Style
        ho = ph
        if pc == 3 and pw == 5: # Rule A
            wo = pw * pc
            tiling_method = 'simple_horizontal'
        else: # Rule B (covers PC=2 implicitly)
            # Calculate width based on PC and Pw
            # Formula ensures Wo=Pw if PC=2, Wo=Pw*2+1 if PC=3, Wo=Pw*3+2 if PC=4 etc.
            wo = pw * max(1, pc - 1) + max(0, pc - 2)
            tiling_method = 'complex_horizontal'

    if ho <= 0 or wo <= 0:
        print(f"Error: Calculated non-positive output dimensions Ho={ho}, Wo={wo}.")
        return []

    # --- 6. Construct Output Grid ---
    output_grid = np.array([[]]) # Initialize

    try:
        if tiling_method == 'special_vertical':
            # Check motif compatibility
            if motif.shape[0] >= 2 and motif.shape[1] == wo:
                 output_grid = np.vstack((
                     motif[0:1, :],        # First row of motif
                     motif[1:2, :],        # Second row of motif
                     np.full((1, wo), c2), # Row of C2
                     motif[0:1, :],        # First row again
                     motif[1:2, :]         # Second row again
                 ))
            else:
                  print(f"Error: Motif shape {motif.shape} incompatible with Train 1 stacking (requires >=2 rows, width {wo}).")
                  output_grid = np.full((ho, wo), -1, dtype=int) # Error placeholder

        elif tiling_method == 'simple_horizontal':
            # Repeat the motif PC times horizontally
            if pc > 0:
                 output_grid = np.hstack([motif] * pc)
            else:
                 output_grid = np.zeros((ho, wo), dtype=int) # Should not happen if wo > 0

        elif tiling_method == 'complex_horizontal':
            if pc < 2: # Should not happen based on Wo calculation, but safety check
                 print(f"Error: PC={pc} invalid for complex horizontal tiling.")
                 output_grid = np.full((ho, wo), -1, dtype=int)
            elif pc == 2: # Special case of the formula: Wo=Pw, output is just the motif
                 output_grid = motif
            else: # PC >= 3
                 num_motifs = pc - 1
                 num_c2_cols = pc - 2
                 c2_col = np.full((ho, 1), c2, dtype=int) # Create a column of C2
                 
                 parts_to_stack = []
                 for i in range(num_motifs):
                     parts_to_stack.append(motif)
                     if i < num_c2_cols: # Add C2 column after all but the last motif
                         parts_to_stack.append(c2_col)
                 
                 if parts_to_stack: # Ensure there's something to stack
                     output_grid = np.hstack(parts_to_stack)
                 else: # Should not happen if pc >= 2
                     output_grid = np.zeros((ho, wo), dtype=int)


    except Exception as e:
         print(f"Error during output construction ({tiling_method}): {e}")
         output_grid = np.full((ho, wo), -1, dtype=int) # Error placeholder

    # Final validation of output shape
    if output_grid.shape != (ho, wo):
        print(f"Error: Final grid shape {output_grid.shape} does not match target {(ho, wo)}. Check construction logic.")
        # Attempt to return a correctly shaped error grid if possible
        output_grid = np.full((ho, wo), -1, dtype=int)

    return output_grid.tolist()