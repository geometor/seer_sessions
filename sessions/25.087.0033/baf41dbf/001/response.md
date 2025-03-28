```python
import numpy as np
from collections import deque

"""
Identifies green (3) rectangular frames and magenta (6) markers in the input grid.
For each green frame, it determines its initial bounding box.
It then searches for magenta markers located strictly outside this initial bounding box.
The frame's boundaries are expanded outwards (up, down, left, right) to align with the row/column of the outermost magenta markers found in each respective direction.
A new output grid is created, initially all white (0).
The expanded green frames are drawn onto this output grid. The area inside the frame remains white (0).
Finally, the original magenta markers are redrawn in their original positions on the output grid.
"""

def find_objects(grid, color):
    """
    Finds all connected components of a given color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of pixels belonging to a connected object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 4 cardinal neighbors (no diagonals needed for frames)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_coords: # ensure we found something
                    objects.append(obj_coords)
    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) inclusive.
               Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None
    
    min_row = min(r for r, c in obj_coords)
    min_col = min(c for r, c in obj_coords)
    max_row = max(r for r, c in obj_coords)
    max_col = max(c for r, c in obj_coords)
    
    return min_row, min_col, max_row, max_col

# Basic check, assumes objects found are frames if they look like it.
# A more robust check could verify pixel counts match perimeter, etc.
# def is_hollow_rectangle(grid, obj_coords, bbox):
#     min_r, min_c, max_r, max_c = bbox
#     width = max_c - min_c + 1
#     height = max_r - min_r + 1
    
#     # Check perimeter pixels - are they all in obj_coords?
#     for c in range(min_c, max_c + 1):
#         if (min_r, c) not in obj_coords or (max_r, c) not in obj_coords:
#             return False
#     for r in range(min_r + 1, max_r):
#         if (r, min_c) not in obj_coords or (r, max_c) not in obj_coords:
#             return False
            
#     # Check interior pixels - are they NOT in obj_coords? (should be 0)
#     for r in range(min_r + 1, max_r):
#         for c in range(min_c + 1, max_c):
#             if (r, c) in obj_coords:
#                 return False
#             # Optional: check if interior is specifically white(0)
#             # if grid[r, c] != 0: return False 
            
#     # Check pixel count matches perimeter
#     expected_perimeter_pixels = 0
#     if width > 0 and height > 0:
#         if width == 1 and height == 1:
#              expected_perimeter_pixels = 1
#         elif width == 1:
#              expected_perimeter_pixels = height
#         elif height == 1:
#              expected_perimeter_pixels = width
#         else:
#              expected_perimeter_pixels = 2 * width + 2 * height - 4
             
#     return len(obj_coords) == expected_perimeter_pixels

def transform(input_grid):
    """
    Transforms the input grid by expanding green frames towards magenta markers.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = np.zeros_like(input_np) # Start with a blank (white) grid

    # --- Step 1: Find Magenta Markers ---
    magenta_markers = []
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] == 6:
                magenta_markers.append((r, c))

    # --- Step 2: Find Green Objects and their original BBoxes ---
    green_objects = find_objects(input_np, 3)
    original_bboxes = []
    for obj_coords in green_objects:
        bbox = get_bounding_box(obj_coords)
        if bbox:
             # Assuming found green objects are the frames as per examples
             # Add more robust check like is_hollow_rectangle if needed
            original_bboxes.append(bbox)

    # --- Step 3: Calculate New Bounding Boxes ---
    new_bboxes = []
    for min_r, min_c, max_r, max_c in original_bboxes:
        new_min_r, new_min_c, new_max_r, new_max_c = min_r, min_c, max_r, max_c

        # Find markers outside the original box and update new boundaries
        markers_above = [m_r for m_r, m_c in magenta_markers if m_r < min_r]
        markers_below = [m_r for m_r, m_c in magenta_markers if m_r > max_r]
        markers_left = [m_c for m_r, m_c in magenta_markers if m_c < min_c]
        markers_right = [m_c for m_r, m_c in magenta_markers if m_c > max_c]

        if markers_above:
            new_min_r = min(markers_above)
        if markers_below:
            new_max_r = max(markers_below)
        if markers_left:
            new_min_c = min(markers_left)
        if markers_right:
            new_max_c = max(markers_right)
            
        new_bboxes.append((new_min_r, new_min_c, new_max_r, new_max_c))

    # --- Step 4: Draw New Frames on Output Grid ---
    for r1, c1, r2, c2 in new_bboxes:
        # Ensure coordinates are within grid bounds (although expansion logic should handle this)
        r1, c1 = max(0, r1), max(0, c1)
        r2, c2 = min(rows - 1, r2), min(cols - 1, c2)

        # Draw frame border if the box has valid dimensions
        if r1 <= r2 and c1 <= c2:
            output_grid[r1, c1:c2+1] = 3  # Top border
            output_grid[r2, c1:c2+1] = 3  # Bottom border
            output_grid[r1:r2+1, c1] = 3  # Left border
            output_grid[r1:r2+1, c2] = 3  # Right border

    # --- Step 5: Redraw Magenta Markers ---
    for r, c in magenta_markers:
        # Ensure marker is within bounds before drawing
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = 6

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```