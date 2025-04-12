import numpy as np
from collections import deque

"""
Identifies connected components (objects) of digits other than 8 (background) in the input grid.
Calculates the bounding box for each object and extracts the corresponding subgrid from the original input grid.
Determines the maximum width among all extracted object subgrids.
Sorts the subgrids based on the top-left coordinate of their original bounding box (top-to-bottom, then left-to-right).
Pads each subgrid symmetrically with the background color (8) to match the maximum width.
Stacks the padded subgrids vertically in their sorted order to create the output grid.

Note: This logic is derived primarily from examples train_2, train_3, and train_4. 
Example train_1 appears to follow a different padding or width determination rule 
and may not be handled correctly by this implementation, as its output width (6) 
does not match the maximum width of its input objects (2).
"""

# Helper function to find connected components (objects) of non-background pixels using BFS
def _find_objects(grid_np: np.ndarray, background_color: int) -> list[dict]:
    """
    Finds all connected components of non-background pixels.

    Args:
        grid_np: The input grid as a numpy array.
        background_color: The integer value representing the background.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its 'bounds' (min_r, max_r, min_c, max_c) and
        'top_left' coordinate (min_r, min_c) for sorting.
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find a non-background cell that hasn't been visited
            if grid_np[r, c] != background_color and not visited[r, c]:
                component_pixels = [] # Store coordinates (r, c) of pixels in this component
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))

                    # Explore neighbors (4-way connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is part of the object and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid_np[nr, nc] != background_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if component_pixels:
                    # Calculate bounding box after finding all pixels for the component
                    obj_min_r = min(px[0] for px in component_pixels)
                    obj_max_r = max(px[0] for px in component_pixels)
                    obj_min_c = min(px[1] for px in component_pixels)
                    obj_max_c = max(px[1] for px in component_pixels)
                    
                    objects.append({
                        'bounds': (obj_min_r, obj_max_r, obj_min_c, obj_max_c),
                        'top_left': (obj_min_r, obj_min_c) # Use top-left for sorting
                    })

    # Sort objects based on their top-left corner (top-to-bottom, then left-to-right)
    objects.sort(key=lambda obj: obj['top_left'])
    return objects

# Helper function to extract the subgrid based on bounding box
def _extract_subgrid(grid_np: np.ndarray, bounds: tuple) -> np.ndarray:
    """
    Extracts the rectangular subgrid defined by the bounds from the grid.
    """
    min_r, max_r, min_c, max_c = bounds
    # Slice the numpy array to get the subgrid
    return grid_np[min_r:max_r+1, min_c:max_c+1]

# Helper function to pad a subgrid symmetrically to a target width
def _pad_subgrid(subgrid_np: np.ndarray, target_width: int, background_color: int) -> np.ndarray:
    """
    Pads a subgrid with the background color to reach the target width.
    Padding is applied symmetrically (left and right).
    """
    if subgrid_np is None or subgrid_np.size == 0:
        # Return an empty array or handle as error if needed
        return np.array([[]], dtype=int) 
        
    current_height, current_width = subgrid_np.shape

    if current_width == target_width:
        return subgrid_np # No padding needed
    elif current_width > target_width:
         # This case should not happen if target_width is the max width found
         # Return original subgrid if it does
         return subgrid_np

    # Calculate padding amounts
    padding_needed = target_width - current_width
    left_padding = padding_needed // 2
    right_padding = padding_needed - left_padding

    # Create padding arrays filled with the background color
    left_pad_arr = np.full((current_height, left_padding), background_color, dtype=subgrid_np.dtype)
    right_pad_arr = np.full((current_height, right_padding), background_color, dtype=subgrid_np.dtype)

    # Concatenate horizontally: left_padding + subgrid + right_padding
    padded_subgrid = np.concatenate((left_pad_arr, subgrid_np, right_pad_arr), axis=1)
    return padded_subgrid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by extracting non-background objects, padding them
    to a uniform width (based on the widest object), and stacking them vertically.
    """
    
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    background_color = 8

    # --- Step 1: Find all non-background objects and their bounding boxes ---
    # Objects are returned sorted by their top-left position.
    objects = _find_objects(input_np, background_color)

    # Handle case where no objects are found
    if not objects:
        return [] 

    # --- Step 2: Extract the subgrid for each object ---
    extracted_subgrids = []
    for obj in objects:
        subgrid = _extract_subgrid(input_np, obj['bounds'])
        extracted_subgrids.append(subgrid)

    # --- Step 3: Determine the target width (max width among all extracted subgrids) ---
    if not extracted_subgrids:
         return [] # Should be caught by object check, but defensive programming
    
    max_width = 0
    for subgrid in extracted_subgrids:
        # Check if subgrid is valid and has 2 dimensions before accessing shape[1]
        if subgrid is not None and subgrid.ndim == 2 and subgrid.shape[1] > 0:
             max_width = max(max_width, subgrid.shape[1])
        # Consider 1D arrays or single elements if they could occur (width 1)
        elif subgrid is not None and subgrid.size > 0:
             max_width = max(max_width, 1) # Width is 1 for a 1D array or single element

    # If max_width remains 0 (e.g., all objects were empty?), return empty
    if max_width == 0:
        return []

    # --- Step 4: Pad each extracted subgrid to the determined maximum width ---
    # The order of subgrids matches the sorted order of objects found earlier.
    padded_subgrids = []
    for subgrid in extracted_subgrids:
         # Ensure subgrid is valid before padding
         if subgrid is not None and subgrid.size > 0:
            padded = _pad_subgrid(subgrid, max_width, background_color)
            padded_subgrids.append(padded)

    # --- Step 5: Concatenate padded subgrids vertically to form the output grid ---
    if not padded_subgrids:
        return [] # No valid subgrids to stack

    # Use numpy's vstack for vertical concatenation
    output_np = np.vstack(padded_subgrids)

    # --- Step 6: Convert the final numpy array back to a list of lists ---
    output_grid = output_np.tolist()

    return output_grid