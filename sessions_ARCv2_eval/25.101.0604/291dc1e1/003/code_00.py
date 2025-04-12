import numpy as np
from collections import deque

"""
Transforms the input grid by:
1. Identifying the core area containing non-background pixels (digits other than 8).
2. Finding all connected non-background objects within this core area using 4-way connectivity.
3. Extracting the bounding box subgrid for each object from the core grid.
4. Determining the maximum width among all extracted object subgrids.
5. Sorting the extracted subgrids based on their original top-left position within the core grid (top-to-bottom, then left-to-right).
6. Padding each subgrid symmetrically with the background color (8) to match the calculated maximum width.
7. Stacking the padded subgrids vertically in their sorted order to create the output grid.

Note: This implementation is based on the pattern observed in examples train_2, 
train_3, and train_4, where the output width matches the maximum width of the 
objects found in the core grid. Example train_1 appears to follow a different 
width determination or padding rule (output width 6 vs max object width 2) and 
may not be handled correctly by this code.
"""

# --- Helper Functions ---

def _find_core_grid(grid_np: np.ndarray, background_color: int) -> np.ndarray | None:
    """
    Finds the smallest bounding box containing all non-background cells
    and returns that subgrid.

    Args:
        grid_np: The input grid as a numpy array.
        background_color: The integer value representing the background.

    Returns:
        The core grid as a numpy array, or None if no non-background cells are found.
    """
    non_bg_coords = np.argwhere(grid_np != background_color)
    if non_bg_coords.size == 0:
        return None  # No non-background cells found

    min_r, min_c = non_bg_coords.min(axis=0)
    max_r, max_c = non_bg_coords.max(axis=0)

    core_grid = grid_np[min_r:max_r + 1, min_c:max_c + 1]
    return core_grid


def _find_objects_in_core(core_grid_np: np.ndarray, background_color: int) -> list[dict]:
    """
    Finds all connected components (objects) of non-background pixels within the core grid.

    Args:
        core_grid_np: The core grid (subgrid containing non-background pixels) as a numpy array.
        background_color: The integer value representing the background.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its 'bounds' (min_r, max_r, min_c, max_c) relative to the core grid
        and 'top_left' coordinate (min_r, min_c) relative to the core grid for sorting.
    """
    if core_grid_np is None or core_grid_np.size == 0:
        return []
        
    rows, cols = core_grid_np.shape
    visited = np.zeros_like(core_grid_np, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find a non-background cell that hasn't been visited
            if core_grid_np[r, c] != background_color and not visited[r, c]:
                component_pixels = [] # Store coordinates (r, c) of pixels in this component relative to core grid
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))

                    # Explore neighbors (4-way connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds within core_grid and if the neighbor is part of the object and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           core_grid_np[nr, nc] != background_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if component_pixels:
                    # Calculate bounding box relative to the core grid
                    obj_min_r = min(px[0] for px in component_pixels)
                    obj_max_r = max(px[0] for px in component_pixels)
                    obj_min_c = min(px[1] for px in component_pixels)
                    obj_max_c = max(px[1] for px in component_pixels)
                    
                    objects.append({
                        'bounds': (obj_min_r, obj_max_r, obj_min_c, obj_max_c),
                        'top_left': (obj_min_r, obj_min_c) # Use top-left relative to core grid for sorting
                    })

    # Sort objects based on their top-left corner within the core grid
    objects.sort(key=lambda obj: obj['top_left'])
    return objects


def _extract_subgrid_from_core(core_grid_np: np.ndarray, bounds: tuple) -> np.ndarray:
    """
    Extracts the rectangular subgrid defined by the bounds from the core grid.
    """
    min_r, max_r, min_c, max_c = bounds
    return core_grid_np[min_r:max_r+1, min_c:max_c+1]


