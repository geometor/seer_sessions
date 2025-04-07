```python
import numpy as np
from collections import Counter

"""
Transformation Rule:

1.  Identify the background color (most frequent color).
2.  Identify the two unique non-background colors. One color forms a single contiguous 'pattern' object, and the other color appears as multiple single 'marker' pixels.
3.  Find the coordinates of all marker pixels.
4.  Find the coordinates of all pixels belonging to the pattern object.
5.  Determine the 'center' of the pattern object (using the center of its bounding box).
6.  Calculate the relative coordinates of each pattern pixel with respect to this center.
7.  Create an output grid of the same dimensions as the input, filled with the background color.
8.  For each marker pixel coordinate (anchor point):
    a.  Iterate through the relative coordinates of the pattern pixels.
    b.  Calculate the absolute target coordinate in the output grid by adding the anchor point coordinate to the relative pattern coordinate.
    c.  If the target coordinate is within the grid bounds, place the corresponding pattern pixel color at that location in the output grid, overwriting the background color.
9.  Return the modified output grid.
"""

def find_objects(grid, color, connectivity=8):
    """Finds connected components (objects) of a specific color."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = []
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    obj_coords.append((row, col))

                    # Define neighbors based on connectivity
                    if connectivity == 8: # Queen's case (includes diagonals)
                        potential_neighbors = [
                            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                            (row, col - 1),                 (row, col + 1),
                            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
                        ]
                    else: # Rook's case (only orthogonal)
                         potential_neighbors = [
                                     (row - 1, col),
                            (row, col - 1),         (row, col + 1),
                                     (row + 1, col)
                         ]

                    for nr, nc in potential_neighbors:
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                objects.append(obj_coords)
    return objects

def get_bounding_box(coords):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a list of coordinates."""
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def get_center(bbox):
    """Calculates the 'center' coordinate from a bounding box. Uses integer division."""
    if not bbox:
        return None
    min_r, min_c, max_r, max_c = bbox
    # Using integer division, effectively floor((min+max)/2)
    center_r = (min_r + max_r) // 2
    center_c = (min_c + max_c) // 2
    return center_r, center_c

def transform(input_grid):
    """
    Applies the pattern stamping transformation.
    Identifies a pattern object and marker pixels in the input grid.
    Stamps the pattern onto an output grid centered at each marker location.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Determine background color
    colors, counts = np.unique(input_np, return_counts=True)
    background_color = colors[np.argmax(counts)]

    # 2. Identify non-background colors
    non_background_colors = [c for c in colors if c != background_color]

    if len(non_background_colors) != 2:
        # This rule assumes exactly two non-background colors: one pattern, one marker
        # Handle error or edge case if needed, maybe return input or raise error
        print(f"Warning: Expected 2 non-background colors, found {len(non_background_colors)}. Returning input.")
        return input_grid # Or handle differently

    color1, color2 = non_background_colors

    # 3 & 4. Identify pattern and marker colors/objects
    objects1 = find_objects(input_np, color1)
    objects2 = find_objects(input_np, color2)

    pattern_color = -1
    marker_color = -1
    pattern_coords = []
    marker_coords = []

    # Assume pattern is the single larger object, markers are multiple single pixels
    # Check color1
    if len(objects1) == 1 and len(objects1[0]) > 1: # Single object, more than one pixel -> Pattern
        pattern_color = color1
        pattern_coords = objects1[0]
        # Check if color2 consists of single-pixel objects -> Markers
        if all(len(obj) == 1 for obj in objects2):
            marker_color = color2
            marker_coords = [obj[0] for obj in objects2]
        else:
             print("Warning: Ambiguous pattern/marker identification (Case 1).")
             return input_grid # Or handle differently

    # Check color2 (if color1 wasn't the pattern)
    elif len(objects2) == 1 and len(objects2[0]) > 1: # Single object, more than one pixel -> Pattern
        pattern_color = color2
        pattern_coords = objects2[0]
         # Check if color1 consists of single-pixel objects -> Markers
        if all(len(obj) == 1 for obj in objects1):
            marker_color = color1
            marker_coords = [obj[0] for obj in objects1]
        else:
            print("Warning: Ambiguous pattern/marker identification (Case 2).")
            return input_grid # Or handle differently
    else:
         # This handles cases like two single-pixel colors, or two multi-pixel objects etc.
         # Based on examples, Markers seem to always be single pixels.
         # Let's refine: Markers are *always* single pixels. Pattern is the other one.
         is_obj1_markers = all(len(obj) == 1 for obj in objects1)
         is_obj2_markers = all(len(obj) == 1 for obj in objects2)

         if is_obj1_markers and not is_obj2_markers and len(objects2) == 1:
             marker_color = color1
             marker_coords = [obj[0] for obj in objects1]
             pattern_color = color2
             pattern_coords = objects2[0]
         elif is_obj2_markers and not is_obj1_markers and len(objects1) == 1:
             marker_color = color2
             marker_coords = [obj[0] for obj in objects2]
             pattern_color = color1
             pattern_coords = objects1[0]
         else:
            print("Warning: Could not definitively identify pattern and marker colors based on object structure.")
            # Fallback: Let's check counts, maybe marker color is more frequent non-bg?
            # Or maybe pattern color always has >1 pixel total?
            count1 = np.sum(input_np == color1)
            count2 = np.sum(input_np == color2)
            if count1 > 1 and count2 > 0 and is_obj2_markers: # Assume color1 is pattern, color2 is marker
                 pattern_color = color1
                 pattern_coords = [(r,c) for r in range(rows) for c in range(cols) if input_np[r,c] == color1] # Recalculate coords if needed
                 marker_color = color2
                 marker_coords = [obj[0] for obj in objects2]
            elif count2 > 1 and count1 > 0 and is_obj1_markers: # Assume color2 is pattern, color1 is marker
                 pattern_color = color2
                 pattern_coords = [(r,c) for r in range(rows) for c in range(cols) if input_np[r,c] == color2] # Recalculate coords if needed
                 marker_color = color1
                 marker_coords = [obj[0] for obj in objects1]
            else:
                print("Fallback failed.")
                return input_grid # Or handle differently


    if not pattern_coords or not marker_coords:
        print("Warning: Failed to find pattern or markers.")
        return input_grid # Or handle differently

    # 5. Determine pattern center
    pattern_bbox = get_bounding_box(pattern_coords)
    pattern_center_r, pattern_center_c = get_center(pattern_bbox)

    # 6. Calculate relative pattern coordinates
    # Store as dictionary: {(dr, dc): color} - color is always pattern_color here
    relative_pattern = {}
    for r, c in pattern_coords:
        dr = r - pattern_center_r
        dc = c - pattern_center_c
        relative_pattern[(dr, dc)] = pattern_color

    # 7. Create output grid
    output_np = np.full_like(input_np, background_color)

    # 8. Stamp pattern for each marker
    for anchor_r, anchor_c in marker_coords:
        # 8a. Iterate through relative coordinates
        for (dr, dc), p_color in relative_pattern.items():
            # 8b. Calculate target coordinate
            target_r = anchor_r + dr
            target_c = anchor_c + dc

            # 8c. Check bounds and place pixel
            if 0 <= target_r < rows and 0 <= target_c < cols:
                output_np[target_r, target_c] = p_color

    # 9. Return the modified grid as list of lists
    return output_np.tolist()
```