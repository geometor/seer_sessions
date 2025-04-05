"""
Transforms an input grid based on the properties of connected components (blobs) of non-zero digits.

1. Identifies connected components (blobs) of non-zero digits using 8-directional connectivity.
2. For each blob, determines the unique non-zero digits (colors) it contains.
3. Filters for blobs containing exactly two distinct non-zero colors.
4. For these two-color blobs, identifies the 'outer color' (at least one cell of this color is adjacent to a background '0' cell or the grid edge) and the 'inner color' (no cell of this color is adjacent to '0' or edge). Blobs where both or neither color touch the border/background are ignored.
5. Identifies cells within the blob that contain the 'inner color'.
6. Filters these 'inner color' cells, keeping only those whose 8 neighbors are all within the grid and contain either the 'inner color' or the 'outer color' (i.e., belong to the same blob).
7. Constructs the output grid containing only the surviving 'inner color' cells, with all other cells set to '0'.
"""

import numpy as np
from scipy.ndimage import label

def _touches_border_or_zero(r, c, H, W, input_array):
    """Checks if cell (r, c) has an 8-neighbor that is 0 or is outside the grid."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if neighbor is out of bounds (adjacent to edge)
            if not (0 <= nr < H and 0 <= nc < W):
                return True
            # Check if neighbor is background color 0
            if input_array[nr, nc] == 0:
                return True
    return False

def _is_fully_surrounded_by_blob(r, c, C_inner, C_outer, H, W, input_array):
    """Checks if cell (r, c) with C_inner is fully surrounded by C_inner or C_outer colors."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if neighbor is out of bounds - if so, not fully surrounded
            if not (0 <= nr < H and 0 <= nc < W):
                return False 
            
            neighbor_val = input_array[nr, nc]
            # Check if neighbor color is valid (must be C_inner or C_outer)
            if neighbor_val != C_inner and neighbor_val != C_outer:
                return False
    # If all neighbors were checked and were valid (in bounds and C_inner/C_outer)
    return True

def transform(input_grid):
    # Convert input to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    H, W = input_array.shape
    
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_array)

    # Define the connectivity structure for 8 directions (Moore neighborhood)
    structure = np.ones((3, 3), dtype=bool)

    # Find connected components (blobs) of non-zero cells
    # labeled_array assigns a unique integer ID to each blob
    # num_features is the total count of blobs found (including background if not excluded)
    labeled_array, num_features = label(input_array > 0, structure=structure)

    # Iterate through each found blob (labels are 1-based)
    for blob_idx in range(1, num_features + 1):
        # Create a boolean mask for the cells belonging to the current blob
        blob_mask = (labeled_array == blob_idx)
        
        # Get the coordinates of the cells in the current blob
        blob_coords = np.argwhere(blob_mask)
        
        # Get the values (colors) of the cells in the current blob
        blob_values = input_array[blob_mask]
        
        # Find the unique non-zero colors present within the blob
        unique_colors = np.unique(blob_values[blob_values > 0])

        # --- Filter for blobs containing exactly two distinct non-zero colors ---
        if len(unique_colors) != 2:
            continue # Skip blobs that don't meet this criterion

        c1, c2 = unique_colors
        c1_touches_border = False
        c2_touches_border = False

        # --- Determine if c1 or c2 touches border/zero anywhere in the blob ---
        for r, c in blob_coords:
            val = input_array[r, c]
            # Check if this specific cell touches border/zero
            if _touches_border_or_zero(r, c, H, W, input_array):
                if val == c1:
                    c1_touches_border = True
                elif val == c2:
                    c2_touches_border = True
            
            # Optimization: If we've found both touch, no need to check further cells in this blob
            if c1_touches_border and c2_touches_border:
                break
        
        # --- Determine Outer and Inner colors ---
        # The rule requires exactly one color touching the border/zero
        if c1_touches_border == c2_touches_border: 
            # If both touch OR neither touches, ignore this blob
            continue 

        # Assign Outer and Inner based on the border-touching check
        C_outer = c1 if c1_touches_border else c2
        C_inner = c2 if c1_touches_border else c1

        # --- Filter Inner Color Cells based on Full Surrounding ---
        # Iterate through the blob cells again
        for r, c in blob_coords:
            # Focus only on cells that have the Inner color
            if input_array[r, c] == C_inner:
                # Check if this inner cell is fully surrounded by blob colors (Inner or Outer)
                if _is_fully_surrounded_by_blob(r, c, C_inner, C_outer, H, W, input_array):
                    # If it is, place its color in the corresponding output grid cell
                    output_grid[r, c] = C_inner

    return output_grid.tolist() # Return as list of lists as per standard format