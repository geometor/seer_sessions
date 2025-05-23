import numpy as np
from collections import deque

"""
Identifies rectangular regions enclosed by single-color frames within the input grid.
Sorts these regions based on their top-left corner (row, then column).
Extracts the subgrid corresponding to the bounding box (including the frame) of the second identified region.
"""

def _find_connected_components(grid, target_color):
    """
    Finds all connected components of a specific color in the grid using BFS.
    Args:
        grid (np.array): The input grid.
        target_color (int): The color to find components of.
    Returns:
        list: A list of dictionaries, each representing a component with
              'pixels' (a set of (row, col) tuples) and
              'bbox' (min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find a pixel of the target color that hasn't been visited
            if grid[r, c] == target_color and not visited[r, c]:
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    # Update bounding box coordinates
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the component information
                components.append({
                    'pixels': set(component_pixels),
                    'bbox': (min_r, min_c, max_r, max_c),
                    'color': target_color
                })
    return components

def _find_framed_rectangles(grid):
    """
    Identifies all rectangular regions enclosed by a single-color frame.
    Args:
        grid (np.array): The input grid.
    Returns:
        list: A list of bounding boxes (r1, c1, r2, c2) for the identified
              framed rectangles, sorted by top-left corner (row, then column).
    """
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    all_components = []
    # Find components for every color present in the grid
    for color in unique_colors:
        all_components.extend(_find_connected_components(grid, color))

    framed_rectangles_data = [] # Store tuples: (bbox, frame_color)

    # Analyze each component to see if it forms a valid frame
    for comp in all_components:
        min_r, min_c, max_r, max_c = comp['bbox']
        pixels = comp['pixels']
        frame_color = comp['color']

        # A frame must have a minimum bounding box size of 2x2 to enclose an interior
        if max_r - min_r < 1 or max_c - min_c < 1:
            continue

        is_valid_frame = True
        # Condition 1: All pixels of the component must lie exactly on the perimeter of its bounding box.
        for r_pix, c_pix in pixels:
            is_on_border = (r_pix == min_r or r_pix == max_r or
                            c_pix == min_c or c_pix == max_c)
            if not is_on_border:
                is_valid_frame = False
                break
        if not is_valid_frame: continue

        # Condition 2: All cells on the perimeter of the bounding box must belong to the component.
        # Check top/bottom rows of the bounding box
        for c in range(min_c, max_c + 1):
             if (min_r, c) not in pixels or (max_r, c) not in pixels:
                  is_valid_frame = False; break
        if not is_valid_frame: continue
        # Check left/right columns of the bounding box (excluding corners already checked)
        for r in range(min_r + 1, max_r):
             if (r, min_c) not in pixels or (r, max_c) not in pixels:
                  is_valid_frame = False; break
        if not is_valid_frame: continue

        # Condition 3: The interior area must exist and must not contain any pixels of the frame's color.
        has_interior = False
        interior_is_clear = True
        # Iterate through the cells strictly inside the bounding box
        for r in range(min_r + 1, max_r):
            for c in range(min_c + 1, max_c):
                has_interior = True # Mark that an interior exists
                if grid[r, c] == frame_color:
                    interior_is_clear = False # Found frame color inside
                    break
            if not interior_is_clear: break # Stop checking interior if violation found

        # If all conditions are met, it's a valid framed rectangle
        if is_valid_frame and has_interior and interior_is_clear:
            framed_rectangles_data.append(((min_r, min_c, max_r, max_c), frame_color))

    # Sort the identified frames primarily by top row, secondarily by leftmost column
    framed_rectangles_data.sort(key=lambda item: (item[0][0], item[0][1]))

    # Return only the bounding boxes in sorted order
    return [box for box, color in framed_rectangles_data]


def transform(input_grid):
    """
    Identifies rectangular regions enclosed by single-color frames within the input grid.
    Sorts these regions based on their top-left corner (row, then column).
    Extracts the subgrid corresponding to the bounding box (including the frame) of the second identified region.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Find all framed rectangles, sorted by position (top-left corner)
    framed_rect_bboxes = _find_framed_rectangles(input_array)

    # Check if at least two framed rectangles were found
    if len(framed_rect_bboxes) < 2:
        # If fewer than two frames are found, the rule cannot be applied as described.
        # Behavior in this edge case isn't specified; raising an error or returning
        # a default (like empty list or original grid) are options.
        # Here, we'll raise an IndexError implicitly if we try to access index 1.
        # Consider adding explicit error handling if needed.
        print(f"Warning: Found {len(framed_rect_bboxes)} framed rectangles, expected at least 2.")
        # Or return input_grid or [] depending on desired behavior for non-applicable cases
        if not framed_rect_bboxes: return [] # Return empty list if none found
        # If only one found, the task description for the *second* cannot be met.
        # Let's cause an error to signal the condition isn't met.
        # Fallthrough will cause IndexError below if len < 2


    # Select the bounding box of the second rectangle (index 1 in the sorted list)
    r1, c1, r2, c2 = framed_rect_bboxes[1]

    # Extract the subgrid defined by the bounding box (inclusive slicing)
    # Numpy slicing is exclusive of the end index, so add 1 to r2 and c2
    output_array = input_array[r1 : r2 + 1, c1 : c2 + 1]

    # Convert the resulting numpy array back to a list of lists format
    output_grid = output_array.tolist()

    return output_grid