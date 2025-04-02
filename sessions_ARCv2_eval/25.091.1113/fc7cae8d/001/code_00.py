import numpy as np

"""
Identify the largest contiguous rectangular block composed of a single non-background (non-white, non-0) color in the input grid. This rectangle serves as a bounding frame. Extract the subgrid located strictly inside this bounding frame (excluding the frame's border pixels). The extracted subgrid is the output.
"""

def find_colored_rectangles(grid):
    """
    Finds all maximal contiguous rectangular blocks of a single color (excluding color 0).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a rectangle
              and contains 'color', 'top', 'left', 'bottom', 'right', and 'area'.
              Returns an empty list if no such rectangles are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                q = [(r, c)]
                visited[r, c] = True
                coords = [(r, c)]
                min_r, max_r = r, r
                min_c, max_c = c, c

                # BFS to find all connected cells of the same color
                head = 0
                while head < len(q):
                    curr_r, curr_c = q[head]
                    head += 1

                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            coords.append((nr, nc))

                # Check if the found shape is a solid rectangle
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                is_rectangle = True
                if len(coords) != height * width:
                    is_rectangle = False
                else:
                    # Double-check all cells within the bounds match the color
                    for check_r in range(min_r, max_r + 1):
                        for check_c in range(min_c, max_c + 1):
                            if grid[check_r, check_c] != color:
                                is_rectangle = False
                                break
                        if not is_rectangle:
                            break
                
                # Reset visited status for non-rectangular shapes within the bounding box
                # This is important if a non-rectangular shape was initially explored
                if not is_rectangle:
                     for cr, cc in coords:
                         # Check if the cell truly belongs only to this failed exploration
                         # A simple reset might be incorrect if cells were shared by overlapping checks
                         # A safer approach might involve more complex region tracking, but let's try resetting
                         # if it doesn't form the calculated bounding box.
                         # This BFS finds connected components. If it's not a rect, we just discard it.
                         # The cells will be revisited if they are part of *another* starting point's component.
                         # So, no need to reset visited status here. The `visited` prevents re-starting BFS
                         # from within an already explored component.
                         pass # No reset needed based on BFS logic


                if is_rectangle:
                    rectangles.append({
                        'color': color,
                        'top': min_r,
                        'left': min_c,
                        'bottom': max_r,
                        'right': max_c,
                        'area': height * width
                    })

    return rectangles


def transform(input_grid):
    """
    Transforms the input grid by finding the largest non-background colored rectangle
    and extracting the content strictly inside it.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the output grid, which is the
                   subgrid inside the largest identified rectangle. Returns an empty
                   grid if no suitable rectangle is found or if the inner region
                   has zero height or width.
    """
    input_grid_np = np.array(input_grid)

    # 1. Find all non-background (non-0) colored rectangles
    rectangles = find_colored_rectangles(input_grid_np)

    # Handle case where no rectangles are found
    if not rectangles:
        # Return empty or default based on potential ARC conventions
        # For now, returning an empty 0x0 grid
        return np.array([[]], dtype=input_grid_np.dtype)

    # 2. Find the rectangle with the largest area
    largest_rect = max(rectangles, key=lambda r: r['area'])

    # 3. Define the inner bounds (excluding the frame)
    inner_top = largest_rect['top'] + 1
    inner_left = largest_rect['left'] + 1
    inner_bottom = largest_rect['bottom'] - 1
    inner_right = largest_rect['right'] - 1

    # 4. Check if the inner bounds are valid (positive height and width)
    if inner_top > inner_bottom or inner_left > inner_right:
        # The frame is too thin (1 pixel wide/high) or invalid
        return np.array([[]], dtype=input_grid_np.dtype) # Return empty grid

    # 5. Extract the subgrid corresponding to the inner area
    output_grid = input_grid_np[inner_top : inner_bottom + 1, inner_left : inner_right + 1]

    return output_grid