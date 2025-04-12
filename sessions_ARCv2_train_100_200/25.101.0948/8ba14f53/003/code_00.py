import numpy as np
from collections import deque

"""
Natural Language Program Description:
1.  Identify the two main, non-overlapping, non-white objects (A left, B right) and their bounding boxes (`bbox_A`, `bbox_B`). Main objects are assumed to be the two largest distinct color blocks.
2.  Extract the top-left 3x3 subgrids `A_sub` and `B_sub` from their respective bounding boxes. Let the rows be `A0, A1, A2` and `B0, B1, B2`. Pad with 0 if the bounding box is smaller than 3x3.
3.  Extract the first 3 elements of the 4th row (index 3 relative to bbox top) of `bbox_B`, handling boundary conditions (padding with 0 if necessary). Call this `B3_slice`.
4.  Define a function `is_complete(row)` that returns true if the 3-element `row` contains no zeros.
5.  Define a function `modify(row)` that returns a copy of the 3-element `row` with its rightmost non-zero element changed to zero.
6.  Determine if `A2` is complete: `A2_complete = is_complete(A2)`.
7.  Determine if `B2` is complete: `B2_complete = is_complete(B2)`.
8.  Determine Output Row 0 (`Out0`):
    a.  If `A2_complete` is true: `Out0 = modify(A1)`.
    b.  Else (`A2_complete` is false):
        i.  If the last element `A2[2]` is 0: `Out0 = A0`.
        ii. Else (`A2[2]` is not 0): `Out0 = modify(A0)`.
9.  Determine Output Row 1 (`Out1`): Set flag `Out1_from_A1 = false` initially.
    a.  If `A2_complete` is true:
        i.  If `B2_complete` is true: `Out1 = modify(B1)`.
        ii. Else (`B2_complete` is false): `Out1 = B0`.
    b.  Else (`A2_complete` is false):
        i.  If `A2[2]` is 0:
            1.  Check if `A1` has the pattern `[color, 0, 0]` (i.e., `A1[0]!=0`, `A1[1]==0`, `A1[2]==0`). If yes: `Out1 = A1`. Set `Out1_from_A1 = true`.
            2.  Else if `B2_complete` is true: `Out1 = modify(B0)`.
            3.  Else (`B2_complete` is false): `Out1 = B0`.
        ii. Else (`A2[2]` is not 0): `Out1 = B0`.
10. Determine Output Row 2 (`Out2`):
    a. If `Out1_from_A1` is true: `Out2 = modify(B0)`.
    b. Else if `A2_complete` is true:
        i. If `B3_slice` is identical to `B0`: `Out2 = B3_slice`.
        ii. Else: `Out2 = [0, 0, 0]`.
    c. Else (`A2_complete` is false AND `Out1_from_A1` is false): `Out2 = [0, 0, 0]`.
11. Construct the final 3x3 output grid using `Out0`, `Out1`, and `Out2` as its rows.
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
    elif len(main_objects) == 1:
         # If only one object found, cannot proceed as per task structure
         return None, None 
    else: # No objects found
         return None, None

def get_subgrid(grid_np: np.ndarray, bbox: tuple[int, int, int, int]) -> np.ndarray:
    """Extracts the top-left 3x3 subgrid from the object's bounding box."""
    min_r, max_r, min_c, max_c = bbox
    sub = np.zeros((3, 3), dtype=int)
    rows = min(3, max_r - min_r + 1)
    cols = min(3, max_c - min_c + 1)
    sub[:rows, :cols] = grid_np[min_r : min_r + rows, min_c : min_c + cols]
    return sub

def get_row_slice(grid_np: np.ndarray, bbox: tuple[int, int, int, int], row_offset: int, slice_len: int) -> list[int]:
    """Extracts a slice of a specific row relative to the bbox top-left."""
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

    # 1. Identify objects A and B
    bbox_A, bbox_B = find_objects(input_np)
    if bbox_A is None or bbox_B is None:
        return default_output # Cannot proceed if two objects not found

    # 2. Extract subgrids and get rows A0, A1, A2 and B0, B1, B2
    A_sub = get_subgrid(input_np, bbox_A)
    B_sub = get_subgrid(input_np, bbox_B)
    A0, A1, A2 = list(A_sub[0]), list(A_sub[1]), list(A_sub[2])
    B0, B1, B2 = list(B_sub[0]), list(B_sub[1]), list(B_sub[2])

    # 3. Extract B3_slice
    B3_slice = get_row_slice(input_np, bbox_B, 3, 3)

    # 4. is_complete function defined above
    # 5. modify function defined above

    # 6. Check A2 completeness
    A2_complete = is_complete(A2)

    # 7. Check B2 completeness
    B2_complete = is_complete(B2)

    # 8. Determine Output Row 0 (Out0)
    if A2_complete:
        Out0 = modify(A1)
    else: # A2 incomplete
        if A2[2] == 0:
            Out0 = A0
        else: # A2[2] != 0
            Out0 = modify(A0)

    # 9. Determine Output Row 1 (Out1)
    Out1_from_A1 = False
    if A2_complete:
        if B2_complete:
            Out1 = modify(B1)
        else: # B2 incomplete
            Out1 = B0
    else: # A2 incomplete
        if A2[2] == 0:
            # Check A1 pattern [color, 0, 0]
            if A1[0] != 0 and A1[1] == 0 and A1[2] == 0:
                Out1 = A1
                Out1_from_A1 = True
            elif B2_complete:
                Out1 = modify(B0)
            else: # B2 incomplete
                Out1 = B0
        else: # A2[2] != 0
            Out1 = B0

    # 10. Determine Output Row 2 (Out2)
    if Out1_from_A1:
        Out2 = modify(B0)
    elif A2_complete:
        if B3_slice == B0: # Check list equality
             Out2 = B3_slice
        else:
             Out2 = [0, 0, 0]
    else: # A2 incomplete and not Out1_from_A1
        Out2 = [0, 0, 0]

    # 11. Construct the final 3x3 output grid
    output_grid = [Out0, Out1, Out2]
    
    return output_grid