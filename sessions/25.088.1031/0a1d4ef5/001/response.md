```python
import numpy as np
from collections import defaultdict
import math

"""
Identifies maximal, solid, monochromatic rectangular blocks (excluding white/0) in the input grid.
Calculates the center of each block.
Groups blocks into rows based on similar center y-coordinates.
Sorts the rows from top to bottom based on their average center y-coordinate.
Sorts the blocks within each row from left to right based on their center x-coordinate.
Constructs an output grid where each cell contains the color of a block, arranged according to the sorted row and column structure.
"""

def find_maximal_solid_rectangles(grid):
    """
    Finds all maximal solid monochromatic rectangles in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each containing info about a found rectangle:
              {'color': int, 'bounds': (min_r, min_c, max_r, max_c), 'center': (center_y, center_x)}
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if the pixel is not background and not visited
            if color != background_color and not visited[r, c]:
                # Start BFS to find the connected component
                q = [(r, c)]
                visited[r, c] = True
                component_pixels = [(r, c)]
                min_r, max_r = r, r
                min_c, max_c = c, c

                head = 0
                while head < len(q):
                    curr_r, curr_c = q[head]
                    head += 1

                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_pixels.append((nr, nc))
                
                # Check if the component forms a solid rectangle
                rect_rows = max_r - min_r + 1
                rect_cols = max_c - min_c + 1
                is_solid_rectangle = True
                if len(component_pixels) != rect_rows * rect_cols:
                    # If pixel count doesn't match bounding box area, not a solid rect
                    is_solid_rectangle = False
                else:
                    # Verify all pixels within the bounding box have the same color
                    for rr in range(min_r, max_r + 1):
                        for cc in range(min_c, max_c + 1):
                            if grid[rr, cc] != color:
                                is_solid_rectangle = False
                                break
                        if not is_solid_rectangle:
                            break
                
                # If it's a solid rectangle, store its properties
                if is_solid_rectangle:
                    center_y = min_r + (rect_rows - 1) / 2.0
                    center_x = min_c + (rect_cols - 1) / 2.0
                    rectangles.append({
                        'color': color,
                        'bounds': (min_r, min_c, max_r, max_c),
                        'center': (center_y, center_x)
                    })
                    # Mark all pixels within the verified rectangle bounds as visited
                    # This handles cases where BFS might not cover the entire conceptual rectangle
                    # if the shape is unusual initially but fits a rect bbox. Redundant marking is fine.
                    for rr in range(min_r, max_r + 1):
                        for cc in range(min_c, max_c + 1):
                           visited[rr, cc] = True


    return rectangles


def group_and_sort_rectangles(rectangles):
    """
    Groups rectangles into rows based on center y-coordinate and sorts them.

    Args:
        rectangles (list): List of rectangle dictionaries.

    Returns:
        list: A list of lists, where each inner list represents a row
              of rectangle colors, sorted top-to-bottom and left-to-right.
    """
    if not rectangles:
        return []

    # Sort primarily by center y, then by center x
    rectangles.sort(key=lambda r: (r['center'][0], r['center'][1]))

    rows_of_rects = []
    current_row = []
    if rectangles:
        current_row.append(rectangles[0])

    # Group by similar center y (using a small tolerance or comparing to the first element of the row)
    # A simple approach: if y-center is 'close enough' to the first rect in the current row, add it.
    y_tolerance = 1.0 # Allow for slight vertical variations within a row

    for i in range(1, len(rectangles)):
        rect = rectangles[i]
        first_rect_in_row = current_row[0]
        # Check if the current rectangle's y-center is close to the first rectangle's y-center in the current row
        if abs(rect['center'][0] - first_rect_in_row['center'][0]) <= y_tolerance:
            current_row.append(rect)
        else:
            # Start a new row
            # Sort the completed row by x-coordinate before adding
            current_row.sort(key=lambda r: r['center'][1])
            rows_of_rects.append(current_row)
            current_row = [rect]

    # Add the last row after sorting it
    if current_row:
        current_row.sort(key=lambda r: r['center'][1])
        rows_of_rects.append(current_row)

    # Extract colors
    output_rows = []
    for row in rows_of_rects:
        output_rows.append([rect['color'] for rect in row])

    return output_rows


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by finding solid rectangular blocks,
    arranging them by row and column based on their spatial positions,
    and outputting a grid of their colors.
    """
    # 1. Find all maximal solid rectangular blocks (non-background)
    rectangles = find_maximal_solid_rectangles(input_grid)

    # 2. Group rectangles into rows (based on y-center) and sort
    #    - Rows are sorted top-to-bottom (implicitly by sorting rects first)
    #    - Rectangles within rows are sorted left-to-right (based on x-center)
    grouped_sorted_colors = group_and_sort_rectangles(rectangles)

    # 3. Construct the output grid
    if not grouped_sorted_colors:
        return np.array([[]], dtype=int) # Return empty grid if no rects found

    num_rows = len(grouped_sorted_colors)
    # Ensure all rows have the same length for a rectangular output grid.
    # This task's examples suggest rows can have different lengths, 
    # which numpy arrays don't directly support without padding or object dtype.
    # Let's assume the task implies a rectangular output matching the structure.
    # The examples show rectangular outputs, implying consistent columns per task.
    num_cols = 0
    if num_rows > 0:
        num_cols = len(grouped_sorted_colors[0]) # Assume consistent columns based on first row
        # Verify assumption (optional, but good practice)
        # for row in grouped_sorted_colors:
        #     if len(row) != num_cols:
        #         # Handle inconsistency if needed, maybe pad or raise error
        #         print(f"Warning: Inconsistent number of columns found. {len(row)} vs {num_cols}")
        #         # For now, let's trust the examples imply rectangular structure
        #         pass


    # Create the output grid
    output_grid = np.zeros((num_rows, num_cols), dtype=int)
    for r_idx, row_colors in enumerate(grouped_sorted_colors):
         # Ensure the row length matches expected columns before assignment
        if len(row_colors) == num_cols:
            output_grid[r_idx, :] = row_colors
        else:
             # Handle potential inconsistencies, e.g., pad or truncate if necessary
             # For this task, seems safe to assume consistency based on examples
             print(f"Error: Row {r_idx} has {len(row_colors)} columns, expected {num_cols}")
             # Fallback: Pad with a default value (like 0) or truncate
             padded_row = row_colors[:num_cols] + [0] * (num_cols - len(row_colors))
             output_grid[r_idx, :] = padded_row


    return output_grid
```