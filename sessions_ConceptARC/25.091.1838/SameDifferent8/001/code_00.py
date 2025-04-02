import numpy as np
from collections import Counter
import itertools

"""
1.  **Find Separator:** Scan the input grid rows and columns to find a line composed entirely of white (0) pixels. This line separates the grid into two subgrids. Define the subgrid encountered first (top or left) as Subgrid A and the other (bottom or right) as Subgrid B.
2.  **Identify Inner Colors and Shapes:**
    *   In Subgrid A, determine the background color (most frequent non-white) and the inner color (the other non-white color). Extract the shape (relative pixel coordinates) formed by the inner color (Shape A).
    *   In Subgrid B, determine the background color and the inner color. Extract the shape formed by the inner color (Shape B).
    *   Verify that the inner color is the same in both subgrids. Let the common inner color be `C`.
3.  **Compare Shapes:** Check if Shape A and Shape B are identical (same pattern of `C` pixels relative to their top-left corners).
4.  **Determine Output Based on Comparison:**
    *   **If Shape A and Shape B are identical:**
        a.  Find the minimum bounding box containing Shape A within Subgrid A.
        b.  Create an output grid matching the size of this bounding box.
        c.  Fill the output grid: For each position within the bounding box, if the corresponding pixel in Subgrid A is the inner color `C`, place `C` in the output. Otherwise, place white (0).
    *   **If Shape A and Shape B are different:**
        a.  Determine if Shape B constitutes a solid, filled rectangle (a rectangular block of color `C` with no holes or missing internal pixels).
        b.  **If Shape B is a solid rectangle:** The output is a 1x1 grid containing only white (0).
        c.  **If Shape B is NOT a solid rectangle:**
            i.  Find the minimum bounding box containing Shape B within Subgrid B.
            ii. Create an output grid matching the size of this bounding box.
            iii. Fill the output grid: For each position within the bounding box, if the corresponding pixel in Subgrid B is the inner color `C`, place `C` in the output. Otherwise, place white (0).
5.  **Return Output:** Return the generated output grid.
"""

def _find_separator(grid):
    """Finds the row or column index of the separator line (all zeros)."""
    height, width = grid.shape
    # Check rows
    for r in range(height):
        if np.all(grid[r, :] == 0):
            return 'row', r
    # Check columns
    for c in range(width):
        if np.all(grid[:, c] == 0):
            return 'col', c
    return None, -1 # Should not happen based on problem description

def _split_grid(grid, separator_type, separator_index):
    """Splits the grid into two subgrids based on the separator."""
    if separator_type == 'row':
        subgrid_a = grid[:separator_index, :]
        subgrid_b = grid[separator_index + 1:, :]
    elif separator_type == 'col':
        subgrid_a = grid[:, :separator_index]
        subgrid_b = grid[:, separator_index + 1:]
    else:
         # Handle error case or unexpected input - return empty grids for safety
        return np.array([[]]), np.array([[]])
    return subgrid_a, subgrid_b

def _find_pattern(subgrid):
    """Identifies background, inner color, relative coordinates, and bounding box."""
    if subgrid.size == 0:
         # Handle empty subgrid case
        return -1, -1, set(), None # Indicate invalid pattern

    # Count colors, ignoring white (0)
    colors, counts = np.unique(subgrid[subgrid != 0], return_counts=True)

    if len(colors) == 0: # Only white pixels or empty
        return -1, -1, set(), None
    elif len(colors) == 1: # Only one non-white color
        background_color = -1 # No distinct background within the non-white pixels
        inner_color = colors[0]
    else:
        # Assume background is the most frequent non-white color
        # And inner is the second most frequent (or only other non-white)
        sorted_indices = np.argsort(counts)[::-1]
        background_color = colors[sorted_indices[0]]
        inner_color = colors[sorted_indices[1]] # Might fail if only one non-white color, handled above

    # Find coordinates of the inner color
    inner_coords = np.argwhere(subgrid == inner_color)

    if inner_coords.size == 0:
        return background_color, inner_color, set(), None # Inner color not found

    # Calculate bounding box
    min_r, min_c = inner_coords.min(axis=0)
    max_r, max_c = inner_coords.max(axis=0)
    bbox = (min_r, min_c, max_r, max_c)

    # Calculate relative coordinates (relative to top-left of bounding box)
    relative_coords = set((r - min_r, c - min_c) for r, c in inner_coords)

    return background_color, inner_color, relative_coords, bbox

