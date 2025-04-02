import numpy as np
from typing import List, Tuple, Dict, Set, Optional

"""
Identify two distinct non-background objects in the input grid. An object is a contiguous group of non-background pixels (colors 1-9), connected cardinally, and can be composed of multiple colors.
One object acts as a 'frame': it must be monochromatic (all its pixels have the same single color) and enclose a rectangular area composed entirely of the background color (white, 0).
The other object acts as a 'pattern'.
Copy the 'pattern' object (preserving its shape and colors relative to its bounding box) into the background area enclosed by the 'frame' object.
The alignment is such that the top-left corner of the pattern's bounding box corresponds to the top-left corner of the frame's enclosed background area.
The original pattern and frame objects remain in their initial positions in the output grid, with the copied pattern overwriting the background inside the frame.
"""

def find_connected_components(grid: np.ndarray, background_color: int = 0) -> List[Set[Tuple[int, int]]]:
    """
    Finds all distinct contiguous groups (objects) of non-background pixels.
    Objects can be multi-colored. Connection is cardinal (4-way).

    Args:
        grid: The input numpy array representing the grid.
        background_color: The integer value representing the background color.

    Returns:
        A list where each element is a set of (row, col) tuples representing an object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != background_color:
                # Start BFS for a new object
                obj_pixels = set()
                q = [(r, c)]
                visited.add((r, c))

                while q:
                    row, col = q.pop(0)
                    obj_pixels.add((row, col))

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] != background_color:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                if obj_pixels:
                    objects.append(obj_pixels)

    return objects

def get_bounding_box(pixels: Set[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """
    Calculates the bounding box of a set of pixels.

    Args:
        pixels: A set of (row, col) tuples.

    Returns:
        A tuple (min_row, min_col, max_row, max_col). Returns (0,0,0,0) for empty set.
    """
    if not pixels:
        return (0, 0, 0, 0) # Or raise error, depending on expected usage
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    return min(rows), min(cols), max(rows), max(cols)

def get_object_colors(grid: np.ndarray, pixels: Set[Tuple[int, int]]) -> Set[int]:
    """Gets the set of unique colors present in an object's pixels."""
    return set(grid[r, c] for r, c in pixels)

def find_frame_details(grid: np.ndarray, obj_pixels: Set[Tuple[int, int]], background_color: int = 0) -> Optional[Tuple[int, int]]:
    """
    Checks if an object is a frame (encloses a pure background rectangle).

    Args:
        grid: The input numpy array.
        obj_pixels: The set of pixels belonging to the potential frame object.
        background_color: The background color value.

    Returns:
        The (row, col) of the top-left corner of the enclosed background area if it's a valid frame,
        otherwise None.
    """
    if not obj_pixels:
        return None

    min_r, min_c, max_r, max_c = get_bounding_box(obj_pixels)

    # Frame needs space for an interior
    if max_r <= min_r + 1 or max_c <= min_c + 1:
        return None

    inner_bg_pixels = set()
    potential_inner_area_defined = False

    # Iterate through the potential inner rectangle (excluding the bounding box edges)
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            if (r, c) not in obj_pixels:
                potential_inner_area_defined = True # At least one non-object pixel inside BB
                if grid[r, c] == background_color:
                    inner_bg_pixels.add((r, c))
                else:
                    # Found a non-background color inside that doesn't belong to the object
                    return None # Not a valid frame

    # If we checked the inner area and found no non-object pixels, or only object pixels,
    # it doesn't enclose a background area. Also requires at least one bg pixel inside.
    if not potential_inner_area_defined or not inner_bg_pixels:
         return None

    # Verify the background pixels form a solid rectangle
    inner_min_r, inner_min_c, inner_max_r, inner_max_c = get_bounding_box(inner_bg_pixels)
    expected_bg_count = (inner_max_r - inner_min_r + 1) * (inner_max_c - inner_min_c + 1)
    if len(inner_bg_pixels) != expected_bg_count:
        # The background pixels found don't form a solid rectangle
        return None
    # Check if all pixels within this inner bounding box are indeed the found background pixels
    for r in range(inner_min_r, inner_max_r + 1):
        for c in range(inner_min_c, inner_max_c + 1):
            if (r,c) not in inner_bg_pixels:
                 # Hole in the background rectangle or includes non-bg pixels mistakenly identified
                 return None # This check might be redundant due to previous checks but adds robustness

    # All checks passed, it encloses a background rectangle
    return (inner_min_r, inner_min_c)


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the frame/pattern copy rule.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    background_color = 0
    rows, cols = input_np.shape

    # 1. Find all distinct connected non-background objects
    objects_pixels = find_connected_components(input_np, background_color)

    # 2. Expect exactly two objects
    if len(objects_pixels) != 2:
        # print(f"Error: Expected 2 objects, found {len(objects_pixels)}. Returning original grid.")
        return input_grid # Task constraint not met

    # 3. Identify frame and pattern
    frame_obj_pixels: Optional[Set[Tuple[int, int]]] = None
    pattern_obj_pixels: Optional[Set[Tuple[int, int]]] = None
    frame_inner_tl: Optional[Tuple[int, int]] = None

    for i, obj_pixels in enumerate(objects_pixels):
        colors = get_object_colors(input_np, obj_pixels)
        is_mono = len(colors) == 1
        
        # Check if it's potentially a frame (monochromatic and encloses background)
        if is_mono:
            inner_tl = find_frame_details(input_np, obj_pixels, background_color)
            if inner_tl is not None:
                # Found the frame
                if frame_obj_pixels is not None:
                     # Error: Found more than one object matching frame criteria
                     # print("Error: Ambiguous frame identification. Returning original grid.")
                     return input_grid
                frame_obj_pixels = obj_pixels
                frame_inner_tl = inner_tl
                # The other object must be the pattern
                pattern_obj_pixels = objects_pixels[1 - i]
                # break # Found frame, no need to check the other as a frame

    # 4. Verify frame and pattern were identified
    if frame_obj_pixels is None or pattern_obj_pixels is None or frame_inner_tl is None:
        # print("Error: Could not identify frame and pattern objects uniquely. Returning original grid.")
        return input_grid # Identification failed

    # 5. Get bounding box of the pattern
    pat_min_r, pat_min_c, _, _ = get_bounding_box(pattern_obj_pixels)

    # 6. Get top-left coordinate of the frame's inner area
    target_r_start, target_c_start = frame_inner_tl

    # 7. Copy pattern pixels into the frame's inner area in the output grid
    for r, c in pattern_obj_pixels:
        # Calculate relative position within the pattern's bounding box
        relative_r = r - pat_min_r
        relative_c = c - pat_min_c

        # Calculate target position in the output grid
        target_r = target_r_start + relative_r
        target_c = target_c_start + relative_c

        # Ensure the target position is within the grid bounds (safety check)
        if 0 <= target_r < rows and 0 <= target_c < cols:
            # Get the color of the pattern pixel from the input grid
            pattern_color = input_np[r, c]
            # Update the output grid at the target coordinate
            # (This overwrites the background pixels inside the frame)
            output_np[target_r, target_c] = pattern_color
        # else: # Optional: handle cases where pattern might theoretically extend beyond frame's inner area/grid bounds
            # print(f"Warning: Pattern pixel at ({r},{c}) maps outside grid to ({target_r},{target_c}). Skipping.")

    # Convert back to list of lists for the required output format
    return output_np.tolist()