import numpy as np
from collections import deque

"""
Identifies distinct non-white objects in the input grid.
Determines a color mapping from special marker pairs (horizontal non-white pixels) 
typically found in the bottom-left corner (columns 0 and 1): the color in column 0
maps to the color in column 1.
For each object found:
  Calculates its minimal bounding box.
  Finds the target fill color using the object's color and the derived color mapping.
  Fills all white (0) pixels within the object's minimal bounding box in the 
  output grid with the target fill color.
  Preserves the original non-white pixels of the object.
The background outside any object's bounding box remains white. Pixels belonging
to objects whose color does not appear as a key in the marker pairs are left
untouched, and their bounding boxes are not filled.
"""

def find_marker_pairs(grid):
    """
    Finds horizontal marker pairs in the bottom-left corner (cols 0 and 1)
    and returns a dictionary mapping left_color -> right_color.
    It iterates from the bottom row upwards.
    """
    color_map = {}
    height, width = grid.shape

    # Only proceed if there are at least 2 columns for horizontal pairs
    if width < 2:
        return color_map

    # Search columns 0 and 1, from bottom row up
    for r in range(height - 1, -1, -1): # Iterate from bottom row (height-1) up to 0
        left_color = grid[r, 0]
        right_color = grid[r, 1]

        # Check if both are non-white (not 0)
        if left_color != 0 and right_color != 0:
            # If this left_color hasn't been mapped yet, add the mapping
            if left_color not in color_map:
                color_map[left_color] = right_color
                # print(f"Found marker pair at row {r}: {left_color} -> {right_color}")

    # print(f"Derived color map: {color_map}")
    return color_map

def find_objects_and_fill(input_grid, color_map):
    """
    Finds all non-white objects, calculates their bounding boxes,
    and fills the background (white pixels) within those boxes according 
    to the color_map. Objects whose colors are not keys in the color_map
    are ignored for filling purposes.
    Returns the modified grid.
    """
    height, width = input_grid.shape
    # Start with a copy of the input grid
    output_grid = np.copy(input_grid) 
    visited = np.zeros_like(input_grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            # If pixel is non-white and not yet visited (part of a found object)
            if input_grid[r, c] != 0 and not visited[r, c]:
                object_color = input_grid[r, c]
                
                # Check if this object's color has a mapping defined in the markers
                if object_color not in color_map:
                    # If no mapping exists, we still need to mark all parts of this object
                    # as visited so we don't process them again, but we won't fill its bbox.
                    q_skip = deque([(r, c)])
                    while q_skip:
                        row_s, col_s = q_skip.popleft()
                        if not (0 <= row_s < height and 0 <= col_s < width) or \
                           visited[row_s, col_s] or \
                           input_grid[row_s, col_s] != object_color:
                            continue
                        visited[row_s, col_s] = True
                        # Add neighbors for BFS
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                             q_skip.append((row_s + dr, col_s + dc))
                    # print(f"Skipping object color {object_color} starting at ({r},{c}) - no mapping found.")
                    continue # Move to the next pixel in the grid scan

                # If a mapping exists, proceed to find the object and fill its bbox
                fill_color = color_map[object_color]
                object_coords = set()
                q = deque([(r, c)])
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Perform BFS to find all connected pixels of the same object_color
                while q:
                    row, col = q.popleft()

                    # Bounds check, color check, visited check
                    if not (0 <= row < height and 0 <= col < width) or \
                       visited[row, col] or \
                       input_grid[row, col] != object_color:
                        continue

                    visited[row, col] = True
                    object_coords.add((row, col))

                    # Update bounding box coordinates
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Add neighbors to queue for continuing the BFS
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        q.append((nr, nc))

                # Now fill the bounding box in the output grid
                # print(f"Found object color {object_color} at ({r},{c}). BBox: ({min_r}-{max_r}, {min_c}-{max_c}). Fill background with {fill_color}")
                for br in range(min_r, max_r + 1):
                    for bc in range(min_c, max_c + 1):
                        # Only fill if the original pixel in the input grid was white (0)
                        # This preserves the original object pixels within the bbox
                        if input_grid[br, bc] == 0:
                            output_grid[br, bc] = fill_color
                        # Else (if input_grid[br, bc] != 0), do nothing, preserving the object pixel

    return output_grid


def transform(input_grid):
    """
    Transforms the input grid by:
    1. Finding color mappings from horizontal marker pairs in the bottom-left corner.
    2. Identifying all distinct non-white objects.
    3. For each object whose color has a mapping, determining its minimal bounding box.
    4. Filling the white background pixels within that bounding box with the mapped color.
    5. Preserving the original object pixels.
    """
    # Convert list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Step 1: Find the color mapping from horizontal marker pairs
    color_map = find_marker_pairs(input_np)

    # Step 2: Find objects and fill their bounding box backgrounds based on the map
    output_np = find_objects_and_fill(input_np, color_map)

    # Convert back to list of lists for the expected output format
    return output_np.tolist()