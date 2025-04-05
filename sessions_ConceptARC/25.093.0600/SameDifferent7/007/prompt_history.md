
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 6 6 6 6 0 0
0 0 4 3 4 0 6 8 6 6 6 6
0 0 3 3 3 0 8 8 8 6 6 6
0 0 4 3 4 0 6 8 6 6 0 0
0 0 4 4 4 0 6 6 6 6 0 0
0 3 3 3 3 0 0 7 7 7 7 7
0 3 2 2 3 0 0 7 4 4 7 7
0 3 2 2 3 0 0 7 4 7 7 7
0 3 3 3 3 0 0 7 4 4 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 3 3 3 0 8 8 8 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 9 9 9 9 9
0 0 0 0 0 0 0 9 4 4 4 9
0 1 1 1 1 0 0 9 4 4 9 9
0 1 6 6 1 0 0 9 4 9 9 9
0 1 6 1 1 1 0 9 4 4 4 9
0 1 6 6 1 1 0 9 9 9 9 9
0 1 1 1 1 0 0 0 3 3 3 3
0 0 0 0 7 7 7 0 3 1 1 3
0 0 0 7 7 3 3 0 3 1 3 3
0 0 0 7 7 3 7 0 3 1 1 3
0 0 0 7 7 3 3 0 3 1 3 3
0 0 0 0 7 7 7 0 3 1 1 3
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0
0 0 5 5 5 5 6 6 6 6 0 0
5 5 5 4 4 5 6 3 3 6 0 0
5 5 5 4 4 5 6 3 3 6 0 0
5 5 5 4 4 5 6 6 6 6 0 0
5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 7 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:** The task involves transforming a 2D grid of digits (0-9) into another grid of the same dimensions. The input grids contain distinct regions or "blobs" formed by connected non-zero digits. The output grids are much sparser, retaining only specific digits from certain input blobs. The digit '0' acts as a background color.
*   **Analysis:** The transformation focuses on blobs composed of exactly two distinct non-zero digits. Within such blobs, one digit seems to form an outer layer or border ('outer color'), while the other forms an inner core ('inner color'). The transformation rule isolates and retains only those cells of the 'inner color' that are completely surrounded by other cells belonging to the *same* blob (i.e., cells with either the inner or outer color). Blobs with only one non-zero color or more than two non-zero colors are completely removed (replaced by 0s) in the output. The 'outer color' is typically the one that has cells adjacent to the '0' background, while the 'inner color' does not (or does so to a lesser extent).

*   **YAML Facts:**
    
