import numpy as np
from typing import List, Tuple, Optional

"""
The transformation rule operates on a 2D grid containing integers (0, 2, 5).
It identifies a static 'boundary' pattern (value 2) and a mobile 'object' pattern group (value 5).

1.  The boundary pattern (2) remains fixed in its original position in the output grid.
2.  The object pattern group (5), potentially consisting of multiple disconnected components treated as a single entity based on their combined bounding box, is moved from its original location.
3.  The original locations occupied by the object group become background (0) in the output.
4.  An 'internal empty space' is identified. This space consists of all background cells (0) located within the bounding box of the boundary pattern (2) in the input grid.
5.  The object pattern group (5) is then placed onto the output grid. The placement is determined by aligning the geometric center of the object pattern group's bounding box (from the input) with the geometric center of the bounding box of the identified 'internal empty space'.
6.  The relative spatial arrangement of all cells within the object group (5) is preserved during the move.
7.  If essential components (boundary pattern, object pattern, or internal empty space) are missing, the transformation might not fully apply, potentially resulting in an output grid containing only the copied boundary pattern.
"""

# =================================
# Helper Functions
# =================================

def find_cells(grid: np.ndarray, value: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of cells with a specific value."""
    rows, cols = np.where(grid == value)
    # Use tolist() to ensure standard python ints, not numpy ints
    return list(zip(rows.tolist(), cols.tolist()))

def get_bounding_box(coords: List[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col) for a list of coordinates.
    Returns None if the list is empty.
    """
    if not coords:
        return None
    rows, cols = zip(*coords)
    min_row = min(rows)
    min_col = min(cols)
    max_row = max(rows)
    max_col = max(cols)
    return min_row, min_col, max_row, max_col

def get_relative_pattern_group(grid: np.ndarray, value: int) -> Tuple[List[Tuple[int, int]], Optional[Tuple[int, int, int, int]]]:
    """
    Finds the pattern of a given value relative to its combined top-left corner.
    Returns a list of relative coordinates (relative_row, relative_col) and the
    combined bounding box (min_row, min_col, max_row, max_col) of the pattern in the original grid.
    Returns ([], None) if no cells of the value are found.
    """
    coords = find_cells(grid, value)
    if not coords:
        return [], None

    bbox = get_bounding_box(coords)
    # bbox is guaranteed not None here because coords is not empty
    min_row, min_col, _, _ = bbox # type: ignore

    relative_coords = [(r - min_row, c - min_col) for r, c in coords]
    return relative_coords, bbox

def find_internal_zeros_bbox(grid: np.ndarray, container_bbox: Optional[Tuple[int, int, int, int]]) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the bounding box of the zero cells (0) located strictly within the given container_bbox.
    Returns (min_row, min_col, max_row, max_col) or None if no container or no zeros inside.
    """
    if container_bbox is None:
        return None

    c_min_r, c_min_c, c_max_r, c_max_c = container_bbox
    zero_coords = find_cells(grid, 0)

    # Filter zero cells to include only those strictly within the container bounding box
    internal_zeros = [
        (r, c) for r, c in zero_coords
        if c_min_r <= r <= c_max_r and c_min_c <= c <= c_max_c
    ]
    
    # Return the bounding box of these internal zero cells
    return get_bounding_box(internal_zeros)

def calculate_center(bbox: Optional[Tuple[int, int, int, int]]) -> Optional[Tuple[float, float]]:
    """Calculates the geometric center (row, col) of a bounding box."""
    if bbox is None:
        return None
    min_r, min_c, max_r, max_c = bbox
    center_r = min_r + (max_r - min_r) / 2.0
    center_c = min_c + (max_c - min_c) / 2.0
    return center_r, center_c

# =================================
# Main Transformation Function
# =================================

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    # Initialize output grid with background color 0
    output_array = np.zeros_like(input_array)

    # --- Step 1 & 2: Identify and copy the boundary pattern (value 2) ---
    boundary_coords = find_cells(input_array, 2)
    for r, c in boundary_coords:
        output_array[r, c] = 2
    # Calculate the bounding box of the boundary
    boundary_bbox = get_bounding_box(boundary_coords)

    # --- Step 4 & 5: Identify the object pattern group (value 5) ---
    object_relative_coords, object_bbox_in = get_relative_pattern_group(input_array, 5)

    # If no object pattern, return the grid with only the (potentially empty) boundary
    if not object_relative_coords or object_bbox_in is None:
        return output_array.tolist()

    # --- Step 6 & 7: Identify the bounding box of the internal empty space ---
    internal_zeros_bbox = find_internal_zeros_bbox(input_array, boundary_bbox)

    # If no internal empty space found (e.g., no boundary, or no zeros inside boundary bbox),
    # return grid with only the boundary pattern copied.
    if internal_zeros_bbox is None:
         return output_array.tolist()

    # --- Step 8 & 9: Calculate centers ---
    object_center_in = calculate_center(object_bbox_in)
    internal_zeros_center = calculate_center(internal_zeros_bbox)

    # Defensive check: ensure centers could be calculated
    if object_center_in is None or internal_zeros_center is None:
         # This case should technically be covered by earlier checks, but belts and suspenders
         return output_array.tolist()

    # --- Step 10: Calculate target top-left corner for placing the object group ---
    # The goal is to align the centers. We calculate the offset required to move
    # the object's original center to the target center, and apply this offset
    # to the object's original top-left corner.

    obj_min_r, obj_min_c, _, _ = object_bbox_in # Original top-left
    obj_center_r, obj_center_c = object_center_in # Original center
    target_center_r, target_center_c = internal_zeros_center # Target center

    # Calculate the difference (offset) between target and original centers
    offset_r = target_center_r - obj_center_r
    offset_c = target_center_c - obj_center_c

    # Apply the offset to the original top-left corner and round to get target top-left
    target_min_r = int(round(obj_min_r + offset_r))
    target_min_c = int(round(obj_min_c + offset_c))

    # --- Step 11: Place the object pattern group onto the output grid ---
    for rel_r, rel_c in object_relative_coords:
        # Calculate the absolute coordinates in the output grid
        place_r = target_min_r + rel_r
        place_c = target_min_c + rel_c

        # Place the object cell (value 5) if it's within the grid boundaries
        if 0 <= place_r < rows and 0 <= place_c < cols:
            # Overwrite whatever value is currently at the target location (likely 0)
            output_array[place_r, place_c] = 5

    # --- Step 12: Return the final grid ---
    # Convert the NumPy array back to a standard Python list of lists
    return output_array.tolist()