import numpy as np

"""
Identifies two non-white colors: C1 (forming the largest contiguous object) and C2 (forming a crosshair).
Finds the bounding box of the largest C1 object and the center of the C2 crosshair in the input.
Calculates a shift 'S' based on half the width of the C1 object's bounding box.
Determines a target row (original center row - S) and target column (original center column + S).
Constructs an output grid containing only the largest C1 object initially.
Draws a new horizontal line of color C2 at the target row, excluding the horizontal span of the C1 bounding box.
Draws a new vertical line of color C2 at the target column, excluding the vertical span of the C1 bounding box.
"""

# Helper function to find contiguous objects (using only cardinal neighbors)
def find_contiguous_objects(grid, color):
    """Finds all contiguous objects of a specific color using BFS (4-connectivity)."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    q = [] # Use list as deque

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = set()
                q.append((r, c))
                visited[r, c] = True
                obj_pixels.add((r, c))

                head = 0
                while head < len(q):
                    row, col = q[head]
                    head += 1
                    # Von Neumann neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            obj_pixels.add((nr, nc))
                if obj_pixels:
                    objects.append(obj_pixels)
                q = [] # Reset queue for next potential object
    return objects

# Helper function to identify colors and the largest C1 object
def find_colors_and_c1_object(grid):
    """Identifies C1 (largest object color), C2 (other color), and the specific C1 object pixels."""
    unique_colors = np.unique(grid)
    non_white_colors = unique_colors[unique_colors != 0]

    if len(non_white_colors) == 0:
        return -1, -1, set() # No non-white colors
    
    c1 = -1
    c1_object = set()
    c2 = -1
    max_obj_size = -1

    # Find the color with the largest single contiguous object
    found_objects_for_color = {}
    for color in non_white_colors:
        objects = find_contiguous_objects(grid, int(color)) # Ensure color is int
        if objects:
            found_objects_for_color[int(color)] = objects
            largest_obj_for_color = max(objects, key=len)
            if len(largest_obj_for_color) > max_obj_size:
                max_obj_size = len(largest_obj_for_color)
                c1 = int(color)
                c1_object = largest_obj_for_color

    # Handle cases where no object found or tie-breaking needed (fallback to frequency)
    if c1 == -1:
         if len(non_white_colors) > 0:
             counts = {int(color): np.sum(grid == color) for color in non_white_colors}
             c1 = max(counts, key=counts.get)
             # Need to find the largest object for this chosen C1 again
             objects = find_contiguous_objects(grid, c1)
             if objects:
                 c1_object = max(objects, key=len)
             else: # Should not happen if counts > 0 but safety check
                 return -1, -1, set()
         else: # Should already be handled by the initial check
             return -1, -1, set()


    # Assign C2
    if len(non_white_colors) > 1:
        for color in non_white_colors:
            if int(color) != c1:
                c2 = int(color)
                break
    # If only one non-white color, C2 remains -1

    return c1, c2, c1_object

# Helper function to find bounding box from pixels
def find_bounding_box_from_pixels(pixels):
    """Finds the bounding box of a given set of pixels."""
    if not pixels:
        return -1, -1, -1, -1, 0, 0
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    width = max_col - min_col + 1
    height = max_row - min_row + 1
    return min_row, max_row, min_col, max_col, width, height

# Helper function to find the 'center' of the C2 crosshair
def find_crosshair_center(grid, color):
    """Finds the row and column with the most pixels of the crosshair color."""
    if color == -1 or np.sum(grid == color) == 0:
        return -1, -1 # Color not present or invalid
        
    rows, cols = grid.shape
    center_row = -1
    row_counts = np.sum(grid == color, axis=1)
    if np.any(row_counts > 0):
         # Find the index (row) with the maximum count
         max_row_count = np.max(row_counts)
         # Find the first row index that has this max count
         center_row = np.where(row_counts == max_row_count)[0][0]


    center_col = -1
    col_counts = np.sum(grid == color, axis=0)
    if np.any(col_counts > 0):
        # Find the index (col) with the maximum count
        max_col_count = np.max(col_counts)
        # Find the first col index that has this max count
        center_col = np.where(col_counts == max_col_count)[0][0]

    # If somehow only horizontal or vertical line exists, one might still be -1
    # The calling code needs to handle potentially invalid center coords

    return center_row, center_col


def transform(input_grid):
    """
    Transforms the input grid by keeping the largest object (C1), removing the
    original crosshair (C2), and drawing a new crosshair shifted based on C1's width.
    """
    input_np = np.array(input_grid)
    rows, cols = input_np.shape

    # 1. Identify Colors and Main Shape
    c1, c2, c1_object_pixels = find_colors_and_c1_object(input_np)

    # If no main shape found, return empty or input? Return empty for now.
    if c1 == -1 or not c1_object_pixels:
        return np.zeros_like(input_np).tolist()

    # 2. Analyze Shape C1
    min_r, max_r, min_c, max_c, width, height = find_bounding_box_from_pixels(c1_object_pixels)

    # 3. Analyze Original Crosshair (Color C2)
    center_r, center_c = -1, -1
    if c2 != -1:
        center_r, center_c = find_crosshair_center(input_np, c2)
        # If C2 exists but doesn't form a clear crosshair center, drawing logic will skip

    # 4. Calculate Shift and Target Lines
    shift_s = width // 2
    target_r = -1
    target_c = -1
    can_draw_c2 = (c2 != -1 and center_r != -1 and center_c != -1)

    if can_draw_c2:
        target_r = center_r - shift_s
        target_c = center_c + shift_s

    # 5. Construct Output Grid
    # Start with a white grid
    output_grid = np.zeros_like(input_np)

    # Copy C1 shape pixels
    for r, c in c1_object_pixels:
        if 0 <= r < rows and 0 <= c < cols: # Bounds check (should be inherent)
             output_grid[r, c] = c1

    # Draw new C2 lines only if C2 and its center were validly found
    if can_draw_c2:
        # Draw horizontal line at target_r, outside C1's horizontal span
        if 0 <= target_r < rows: # Check if target row is valid
            for c in range(cols):
                is_inside_c1_horizontal_span = (min_c <= c <= max_c)
                if not is_inside_c1_horizontal_span:
                    output_grid[target_r, c] = c2

        # Draw vertical line at target_c, outside C1's vertical span
        if 0 <= target_c < cols: # Check if target col is valid
            for r in range(rows):
                is_inside_c1_vertical_span = (min_r <= r <= max_r)
                if not is_inside_c1_vertical_span:
                    output_grid[r, target_c] = c2

    # 6. Return the final grid as a list of lists
    return output_grid.tolist()