```yaml
    task_elements:
      - type: Grid
        properties: [2D, Integer Digits (0-9)]
      - type: Background
        properties: [Digit 0]
      - type: Object
        name: Blob
        properties: [Connected Component of Non-Zero Digits, Moore Connectivity (8 directions)]
      - type: Blob Property
        name: Colors
        properties: [Set of unique non-zero digits within the blob]
      - type: Blob Property
        name: Color Count
        properties: [Number of unique non-zero digits]
      - type: Special Blob
        name: Two-Color Blob
        criteria: [Color Count == 2]
        properties:
          - Outer Color: [The color within the blob that has adjacency to the Background (0)]
          - Inner Color: [The color within the blob that is not the Outer Color]
      - type: Cell
        properties: [Row, Column, Digit Value]
      - type: Cell Property
        name: Neighborhood
        properties: [8 adjacent cells (Moore Neighborhood)]
      - type: Cell Condition
        name: Fully Surrounded within Blob
        criteria: [Applies to Inner Color cells in a Two-Color Blob, All 8 neighbors must have either Inner Color or Outer Color]
    actions:
      - Identify Blobs in Input Grid
      - Analyze Colors within each Blob
      - Filter for Two-Color Blobs
      - Identify Inner and Outer Colors for Two-Color Blobs
      - Filter Inner Color cells based on the "Fully Surrounded within Blob" condition
      - Construct Output Grid: Initialize with 0s, place surviving Inner Color cells
    relationships:
      - Blobs are composed of Cells.
      - Cells have Neighbors.
      - Output Grid is derived from Input Grid based on Blob properties and Cell conditions.
      - Only Inner Color cells from Two-Color Blobs that are fully surrounded within their blob appear in the Output Grid.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled with zeros.
    2.  Identify all distinct connected components (blobs) of non-zero cells in the input grid, using 8-directional (Moore) connectivity.
    3.  For each identified blob:
        a.  Determine the set of unique non-zero digits (colors) present within the blob.
        b.  Count the number of unique colors.
        c.  If the count is exactly two, proceed to the next step. Otherwise, ignore this blob (it contributes only zeros to the output).
        d.  Designate the two colors as `color1` and `color2`. Identify which color has at least one cell adjacent (horizontally, vertically, or diagonally) to a background cell (0). Label this color as `C_outer` (outer color) and the other color as `C_inner` (inner color).
        e.  Iterate through all cells `(r, c)` within this blob that contain the `C_inner` color.
        f.  For each such cell `(r, c)`, examine its 8 neighboring cells.
        g.  Check if all 8 neighbors are within the grid boundaries AND contain either the `C_inner` or `C_outer` color.
        h.  If this condition is met (the `C_inner` cell is fully surrounded by cells of the same blob), set the corresponding cell `(r, c)` in the output grid to `C_inner`.
    4.  Return the completed output grid.
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
```python
"""
Transforms an input grid based on the properties of connected components (blobs) of non-zero digits.

1. Identifies connected components (blobs) of non-zero digits using 8-directional connectivity.
2. For each blob, determines the unique non-zero digits (colors) it contains.
3. Filters for blobs containing exactly two distinct non-zero colors.
4. For these two-color blobs, identifies the 'outer color' (adjacent to background '0' cells) and the 'inner color'. A blob is ignored if both or neither of its colors are adjacent to the background.
5. Identifies cells within the blob that contain the 'inner color'.
6. Filters these 'inner color' cells, keeping only those whose 8 neighbors are all within the grid and contain either the 'inner color' or the 'outer color' (i.e., belong to the same blob).
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

        # --- Identify Inner and Outer Colors based on adjacency to background (0) ---
        c1_adj_0 = False
        c2_adj_0 = False
        
        # Check adjacency to background (0) or grid edge for each color
        for r, c in blob_coords:
            val = input_array[r, c]
            is_c1 = (val == color1)
            is_c2 = (val == color2)
            
            # If we already found both adjacent, no need to check more coords for this blob
            if c1_adj_0 and c2_adj_0:
                break

            # Check 8 neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r + dr, c + dc
                    
                    neighbor_is_0_or_edge = False
                    # If neighbor is out of bounds, it's adjacent to 'outside' (like 0)
                    if not (0 <= nr < H and 0 <= nc < W):
                         neighbor_is_0_or_edge = True
                    # If neighbor is inside bounds and is 0
                    elif input_array[nr, nc] == 0:
                         neighbor_is_0_or_edge = True

                    if neighbor_is_0_or_edge:
                         if is_c1: c1_adj_0 = True
                         if is_c2: c2_adj_0 = True
                         # Optimization: if both found adjacent to 0 while checking neighbors of a single cell, break neighbor loop
                         if c1_adj_0 and c2_adj_0:
                             break 
            # Optimization: if both found adjacent to 0, break coordinate loop
            if c1_adj_0 and c2_adj_0:
                break 


        # Determine outer and inner based on adjacency to 0
        # If both or neither touch 0, the blob structure is ambiguous or doesn't fit the rule
        # So, discard the blob (skip to next blob).
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
                            break # Neighbor is outside grid, so not surrounded

                        # Check if neighbor belongs to the same blob (has C_inner or C_outer color)
                        # Use labeled_array for robust check of blob membership
                        if labeled_array[nr, nc] != i: 
                            # We only need to check the value if the neighbor is not part of the *current* blob
                            # If it's part of the current blob (labeled_array[nr, nc] == i), it must have C_inner or C_outer by definition.
                            # However, checking the value directly is also fine and potentially clearer.
                            neighbor_val = input_array[nr, nc]
                            if neighbor_val != C_inner and neighbor_val != C_outer:
                                # Actually, the check should be if the neighbour belongs to the same blob *label*
                                # Because a neighbour might be 0, which is neither C_inner nor C_outer
                                is_fully_surrounded_by_blob = False
                                break # Neighbor is not part of the blob colors


                # If all neighbors passed the checks, keep this inner cell in the output
                if is_fully_surrounded_by_blob:
                    output_grid[r, c] = C_inner

    return output_grid
```
```python
"""
Transforms an input grid based on identifying local color interfaces and checking neighborhood conditions.

