"""
1. Identify the contiguous block of white pixels (color 0) in the input grid. Determine its top-left corner coordinates (`wr`, `wc`) and its dimensions (height `wh`, width `ww`). The output grid will have these dimensions (`wh`, `ww`).
2. Find all red pixels (color 2) located in the same rows as the white block (rows `wr` to `wr + wh - 1`). Call these "relevant red pixels".
3. Determine the starting coordinates (`otr`, `otc`) for extracting the output subgrid based on the presence and location of relevant red pixels:
    a.  **If no relevant red pixels exist:**
        *   Set the starting row `otr = wr + 2`.
        *   Set the starting column `otc = wc`.
    b.  **If relevant red pixels exist:**
        *   Set the starting row `otr = wr`.
        *   Find the minimum column index (`min_rc`) among all relevant red pixels.
        *   **If `min_rc` is greater than or equal to `wc`** (the leftmost relevant red pixel is at or to the right of the white block's left edge):
            *   Set the starting column `otc = wc + 2`.
        *   **If `min_rc` is less than `wc`** (the leftmost relevant red pixel is to the left of the white block's left edge):
            *   Consider only the relevant red pixels whose column index `c` is less than `wc`.
            *   Calculate the horizontal distance from the white block's left edge (`wc`) to each of these pixels (`wc - c`).
            *   Find the minimum of these distances (`min_dist`).
            *   Set the starting column `otc = wc - (min_dist + 2)`.
4. Extract the subgrid of size `wh` x `ww` from the input grid, starting at the calculated coordinates (`otr`, `otc`). This subgrid is the final output.
"""

import numpy as np
from typing import List, Tuple, Optional

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows.tolist(), cols.tolist())) # Ensure standard int types

def find_bounding_box(coords: List[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the top-left corner (min_row, min_col) and dimensions (height, width)
    of a bounding box containing all given coordinates.
    Assumes coordinates represent a contiguous block for the white block case.
    Returns None if coords is empty.
    """
    if not coords:
        return None
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return min_row, min_col, height, width

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    input_h, input_w = input_np.shape

    # 1. Identify the White Block
    white_pixels = find_pixels(input_np, 0)
    if not white_pixels:
        # Handle case where no white block is found (return empty or error)
        # Based on examples, a white block seems guaranteed.
        return [[]] 
    
    white_block_info = find_bounding_box(white_pixels)
    # This check should ideally not fail if white_pixels is not empty
    if white_block_info is None:
         return [[]] 
    wr, wc, wh, ww = white_block_info

    # 2. Find Relevant Red Pixels
    red_pixels = find_pixels(input_np, 2)
    relevant_red_pixels = [
        (r, c) for r, c in red_pixels if wr <= r < wr + wh
    ]

    # 3. Determine Extraction Start Coordinates (otr, otc)
    otr, otc = -1, -1 # Initialize with invalid values
    
    if not relevant_red_pixels:
        # Case 3a: No relevant red pixels
        otr = wr + 2
        otc = wc
    else:
        # Case 3b: Relevant red pixels exist
        otr = wr
        
        # Find the minimum column index among relevant red pixels
        min_rc = min(c for r, c in relevant_red_pixels)
        
        if min_rc >= wc:
            # Case 3b(i): Leftmost relevant red is at or right of white block
            otc = wc + 2
        else:
            # Case 3b(ii): Leftmost relevant red is left of white block
            # Filter for relevant red pixels strictly to the left of the white block
            left_red_pixels = [(r, c) for r, c in relevant_red_pixels if c < wc]
            
            # This should always find pixels since min_rc < wc
            if not left_red_pixels:
                 # This case is theoretically impossible if min_rc < wc, but included for robustness
                 print("Error: min_rc < wc but no red pixels found left of wc.")
                 return [[]] # Or handle error appropriately

            # Calculate distances from white block's left edge
            distances = [wc - c for r, c in left_red_pixels]
            
            # Find the minimum distance
            min_dist = min(distances)
            
            # Calculate the output column based on the minimum distance
            otc = wc - (min_dist + 2)

    # 4. Extract Output Subgrid
    
    # Calculate end row and column for slicing
    end_row = otr + wh
    end_col = otc + ww

    # Check if the calculated coordinates are valid before slicing
    # The analysis suggests the slice should always be within bounds.
    # If an IndexError occurs here, it implies the logic or understanding is wrong.
    if (otr < 0 or otc < 0 or 
        end_row > input_h or end_col > input_w):
        print(f"Warning: Calculated slice [{otr}:{end_row}, {otc}:{end_col}] goes out of input bounds ({input_h}, {input_w}). Returning empty grid.")
        return [[]]

    # Perform the extraction
    output_grid_np = input_np[otr:end_row, otc:end_col]

    # Ensure extracted grid has the expected shape (wh, ww)
    if output_grid_np.shape != (wh, ww):
         print(f"Warning: Extracted subgrid {output_grid_np.shape} differs from expected {(wh, ww)}. Check logic.")
         # Decide how to handle this: return empty, padded, or as is?
         # Based on ARC, exact shape is usually crucial. Return empty for now.
         return [[]]

    return output_grid_np.tolist()