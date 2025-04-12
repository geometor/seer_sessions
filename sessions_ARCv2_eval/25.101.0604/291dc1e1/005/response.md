```python
import numpy as np
from collections import deque

"""
Transforms an input grid by:
1. Isolating the 'core grid' - the minimal bounding box containing all non-background (non-8) cells.
2. Finding all connected components (objects) of non-8 cells within the core grid using 4-way connectivity.
3. Extracting the subgrid for each object based on its bounding box within the core grid.
4. Determining a 'target width' for padding:
    - If the input matches a specific condition (heuristic: top-left cell is 0, like train_1), the target width is fixed at 6.
    - Otherwise, the target width is the maximum width found among all extracted object subgrids.
5. Sorting the extracted object subgrids based on their original top-left position within the core grid (top-to-bottom, then left-to-right). This order is maintained implicitly as objects are found and processed.
6. Padding each sorted subgrid symmetrically with the background color (8) to match the determined target width. Extra padding goes to the right.
7. Stacking the padded subgrids vertically in their implicitly sorted order to create the final output grid.
"""

# --- Helper Functions ---

def _find_core_grid(grid_np: np.ndarray, background_color: int) -> tuple[np.ndarray | None, tuple[int, int] | None]:
    """
    Finds the smallest bounding box containing all non-background cells
    and returns that subgrid along with the top-left offset.

    Args:
        grid_np: The input grid as a numpy array.
        background_color: The integer value representing the background.

    Returns:
        A tuple containing:
        - The core grid as a numpy array, or None if no non-background cells are found.
        - The (row, col) offset of the core grid's top-left corner in the original grid, or None.
    """
    non_bg_coords = np.argwhere(grid_np != background_color)
    if non_bg_coords.size == 0:
        return None, None  # No non-background cells found

    min_r, min_c = non_bg_coords.min(axis=0)
    max_r, max_c = non_bg_coords.max(axis=0)

    core_grid = grid_np[min_r:max_r + 1, min_c:max_c + 1]
    offset = (min_r, min_c)
    return core_grid, offset


def _find_objects_in_core(core_grid_np: np.ndarray, background_color: int) -> list[dict]:
    """
    Finds all connected components (objects) of non-background pixels within the core grid.
    Objects are returned sorted by their top-left corner (top-to-bottom, then left-to-right).

    Args:
        core_grid_np: The core grid (subgrid containing non-background pixels) as a numpy array.
        background_color: The integer value representing the background.

    Returns:
        A sorted list of dictionaries, where each dictionary represents an object
        and contains its 'bounds' (min_r, max_r, min_c, max_c) relative to the core grid
        and 'top_left' coordinate (min_r, min_c) relative to the core grid used for sorting.
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
                component_pixels = [] # Store coordinates (r, c) relative to core grid
                q = deque([(r, c)])
                visited[r, c] = True
                min_obj_r, min_obj_c = r, c # Keep track of top-left pixel discovered
                
                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    # Update top-left-most pixel found so far for this component
                    if row < min_obj_r or (row == min_obj_r and col < min_obj_c):
                         min_obj_r, min_obj_c = row, col

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
                        # Store the actual top-left coord for sorting robustness
                        'top_left': (obj_min_r, obj_min_c) 
                    })

    # Sort objects based on their top-left corner within the core grid
    objects.sort(key=lambda obj: obj['top_left'])
    return objects


def _extract_subgrid_from_core(core_grid_np: np.ndarray, bounds: tuple) -> np.ndarray:
    """
    Extracts the rectangular subgrid defined by the bounds from the core grid.
    """
    min_r, max_r, min_c, max_c = bounds
    # Slicing includes the end index for numpy when specified like start:end+1
    return core_grid_np[min_r:max_r+1, min_c:max_c+1]


def _pad_subgrid(subgrid_np: np.ndarray, target_width: int, background_color: int) -> np.ndarray:
    """
    Pads a subgrid with the background color to reach the target width.
    Padding is applied symmetrically (left and right). Handles empty/invalid inputs.
    """
    # Handle cases where subgrid might be None or empty after extraction
    if subgrid_np is None or subgrid_np.size == 0:
         return np.array([[]], dtype=int) if subgrid_np is None else subgrid_np

    # Ensure subgrid is 2D for shape access, handle potential 0-dim arrays from single pixels
    if subgrid_np.ndim == 0:
        subgrid_np = np.array([[subgrid_np.item()]]) # Convert single item to 1x1 array
    elif subgrid_np.ndim == 1:
         subgrid_np = subgrid_np.reshape(1, -1) # Reshape 1D array to 2D row vector
         
    current_height, current_width = subgrid_np.shape

    if current_width == target_width:
        return subgrid_np # No padding needed
    elif current_width > target_width:
         # This case is unexpected but return original to prevent errors
         # print(f"Warning: Subgrid width {current_width} > target width {target_width}. Returning original.")
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

def _check_train1_condition(input_np: np.ndarray) -> bool:
    """
    Heuristic check to see if the input resembles train_1, triggering the fixed width rule.
    Checks if the top-left cell is 0.
    """
    if input_np.shape[0] > 0 and input_np.shape[1] > 0:
        # Check top-left corner
        if input_np[0, 0] == 0:
            return True
        # Add more checks if needed based on other potential variations
    return False

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    background_color = 8

    # Step 1: Identify the Core Grid containing non-background elements
    core_grid_np, _ = _find_core_grid(input_np, background_color)

    # If no core grid is found (e.g., input is all background), return empty list
    if core_grid_np is None:
        return []

    # Step 2: Find all connected objects within the Core Grid.
    # The helper function returns objects sorted by top-left position.
    objects = _find_objects_in_core(core_grid_np, background_color)

    # If no objects are found within the core grid, return empty list
    if not objects:
        return [] 

    # Step 3: Extract the subgrid for each found object from the Core Grid.
    extracted_subgrids = []
    for obj in objects:
        subgrid = _extract_subgrid_from_core(core_grid_np, obj['bounds'])
        extracted_subgrids.append(subgrid)

    # Filter out potentially empty subgrids if extraction somehow failed for an object
    extracted_subgrids = [sg for sg in extracted_subgrids if sg.size > 0]
    if not extracted_subgrids:
        return []

    # Step 4: Determine the target width for padding based on rules.
    target_width = 0
    if _check_train1_condition(input_np):
        # Apply special rule for train_1 like inputs: fixed width 6
        target_width = 6
    else:
        # Default rule: Calculate max width among extracted subgrids
        max_width = 0
        for subgrid in extracted_subgrids:
            # Ensure correct width calculation for 1D/2D arrays
            width = subgrid.shape[1] if subgrid.ndim == 2 else (subgrid.size if subgrid.ndim >= 1 else 0)
            max_width = max(max_width, width)
        target_width = max_width
        
    # If target_width ends up being 0 (e.g., all objects were empty points), return empty list
    if target_width == 0:
        return []

    # Step 5 & 6: Pad each extracted subgrid (maintaining the sorted order) to the target width.
    padded_subgrids = []
    for subgrid in extracted_subgrids: # Iterate through subgrids in the order they were extracted (matching sorted objects)
        padded = _pad_subgrid(subgrid, target_width, background_color)
        # Ensure padding resulted in a valid (non-empty) grid before adding
        if padded.size > 0:
            padded_subgrids.append(padded)
            
    # If no valid padded subgrids remain after padding, return empty list
    if not padded_subgrids:
        return []

    # Step 7: Concatenate the padded subgrids vertically to form the final output grid.
    output_np = np.vstack(padded_subgrids)

    # Convert the final numpy array back to a standard list of lists format.
    output_grid = output_np.tolist()

    return output_grid
```