1.  Identifies "interface pairs" (Inner Color, Outer Color) by examining adjacent cells with different non-zero colors.
2.  An interface pair is valid only if exactly one of the two colors is locally adjacent (within its own 8 neighbors) to a background cell (0) or the grid edge. The color adjacent to 0/edge is the Outer Color, the other is the Inner Color.
3.  A map stores all potential Outer Colors associated with each Inner Color found.
4.  Iterates through the grid again. For each cell containing a potential Inner Color:
5.  Checks against each associated Outer Color if the cell is "fully surrounded".
6.  "Fully surrounded" means all 8 neighbors are within the grid bounds and have a color equal to either the specific Inner Color or the specific Outer Color being checked.
7.  If a cell is found to be fully surrounded by any of its valid (Inner, Outer) pairs, its Inner Color is placed in the output grid.
"""

import numpy as np
from collections import defaultdict

def is_adjacent_to_zero(r, c, H, W, input_array):
    """Checks if cell (r, c) has a neighbor that is 0 or is on the grid edge."""
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

def is_fully_surrounded(r, c, C_inner, C_outer, H, W, input_array):
    """Checks if cell (r, c) is fully surrounded by C_inner or C_outer colors."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if neighbor is out of bounds
            if not (0 <= nr < H and 0 <= nc < W):
                return False # Cannot be fully surrounded if a neighbor is outside
            
            neighbor_val = input_array[nr, nc]
            # Check if neighbor color is valid (must be C_inner or C_outer)
            if neighbor_val != C_inner and neighbor_val != C_outer:
                return False
    return True

def transform(input_grid):
    """
    Applies the described interface-based transformation rule.
    
    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    H, W = input_array.shape
    
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_array)

    # Map to store potential outer colors for each inner color
    # Key: inner_color, Value: set of potential outer_colors
    inner_to_outer_map = defaultdict(set)

    # --- First Pass: Identify potential (Inner, Outer) pairs from interfaces ---
    for r in range(H):
        for c in range(W):
            v1 = input_array[r, c]
            if v1 == 0:
                continue # Skip background cells

            # Check adjacency of v1 to zero/edge once per cell v1
            v1_adj_0 = is_adjacent_to_zero(r, c, H, W, input_array)

            # Check neighbors of v1
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc

                    # Ensure neighbor is within bounds
                    if not (0 <= nr < H and 0 <= nc < W):
                        continue
                        
                    v2 = input_array[nr, nc]
                    # Consider only adjacent pairs of different non-zero colors
                    if v2 == 0 or v1 == v2:
                        continue

                    # Check adjacency of v2 to zero/edge
                    # Note: This check is somewhat redundant as we iterate through all cells,
                    # but doing it here clarifies the local interface condition.
                    v2_adj_0 = is_adjacent_to_zero(nr, nc, H, W, input_array)

                    # Determine if this pair forms a valid interface
                    if v1_adj_0 and not v2_adj_0:
                        # v1 is outer, v2 is inner
                        inner_to_outer_map[v2].add(v1)
                    elif v2_adj_0 and not v1_adj_0:
                        # v2 is outer, v1 is inner
                        inner_to_outer_map[v1].add(v2)
                    # If both or neither are adjacent to zero, it's not a valid interface pair for this rule

    # --- Second Pass: Filter cells based on the surrounding condition ---
    for r in range(H):
        for c in range(W):
            C_inner = input_array[r, c]
            
            # Skip background or cells never identified as potential inner colors
            if C_inner == 0 or C_inner not in inner_to_outer_map:
                continue

            possible_outers = inner_to_outer_map[C_inner]
            
            # Check against each potential outer color if the cell is surrounded
            for C_outer in possible_outers:
                if is_fully_surrounded(r, c, C_inner, C_outer, H, W, input_array):
                    # If surrounded by this pair, keep the inner color and stop checking other pairs
                    output_grid[r, c] = C_inner
                    break 

    return output_grid
```

Previous Code:
```python
"""
Transforms an input grid based on identifying local color interfaces and checking neighborhood conditions.

