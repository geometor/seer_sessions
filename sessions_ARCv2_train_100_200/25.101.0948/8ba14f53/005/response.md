```python
import numpy as np
from collections import deque

"""
1.  Identify the two largest, non-overlapping, non-white objects (A left, B right) and their bounding boxes (`bbox_A`, `bbox_B`). If fewer than two objects are found, return a default 3x3 grid of zeros.
2.  Extract the top-left 3x3 subgrids `A_sub` and `B_sub`. Let their rows be represented as lists `A0, A1, A2` and `B0, B1, B2`. Pad with 0 if the bounding box is smaller than 3x3 in relevant dimensions.
3.  Extract the first 3 elements of the 4th row (index 3 relative to `bbox_B` top) from the input grid, starting at `bbox_B`'s minimum column. Handle boundary conditions by padding with 0 if necessary. Call this list `B3_slice`.
4.  Define a function `is_complete(row)` that returns true if the 3-element `row` contains no zeros.
5.  Define a function `modify(row)` that returns a copy of the 3-element `row` with its rightmost non-zero element changed to zero.
6.  Determine if `A2` is complete: `A2_complete = is_complete(A2)`.
7.  Determine if `B2` is complete: `B2_complete = is_complete(B2)`.
8.  Determine if `A2` matches the pattern `[color, 0, 0]`: `A2_is_c00 = (A2[0] != 0 and A2[1] == 0 and A2[2] == 0)`.
9.  Determine Output Rows based on `A2_complete`:
    a.  If `A2_complete` is TRUE:
        i.  `Out0 = modify(A1)`.
        ii. If `B2_complete` is TRUE: `Out1 = modify(B1)`.
        iii.Else (`B2_complete` is FALSE): `Out1 = B0`.
        iv. `Out2 = B3_slice`.
    b.  If `A2_complete` is FALSE:
        i.  If `A2[2]` is NOT 0:
            1.  `Out0 = modify(A0)`.
            2.  `Out1 = B0`.
            3.  `Out2 = [0, 0, 0]`.
        ii. If `A2[2]` IS 0:
            1.  `Out0 = A0`.
            2.  If `B2_complete` is TRUE:
                a.  `Out1 = modify(B0)`.
                b.  `Out2 = [0, 0, 0]`.
            3.  If `B2_complete` is FALSE:
                a.  If `A2_is_c00` is TRUE:
                    i.  `Out1 = A1`.
                    ii. `Out2 = modify(B0)`.
                b.  Else (`A2_is_c00` is FALSE):
                    i.  `Out1 = B0`.
                    ii. `Out2 = [0, 0, 0]`.
10. Construct the final 3x3 output grid using `Out0`, `Out1`, and `Out2` as its rows.
"""

def find_objects(grid_np: np.ndarray) -> tuple[tuple[int, int, int, int] | None, tuple[int, int, int, int] | None]:
    """
    Finds the bounding boxes of the two largest non-background (0) objects based on pixel count.
    Assumes objects are contiguous blocks of the same color.
    Returns the bounding boxes sorted left-to-right based on min_col.
    Bounding box format: (min_row, max_row, min_col, max_col)
    """
    h, w = grid_np.shape
    visited = np.zeros((h, w), dtype=bool)
    objects = []
    for r in range(h):
        for c in range(w):
            if grid_np[r, c] != 0 and not visited[r, c]:
                color = grid_np[r, c]
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r, min_c, max_c = r, r, c, c
                
                # BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Check 4 neighbors (N, S, E, W)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < h and 0 <= nc < w and \
                           not visited[nr, nc] and grid_np[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'color': color, 'bbox': (min_r, max_r, min_c, max_c), 'size': len(component_pixels)})

    if not objects:
        return None, None

    # Sort objects by size (descending) to find the two largest
    objects.sort(key=lambda o: o['size'], reverse=True)
    
    main_objects = objects[:2]
    
    # Sort the two main objects by their horizontal position (min_col)
    main_objects.sort(key=lambda o: o['bbox'][2])

    if len(main_objects) == 2:
        return main_objects[0]['bbox'], main_objects[1]['bbox']
    else: 
         # If fewer than two objects found, return None
         return None, None

def get_subgrid(grid_np: np.ndarray, bbox: tuple[int, int, int, int]) -> np.ndarray:
    """Extracts the top-left 3x3 subgrid from the object's bounding box, padding with 0."""
    min_r, max_r, min_c, max_c = bbox
    sub = np.zeros((3, 3), dtype=int)
    # Determine the actual dimensions available in the source grid relative to bbox
    src_h = max_r - min_r + 1
    src_w = max_c - min_c + 1
    # Determine the dimensions to copy (up to 3x3)
    copy_h = min(3, src_h)
    copy_w = min(3, src_w)
    # Copy the relevant part
    sub[:copy_h, :copy_w] = grid_np[min_r : min_r + copy_h, min_c : min_c + copy_w]
    return sub

def get_row_slice(grid_np: np.ndarray, bbox: tuple[int, int, int, int], row_offset: int, slice_len: int) -> list[int]:
    """Extracts a slice of a specific row relative to the bbox top-left, padding with 0."""
    h, w = grid_np.shape
    min_r, _, min_c, _ = bbox
    target_row_idx = min_r + row_offset
    
    row_slice = [0] * slice_len # Initialize with zeros (padding)
    
    if 0 <= target_row_idx < h: # Check if row is within grid bounds
        for c_offset in range(slice_len):
             col_idx = min_c + c_offset
             if 0 <= col_idx < w: # Check if col is within grid bounds
                 row_slice[c_offset] = grid_np[target_row_idx, col_idx]
                 
    return row_slice

def is_complete(row: list[int] | np.ndarray) -> bool:
    """Checks if a 3-element row contains no zeros."""
    return 0 not in row

def modify(row_list: list[int]) -> list[int]:
    """
    Takes a 3-element row (list). Finds the rightmost non-zero element
    and sets it to 0. Returns the potentially modified row as a new list.
    """
    row = row_list[:] # Make a copy
    for i in range(len(row) - 1, -1, -1):
        if row[i] != 0:
            row[i] = 0
            break
    return row

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    input_np = np.array(input_grid, dtype=int)
    default_output = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Step 1: Identify objects A and B
    bbox_A, bbox_B = find_objects(input_np)
    if bbox_A is None or bbox_B is None:
        return default_output # Return default if fewer than two objects found

    # Step 2: Extract subgrids and get rows A0, A1, A2 and B0, B1, B2
    A_sub = get_subgrid(input_np, bbox_A)
    B_sub = get_subgrid(input_np, bbox_B)
    A0, A1, A2 = list(A_sub[0]), list(A_sub[1]), list(A_sub[2])
    B0, B1, B2 = list(B_sub[0]), list(B_sub[1]), list(B_sub[2])

    # Step 3: Extract B3_slice
    B3_slice = get_row_slice(input_np, bbox_B, 3, 3)

    # Step 4 & 5: Helper functions defined above (is_complete, modify)

    # Step 6: Check A2 completeness
    A2_complete = is_complete(A2)

    # Step 7: Check B2 completeness
    B2_complete = is_complete(B2)
    
    # Step 8: Check A2 pattern [color, 0, 0]
    # Note: The description implies A2, but analysis used A1 pattern for Ex1. Let's re-check Ex1 logic.
    # Ex1: A2=[3,0,0] -> A2_is_c00 = True.
    # Re-check analysis for Ex1 Out1: A2[2]=0, B2_inc, A2_is_c00=T -> A1 -> [3,0,0] 
    # Re-check analysis for Ex1 Out2: A2[2]=0, B2_inc, A2_is_c00=T -> mod(B0) -> [1,1,0]
    # It seems the pattern check should indeed be on A2.
    A2_is_c00 = (A2[0] != 0 and A2[1] == 0 and A2[2] == 0)

    # Step 9: Determine Output Rows based on A2_complete
    Out0, Out1, Out2 = [0,0,0], [0,0,0], [0,0,0] # Initialize output rows

    if A2_complete:
        # Case 9.a: A2 is complete
        Out0 = modify(A1)
        if B2_complete:
            Out1 = modify(B1)
        else: # B2 incomplete
            Out1 = B0
        Out2 = B3_slice
    else:
        # Case 9.b: A2 is incomplete
        if A2[2] != 0:
            # Case 9.b.i: A2 incomplete and rightmost element is non-zero
            Out0 = modify(A0)
            Out1 = B0
            Out2 = [0, 0, 0]
        else:
            # Case 9.b.ii: A2 incomplete and rightmost element is zero
            Out0 = A0
            if B2_complete:
                # Case 9.b.ii.2: B2 is complete
                Out1 = modify(B0)
                Out2 = [0, 0, 0]
            else:
                # Case 9.b.ii.3: B2 is incomplete
                if A2_is_c00:
                    # Case 9.b.ii.3.a: A2 matches pattern [c, 0, 0]
                    Out1 = A1
                    Out2 = modify(B0)
                else:
                    # Case 9.b.ii.3.b: A2 does not match pattern [c, 0, 0]
                    Out1 = B0
                    Out2 = [0, 0, 0]

    # Step 10: Construct the final 3x3 output grid
    output_grid = [Out0, Out1, Out2]
    
    return output_grid
```