def _compare_shapes(coords_a, coords_b):
    """Compares two sets of relative coordinates."""
    return coords_a == coords_b

def _is_solid_rectangle(relative_coords, bbox):
    """Checks if the shape defined by relative_coords forms a solid rectangle."""
    if not relative_coords or bbox is None:
        return False
    min_r, min_c, max_r, max_c = bbox # Bbox is absolute, but we use relative coords
    # Calculate dimensions based on relative coords
    rel_max_r = max(r for r, c in relative_coords)
    rel_max_c = max(c for r, c in relative_coords)
    height = rel_max_r + 1
    width = rel_max_c + 1

    # Check if the number of points matches the area of the rectangle
    if len(relative_coords) != height * width:
        return False

    # Check if all points within the relative bounding box are present
    for r in range(height):
        for c in range(width):
            if (r, c) not in relative_coords:
                return False
    return True

def _create_output_pattern(subgrid, inner_color, bbox):
    """Creates the output pattern based on the subgrid, inner color, and bbox."""
    if bbox is None:
       # Handle case where pattern wasn't found properly
       return np.array([[0]]) # Default or error output

    min_r, min_c, max_r, max_c = bbox
    # Extract the relevant portion of the subgrid
    pattern_area = subgrid[min_r:max_r+1, min_c:max_c+1]
    # Create output grid, replacing background with white (0)
    output_grid = np.where(pattern_area == inner_color, inner_color, 0)
    return output_grid


def transform(input_grid):
    """
    Transforms the input grid based on comparing patterns in two subgrids separated by a line of zeros.
    """
    input_grid = np.array(input_grid)

    # 1. Find Separator and Split Grid
    separator_type, separator_index = _find_separator(input_grid)
    if separator_type is None:
        # Handle error: No separator found (shouldn't happen based on examples)
        return np.array([[0]]) # Return a default small grid

    subgrid_a, subgrid_b = _split_grid(input_grid, separator_type, separator_index)

    # 2. Identify Inner Colors and Shapes
    bg_a, inner_a, coords_a, bbox_a = _find_pattern(subgrid_a)
    bg_b, inner_b, coords_b, bbox_b = _find_pattern(subgrid_b)

    # Basic validation: Check if patterns were found and inner colors match
    if inner_a == -1 or inner_b == -1 : # check if pattern finding failed for either
         # Handle cases where one or both subgrids lack a clear pattern per rules
         # Example 2 and 4 output 0, potentially due to this or the rectangle rule.
         # Let's assume for now if one pattern is invalid, the shapes are different.
         # If B has a valid pattern, check if it's a solid rectangle.
         if inner_b != -1 and _is_solid_rectangle(coords_b, bbox_b):
             return np.array([[0]])
         elif inner_b != -1: # If B is valid but not rectangle, maybe output B? Need more info/examples.
             return _create_output_pattern(subgrid_b, inner_b, bbox_b)
         else: # If B is also invalid, output 0 seems safest based on examples 2 & 4
             return np.array([[0]])

    if inner_a != inner_b:
        # Handle error: Inner colors don't match (not expected from examples)
        # Defaulting to the "different shapes" logic might be reasonable.
        # Treat as different shapes. Check if B is solid rectangle.
        if _is_solid_rectangle(coords_b, bbox_b):
             return np.array([[0]])
        else:
             return _create_output_pattern(subgrid_b, inner_b, bbox_b)

    inner_color = inner_a # Common inner color

    # 3. Compare Shapes
    shapes_are_identical = _compare_shapes(coords_a, coords_b)

    # 4. Determine Output Based on Comparison
    if shapes_are_identical:
        # Use pattern from Subgrid A
        output_grid = _create_output_pattern(subgrid_a, inner_color, bbox_a)
    else:
        # Shapes are different, check if Shape B is a solid rectangle
        is_b_solid_rect = _is_solid_rectangle(coords_b, bbox_b)
        if is_b_solid_rect:
            # Output is a single white pixel
            output_grid = np.array([[0]])
        else:
            # Use pattern from Subgrid B
            output_grid = _create_output_pattern(subgrid_b, inner_color, bbox_b)

    # 5. Return Output
    return output_grid.tolist() # Convert back to list of lists if required by caller