def _pad_subgrid(subgrid_np: np.ndarray, target_width: int, background_color: int) -> np.ndarray:
    """
    Pads a subgrid with the background color to reach the target width.
    Padding is applied symmetrically (left and right). Handles empty/invalid inputs.
    """
    # Handle cases where subgrid might be None or empty after extraction
    if subgrid_np is None or subgrid_np.size == 0:
        # Cannot pad an empty array, maybe return an empty array of target width?
        # For this task, returning an empty array seems safer if extraction failed.
         return np.array([[]], dtype=int) if subgrid_np is None else subgrid_np

    # Ensure subgrid is 2D for shape access
    if subgrid_np.ndim == 1:
         subgrid_np = subgrid_np.reshape(1, -1) # Reshape 1D array to 2D row vector
         
    current_height, current_width = subgrid_np.shape

    if current_width == target_width:
        return subgrid_np # No padding needed
    elif current_width > target_width:
         # This case should ideally not happen if target_width is the max width
         # But if it does, return original or handle as error. Returning original for now.
         print(f"Warning: Subgrid width {current_width} > target width {target_width}. Returning original.")
         return subgrid_np

    # Calculate padding amounts
    padding_needed = target_width - current_width
    left_padding = padding_needed // 2
    right_padding = padding_needed - left_padding

    # Create padding arrays filled with the background color
    # Use subgrid_np.dtype to ensure type consistency
    left_pad_arr = np.full((current_height, left_padding), background_color, dtype=subgrid_np.dtype)
    right_pad_arr = np.full((current_height, right_padding), background_color, dtype=subgrid_np.dtype)

    # Concatenate horizontally: left_padding + subgrid + right_padding
    padded_subgrid = np.concatenate((left_pad_arr, subgrid_np, right_pad_arr), axis=1)
    return padded_subgrid


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    # Convert input to numpy array
    input_np = np.array(input_grid, dtype=int)
    background_color = 8

    # --- Step 1: Identify the Core Grid ---
    core_grid_np = _find_core_grid(input_np, background_color)

    # If no core grid found (e.g., input is all background), return empty
    if core_grid_np is None:
        return []

    # --- Step 2: Find Objects within the Core Grid ---
    # Objects are returned sorted by their top-left position within the core grid.
    objects = _find_objects_in_core(core_grid_np, background_color)

    # If no objects found within the core grid, return empty
    if not objects:
        return [] 

    # --- Step 3: Extract the Subgrid for Each Object from the Core Grid ---
    extracted_subgrids = []
    for obj in objects:
        subgrid = _extract_subgrid_from_core(core_grid_np, obj['bounds'])
        extracted_subgrids.append(subgrid)

    # Filter out potentially empty subgrids if extraction somehow failed for an object
    extracted_subgrids = [sg for sg in extracted_subgrids if sg.size > 0]
    if not extracted_subgrids:
        return []

    # --- Step 4: Determine the Target Width (Max Width among Extracted Subgrids) ---
    max_width = 0
    for subgrid in extracted_subgrids:
        width = subgrid.shape[1] if subgrid.ndim == 2 else (subgrid.size if subgrid.ndim == 1 else 0)
        max_width = max(max_width, width)
        
    # If max_width is still 0 (e.g., all objects were somehow empty points), return empty
    if max_width == 0:
        return []

    # --- Step 5: Pad Each Extracted Subgrid to the Maximum Width ---
    # The order is preserved from the sorted objects list.
    padded_subgrids = []
    for subgrid in extracted_subgrids:
        padded = _pad_subgrid(subgrid, max_width, background_color)
        # Check if padding resulted in a valid (non-empty) grid before adding
        if padded.size > 0:
            padded_subgrids.append(padded)
            
    # If no valid padded subgrids remain, return empty
    if not padded_subgrids:
        return []

    # --- Step 6: Concatenate Padded Subgrids Vertically ---
    # Use numpy's vstack for efficient vertical stacking
    output_np = np.vstack(padded_subgrids)

    # --- Step 7: Convert Final Numpy Array Back to List of Lists ---
    output_grid = output_np.tolist()

    return output_grid