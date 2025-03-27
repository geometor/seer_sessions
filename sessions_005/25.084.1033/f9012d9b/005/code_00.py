"""
1. Identify the contiguous block of white pixels (color 0). Determine its top-left corner coordinates (row `wr`, column `wc`) and its dimensions (height `wh`, width `ww`). The output grid will have the same dimensions (`wh`, `ww`).
2. Find all red pixels (color 2) that are located in the same rows as the white block (i.e., in rows from `wr` to `wr + wh - 1`). Call these "relevant red pixels".
3. Check if any relevant red pixels were found.
4. Case 1: No relevant red pixels exist.
    - The top row `otr` of the output subgrid in the input is `wr + 2`.
    - The left column `otc` of the output subgrid in the input is `wc`.
5. Case 2: One or more relevant red pixels exist.
    - The top row `otr` of the output subgrid in the input is `wr`.
    - Find the relevant red pixel with the minimum column index (`min_rc`).
    - Compare this minimum column index `min_rc` to the white block's starting column `wc`:
        - If `min_rc` is less than `wc` (the leftmost relevant red pixel is to the left of the white block), then the left column `otc` of the output subgrid is `wc - 1`.
        - If `min_rc` is greater than or equal to `wc` (the leftmost relevant red pixel is in the same column or to the right of the white block), then the left column `otc` of the output subgrid is `wc + 2`.
6. Extract the subgrid of size `wh` x `ww` from the input grid, starting at the calculated coordinates (`otr`, `otc`). This subgrid is the final output.
"""

import numpy as np
from typing import List, Tuple, Optional

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

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

    # 3. Determine Extraction Start Coordinates
    if not relevant_red_pixels:
        # 4. Case 1: No relevant red pixels
        otr = wr + 2
        otc = wc
    else:
        # 5. Case 2: Relevant red pixels exist
        otr = wr
        # Find the minimum column index among relevant red pixels
        min_rc = min(c for r, c in relevant_red_pixels)
        
        # Compare min_rc to wc
        if min_rc < wc:
            # Leftmost relevant red is left of white block
            otc = wc - 1 # Adjusted logic based on analysis
        else:
            # Leftmost relevant red is at or right of white block
            otc = wc + 2

    # 6. Extract Output Subgrid
    
    # Clamp coordinates to prevent slicing errors if calculated offset goes out of bounds.
    # This assumes we should extract *within* the input grid bounds.
    final_otr = max(0, otr)
    final_otc = max(0, otc)
    # Calculate end row/col based on original white block dimensions
    end_row = final_otr + wh
    end_col = final_otc + ww

    # Check if the calculated region is completely outside or has zero size before slicing
    if final_otr >= input_h or final_otc >= input_w or final_otr >= end_row or final_otc >= end_col:
        # If the target start position is already outside, or results in zero dimensions, return empty.
        return [[]] 

    # Adjust end boundaries if they exceed input grid dimensions (partial extraction)
    # Although typically ARC tasks expect exact size extraction, this handles edge cases.
    safe_end_row = min(input_h, end_row)
    safe_end_col = min(input_w, end_col)
    
    output_grid_np = input_np[final_otr:safe_end_row, final_otc:safe_end_col]

    # Check if the extracted size matches the expected size (wh, ww).
    # If not (due to clamping/boundary conditions), the behavior might need further clarification.
    # For now, return the potentially smaller grid extracted.
    # if output_grid_np.shape != (wh, ww):
    #     print(f"Warning: Extracted subgrid {output_grid_np.shape} differs from expected {(wh, ww)} due to boundary conditions.")

    return output_grid_np.tolist()