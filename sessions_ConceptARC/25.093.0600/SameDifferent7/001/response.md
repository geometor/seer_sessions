```python
"""
Transforms an input grid based on the properties of connected components (blobs) of non-zero digits.

1. Identifies connected components (blobs) of non-zero digits using 8-directional connectivity.
2. For each blob, determines the unique non-zero digits (colors) it contains.
3. Filters for blobs containing exactly two distinct non-zero colors.
4. For these two-color blobs, identifies the 'outer color' (adjacent to background '0' cells) and the 'inner color'.
5. Identifies cells within the blob that contain the 'inner color'.
6. Filters these 'inner color' cells, keeping only those whose 8 neighbors are all within the grid and contain either the 'inner color' or the 'outer color'.
7. Constructs the output grid containing only the surviving 'inner color' cells, with all other cells set to '0'.
"""

import numpy as np
from scipy.ndimage import label

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    H, W = input_array.shape
    
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_array)

    # Define the connectivity structure for 8 directions (Moore neighborhood)
    structure = np.ones((3, 3), dtype=bool)

    # Find connected components (blobs) of non-zero cells
    # labeled_array contains the blob ID for each cell, num_features is the count of blobs
    labeled_array, num_features = label(input_array > 0, structure=structure)

    # Iterate through each found blob (labels are 1-based)
    for i in range(1, num_features + 1):
        # Create a mask for the current blob
        blob_mask = (labeled_array == i)
        
        # Get the coordinates of the cells in the current blob
        blob_coords = np.argwhere(blob_mask)
        
        # Get the values (colors) of the cells in the current blob
        blob_values = input_array[blob_mask]
        
        # Find the unique non-zero colors in the blob
        unique_colors = np.unique(blob_values[blob_values > 0])

        # --- Filter for blobs with exactly two colors ---
        if len(unique_colors) != 2:
            continue # Ignore blobs that don't have exactly two colors

        color1, color2 = unique_colors

        # --- Identify Inner and Outer Colors ---
        c1_adj_0 = False
        c2_adj_0 = False
        
        # Check adjacency to background (0) or grid edge for each color
        for r, c in blob_coords:
            val = input_array[r, c]
            # Check 8 neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r + dr, c + dc
                    
                    # If neighbor is out of bounds, it's considered adjacent to 'outside' (like 0)
                    if not (0 <= nr < H and 0 <= nc < W):
                        if val == color1: c1_adj_0 = True
                        if val == color2: c2_adj_0 = True
                    # If neighbor is inside bounds and is 0
                    elif input_array[nr, nc] == 0:
                         if val == color1: c1_adj_0 = True
                         if val == color2: c2_adj_0 = True
                            
            # Optimization: if both found adjacent to 0, no need to check further for this blob
            if c1_adj_0 and c2_adj_0:
                break 

        # Determine outer and inner based on adjacency to 0
        # If both or neither touch 0, the blob structure might be ambiguous 
        # according to the implied rule, so skip it.
        if c1_adj_0 == c2_adj_0: 
            continue 

        C_outer = color1 if c1_adj_0 else color2
        C_inner = color2 if c1_adj_0 else color1

        # --- Filter Inner Color Cells based on Neighborhood ---
        # Iterate through the cells of the current blob again
        for r, c in blob_coords:
            # Consider only cells with the inner color
            if input_array[r, c] == C_inner:
                is_fully_surrounded_by_blob = True
                # Check all 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc

                        # Check if neighbor is within grid bounds
                        if not (0 <= nr < H and 0 <= nc < W):
                            is_fully_surrounded_by_blob = False
                            break # Neighbor is outside grid

                        # Check if neighbor belongs to the same blob (has C_inner or C_outer color)
                        neighbor_val = input_array[nr, nc]
                        if neighbor_val != C_inner and neighbor_val != C_outer:
                            is_fully_surrounded_by_blob = False
                            break # Neighbor is not part of the blob colors
                
                # If all neighbors passed the checks, keep this inner cell in the output
                if is_fully_surrounded_by_blob:
                    output_grid[r, c] = C_inner

    return output_grid

```