1.  Identifies "interface pairs" (Inner Color, Outer Color) by examining adjacent cells with different non-zero colors.
2.  An interface pair is valid only if exactly one of the two colors is locally adjacent (within its own 8 neighbors) to a background cell (0) or the grid edge. The color adjacent to 0/edge is the Outer Color, the other is the Inner Color.
3.  A map stores all potential Outer Colors associated with each Inner Color found.
4.  Iterates through the grid again. For each cell containing a potential Inner Color:
5.  Checks against each associated Outer Color if the cell is "fully surrounded".
6.  "Fully surrounded" means all 8 neighbors are within the grid bounds and have a color equal to either the specific Inner Color or the specific Outer Color being checked.
7.  If a cell is found to be fully surrounded by any of its valid (Inner, Outer) pairs, its Inner Color is placed in the output grid.
"""

import numpy as np
from collections import defaultdict

def is_adjacent_to_zero(r, c, H, W, input_array):
    """Checks if cell (r, c) has a neighbor that is 0 or is on the grid edge."""
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

def is_fully_surrounded(r, c, C_inner, C_outer, H, W, input_array):
    """Checks if cell (r, c) is fully surrounded by C_inner or C_outer colors."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if neighbor is out of bounds
            if not (0 <= nr < H and 0 <= nc < W):
                return False # Cannot be fully surrounded if a neighbor is outside
            
            neighbor_val = input_array[nr, nc]
            # Check if neighbor color is valid (must be C_inner or C_outer)
            if neighbor_val != C_inner and neighbor_val != C_outer:
                return False
    return True

def transform(input_grid):
    """
    Applies the described interface-based transformation rule.
    
    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    H, W = input_array.shape
    
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_array)

    # Map to store potential outer colors for each inner color
    # Key: inner_color, Value: set of potential outer_colors
    inner_to_outer_map = defaultdict(set)

    # --- First Pass: Identify potential (Inner, Outer) pairs from interfaces ---
    for r in range(H):
        for c in range(W):
            v1 = input_array[r, c]
            if v1 == 0:
                continue # Skip background cells

            # Check adjacency of v1 to zero/edge once per cell v1
            v1_adj_0 = is_adjacent_to_zero(r, c, H, W, input_array)

            # Check neighbors of v1
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc

                    # Ensure neighbor is within bounds
                    if not (0 <= nr < H and 0 <= nc < W):
                        continue
                        
                    v2 = input_array[nr, nc]
                    # Consider only adjacent pairs of different non-zero colors
                    if v2 == 0 or v1 == v2:
                        continue

                    # Check adjacency of v2 to zero/edge
                    # Note: This check is somewhat redundant as we iterate through all cells,
                    # but doing it here clarifies the local interface condition.
                    v2_adj_0 = is_adjacent_to_zero(nr, nc, H, W, input_array)

                    # Determine if this pair forms a valid interface
                    if v1_adj_0 and not v2_adj_0:
                        # v1 is outer, v2 is inner
                        inner_to_outer_map[v2].add(v1)
                    elif v2_adj_0 and not v1_adj_0:
                        # v2 is outer, v1 is inner
                        inner_to_outer_map[v1].add(v2)
                    # If both or neither are adjacent to zero, it's not a valid interface pair for this rule

    # --- Second Pass: Filter cells based on the surrounding condition ---
    for r in range(H):
        for c in range(W):
            C_inner = input_array[r, c]
            
            # Skip background or cells never identified as potential inner colors
            if C_inner == 0 or C_inner not in inner_to_outer_map:
                continue

            possible_outers = inner_to_outer_map[C_inner]
            
            # Check against each potential outer color if the cell is surrounded
            for C_outer in possible_outers:
                if is_fully_surrounded(r, c, C_inner, C_outer, H, W, input_array):
                    # If surrounded by this pair, keep the inner color and stop checking other pairs
                    output_grid[r, c] = C_inner
                    break 

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 6 6 6 6 0 0
0 0 4 3 4 0 6 8 6 6 6 6
0 0 3 3 3 0 8 8 8 6 6 6
0 0 4 3 4 0 6 8 6 6 0 0
0 0 4 4 4 0 6 6 6 6 0 0
0 3 3 3 3 0 0 7 7 7 7 7
0 3 2 2 3 0 0 7 4 4 7 7
0 3 2 2 3 0 0 7 4 7 7 7
0 3 3 3 3 0 0 7 4 4 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 3 3 3 0 8 8 8 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 0 3 0 0 0 8 8 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 4 4 0 0
0 0 2 2 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 36.11111111111114

## Example 2:
Input:
```
0 0 0 0 0 0 0 9 9 9 9 9
0 0 0 0 0 0 0 9 4 4 4 9
0 1 1 1 1 0 0 9 4 4 9 9
0 1 6 6 1 0 0 9 4 9 9 9
0 1 6 1 1 1 0 9 4 4 4 9
0 1 6 6 1 1 0 9 9 9 9 9
0 1 1 1 1 0 0 0 3 3 3 3
0 0 0 0 7 7 7 0 3 1 1 3
0 0 0 7 7 3 3 0 3 1 3 3
0 0 0 7 7 3 7 0 3 1 1 3
0 0 0 7 7 3 3 0 3 1 3 3
0 0 0 0 7 7 7 0 3 1 1 3
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 4 4 0 0
0 0 6 6 0 0 0 0 4 0 0 0
0 0 6 0 0 0 0 0 4 4 4 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 3 0 0 0 1 3 0
0 0 0 0 0 3 0 0 0 1 1 0
0 0 0 0 0 3 0 0 0 1 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 19
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 52.77777777777777

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0
0 0 5 5 5 5 6 6 6 6 0 0
5 5 5 4 4 5 6 3 3 6 0 0
5 5 5 4 4 5 6 3 3 6 0 0
5 5 5 4 4 5 6 6 6 6 0 0
5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 7 7 7 7
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 3 3 0 0 0
0 5 0 4 4 0 0 3 3 0 0 0
0 5 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 16.66666666666663

Test Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 4 4 4 0 0 0 0
0 1 3 3 1 0 0 0 4 6 4 0 0 0 0
0 1 3 3 1 0 0 0 4 6 4 0 0 0 0
0 1 1 1 1 0 0 0 4 6 4 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 1 1 3 3 0 0 0
0 0 0 0 0 0 3 3 1 1 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 4 3 4 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 6 0 0 0 0 0
0 0 3 3 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 37.33333333333337

## Example 2:
Input:
```
4 4 4 4 4 4 4 3 3 3 3 3
0 0 4 1 1 1 4 3 2 2 2 3
0 0 4 1 4 4 0 3 3 3 2 3
0 0 4 1 4 0 0 3 3 3 2 3
0 0 4 1 4 0 0 3 3 3 3 3
0 0 4 4 4 0 0 0 0 0 0 0
8 8 8 8 1 1 1 1 1 0 0 0
6 6 6 8 1 7 7 7 1 0 0 0
6 8 6 8 1 7 1 1 1 0 0 0
6 8 8 0 1 7 1 1 0 0 0 0
8 8 0 0 1 7 1 1 0 0 0 0
0 0 0 0 1 1 1 1 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 2 2 2 0
0 0 0 1 0 0 0 0 0 0 2 0
0 0 0 1 0 0 0 0 0 0 2 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 7 7 7 0 0 0 0
0 8 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 25.0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 6 6 6 0
0 6 6 6 6 6 6 6 0 0 6 4 6 0
0 6 4 4 4 4 4 6 0 0 6 4 6 0
0 0 6 4 4 4 6 0 0 0 6 4 6 0
0 0 0 6 4 6 0 0 0 0 6 6 6 0
0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 4 3 3 0 0 0 5 5 5 5 5 5
3 3 4 3 3 0 0 0 5 7 7 7 7 7
3 3 4 3 3 0 0 0 5 5 7 7 7 5
3 3 4 3 3 0 0 0 5 5 5 7 5 5
3 3 4 3 3 0 0 0 5 5 5 5 5 5
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 4 4 4 0 0 0 0 0 4 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 4 3 0 0 0 0 0 7 7 7 7 0
0 3 4 3 0 0 0 0 0 0 7 7 7 0
0 3 4 3 0 0 0 0 0 0 0 7 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 19
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 38.77551020408163
## General Assessment and Strategy

The previous attempt (`code_00.py`) used a local interface-based approach to identify inner/outer colors, which proved incorrect. It failed to capture the global property of a blob (whether *any* part of one color touches the background determines its "outer" status for the *entire* blob). The errors consistently show colors being kept incorrectly, either because they were misidentified as inner colors or because the "fully surrounded" check was flawed or applied to the wrong pairs.

The strategy is to revert to the initial blob-based analysis, but with a more precise implementation:

1.  **Identify Blobs:** Use `scipy.ndimage.label` with 8-connectivity on non-zero cells.
2.  **Filter Blobs:** Keep only blobs with exactly two distinct non-zero colors.
3.  **Determine Global Inner/Outer:** For each two-color blob, check if *any* cell of `color1` is adjacent (8-way) to 0 or the grid edge. Do the same for `color2`. If exactly one color type has such adjacency, it's the `C_outer`, and the other is `C_inner`. If both or neither have adjacency, the blob is ignored.
4.  **Filter Inner Cells:** Iterate through cells with `C_inner` in the valid blobs. Keep only those where all 8 neighbors are within the grid bounds AND have a color of either `C_inner` or `C_outer`.
5.  **Construct Output:** Create the output grid containing only the filtered `C_inner` cells.

## Metrics and Analysis

Let's re-analyze `train_1` using the refined strategy to gather metrics.

**Train 1 Input:**

```
[[0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,4,4,4,0,6,6,6,6,0,0],
 [0,0,4,3,4,0,6,8,6,6,6,6],
 [0,0,3,3,3,0,8,8,8,6,6,6],
 [0,0,4,3,4,0,6,8,6,6,0,0],
 [0,0,4,4,4,0,6,6,6,6,0,0],
 [0,3,3,3,3,0,0,7,7,7,7,7],
 [0,3,2,2,3,0,0,7,4,4,7,7],
 [0,3,2,2,3,0,0,7,4,7,7,7],
 [0,3,3,3,3,0,0,7,4,4,7,0],
 [0,0,0,0,0,0,0,7,7,7,7,0],
 [0,0,0,0,0,0,0,0,0,0,0,0]]
```

**Train 1 Expected Output:**

```
[[0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,3,0,0,0,8,0,0,0,0],
 [0,0,3,3,3,0,8,8,8,0,0,0],
 [0,0,0,3,0,0,0,8,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0]]
```



