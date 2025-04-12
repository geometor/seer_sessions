import copy

"""
Move a single pixel towards a boundary line until adjacent.

The transformation identifies a single 'moving' pixel and a 'boundary' line 
(a horizontal or vertical line of a single color along one edge of the grid).
The moving pixel is moved in a straight line, perpendicular to the boundary, 
until it reaches the position immediately adjacent to the boundary line. 
The background color is assumed to be 0 (white).
"""

def find_boundary_line(grid: list[list[int]]) -> tuple[int, str, int] | None:
    """
    Finds the boundary line in the grid.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing (color, orientation, index) if found, else None.
        orientation is 'h' for horizontal, 'v' for vertical.
        index is the row index for 'h' or column index for 'v'.
    """
    height = len(grid)
    width = len(grid[0])
    background_color = 0 # Assuming white background

    # Check top edge (horizontal)
    first_pixel_color = grid[0][0]
    if first_pixel_color != background_color and all(grid[0][j] == first_pixel_color for j in range(width)):
        return first_pixel_color, 'h', 0

    # Check bottom edge (horizontal)
    first_pixel_color = grid[height - 1][0]
    if first_pixel_color != background_color and all(grid[height - 1][j] == first_pixel_color for j in range(width)):
        return first_pixel_color, 'h', height - 1

    # Check left edge (vertical)
    first_pixel_color = grid[0][0]
    if first_pixel_color != background_color and all(grid[i][0] == first_pixel_color for i in range(height)):
        # Check if top edge wasn't already identified as the boundary
        top_edge_color = grid[0][0]
        is_top_edge_boundary = top_edge_color != background_color and all(grid[0][j] == top_edge_color for j in range(width))
        if not is_top_edge_boundary:
             return first_pixel_color, 'v', 0
        # Need to be careful here - if the top-left corner belongs to both a horizontal and vertical line.
        # Let's refine: Find the *predominant* line color on the edge.

    # Check right edge (vertical)
    first_pixel_color = grid[0][width - 1]
    if first_pixel_color != background_color and all(grid[i][width - 1] == first_pixel_color for i in range(height)):
         return first_pixel_color, 'v', width - 1

    # Refined edge check - handle corners and partial lines more explicitly
    # Scan edges again, prioritizing full lines
    
    # Top edge
    if grid[0][0] != background_color and all(grid[0][j] == grid[0][0] for j in range(width)):
        return grid[0][0], 'h', 0
    # Bottom edge
    if grid[height-1][0] != background_color and all(grid[height-1][j] == grid[height-1][0] for j in range(width)):
        return grid[height-1][0], 'h', height - 1
    # Left edge
    if grid[0][0] != background_color and all(grid[i][0] == grid[0][0] for i in range(height)):
         # Avoid conflict if top-left is part of horizontal boundary already checked
         is_top_boundary = grid[0][0] != background_color and all(grid[0][j] == grid[0][0] for j in range(width))
         if not is_top_boundary:
            return grid[0][0], 'v', 0
    # Right edge
    if grid[0][width-1] != background_color and all(grid[i][width-1] == grid[0][width-1] for i in range(height)):
        # Avoid conflict if top-right is part of horizontal boundary
        is_top_boundary = grid[0][0] != background_color and all(grid[0][j] == grid[0][0] for j in range(width))
        # This check isn't quite right. Let's check if the pixel grid[0][width-1] could belong to the top boundary
        top_boundary_color_if_exists = grid[0][0] if is_top_boundary else -1 # Use -1 if no top boundary
        if not (is_top_boundary and grid[0][width-1] == top_boundary_color_if_exists) :
             return grid[0][width-1], 'v', width - 1

    # If full lines weren't found (e.g. example 1), check again allowing variations,
    # or maybe rethink the definition based on examples.
    # Example 1: Vertical line at col 9, color 4.
    # Example 2: Horizontal line at row 0, color 3.

    # Let's find the most frequent non-background color on each edge.
    edge_candidates = []
    # Top
    colors = [grid[0][j] for j in range(width) if grid[0][j] != background_color]
    if colors:
        top_color = max(set(colors), key=colors.count)
        if all(c == top_color or c == background_color for c in grid[0]): # Allow background gaps
             edge_candidates.append({'color': top_color, 'orientation': 'h', 'index': 0, 'count': colors.count(top_color)})
             
    # Bottom
    colors = [grid[height-1][j] for j in range(width) if grid[height-1][j] != background_color]
    if colors:
        bottom_color = max(set(colors), key=colors.count)
        if all(c == bottom_color or c == background_color for c in grid[height-1]):
             edge_candidates.append({'color': bottom_color, 'orientation': 'h', 'index': height - 1, 'count': colors.count(bottom_color)})
             
    # Left
    colors = [grid[i][0] for i in range(height) if grid[i][0] != background_color]
    if colors:
        left_color = max(set(colors), key=colors.count)
        if all(c == left_color or c == background_color for c in [grid[i][0] for i in range(height)]):
             edge_candidates.append({'color': left_color, 'orientation': 'v', 'index': 0, 'count': colors.count(left_color)})
             
    # Right
    colors = [grid[i][width-1] for i in range(height) if grid[i][width-1] != background_color]
    if colors:
        right_color = max(set(colors), key=colors.count)
        if all(c == right_color or c == background_color for c in [grid[i][width-1] for i in range(height)]):
             edge_candidates.append({'color': right_color, 'orientation': 'v', 'index': width - 1, 'count': colors.count(right_color)})
             
    # Choose the candidate with the most pixels (longest line)
    if edge_candidates:
        best_candidate = max(edge_candidates, key=lambda x: x['count'])
        return best_candidate['color'], best_candidate['orientation'], best_candidate['index']
        
    return None # No clear boundary line found


def find_moving_pixel(grid: list[list[int]], boundary_color: int) -> tuple[int, int, int] | None:
    """
    Finds the single moving pixel (not background and not boundary color).

    Args:
        grid: The input grid.
        boundary_color: The color of the boundary line.

    Returns:
        A tuple containing (color, row, column) if found, else None.
    """
    height = len(grid)
    width = len(grid[0])
    background_color = 0 # Assuming white background
    moving_pixel = None
    count = 0

    for r in range(height):
        for c in range(width):
            pixel_color = grid[r][c]
            if pixel_color != background_color and pixel_color != boundary_color:
                # Check if this pixel is part of the boundary line even if color matches? No, boundary is on edge.
                moving_pixel = (pixel_color, r, c)
                count += 1

    # Expect exactly one moving pixel
    if count == 1:
        return moving_pixel
    else:
        # Handle cases with zero or multiple potential movers if needed,
        # but based on examples, expect exactly one.
        # print(f"Warning: Found {count} potential moving pixels.")
        return None


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Moves a single colored pixel towards a static boundary line along an edge 
    until it is immediately adjacent to the boundary. The movement is perpendicular 
    to the boundary line.
    """
    # Initialize output_grid as a copy of the input
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])
    background_color = 0 # Assuming white background

    # 1. Identify the boundary line
    boundary_info = find_boundary_line(output_grid)
    if boundary_info is None:
        # print("Error: Boundary line not found.")
        return output_grid # Return original grid if no boundary found
    boundary_color, boundary_orientation, boundary_index = boundary_info
    
    # 2. Identify the moving pixel
    mover_info = find_moving_pixel(output_grid, boundary_color)
    if mover_info is None:
        # print("Error: Moving pixel not found or ambiguous.")
        return output_grid # Return original grid if no mover found
    mover_color, original_row, original_col = mover_info

    # 3. Erase the moving pixel from its original position
    output_grid[original_row][original_col] = background_color

    # 4. Determine the target position
    target_row, target_col = original_row, original_col # Initialize

    if boundary_orientation == 'h': # Horizontal boundary
        # Mover moves vertically
        target_col = original_col # Column stays the same
        if boundary_index == 0: # Top boundary
            target_row = boundary_index + 1
        elif boundary_index == height - 1: # Bottom boundary
             target_row = boundary_index - 1
        else: # Should not happen based on find_boundary_line logic
            # print("Error: Horizontal boundary not at top or bottom edge?")
            return output_grid 
            
    elif boundary_orientation == 'v': # Vertical boundary
        # Mover moves horizontally
        target_row = original_row # Row stays the same
        if boundary_index == 0: # Left boundary
            target_col = boundary_index + 1
        elif boundary_index == width - 1: # Right boundary
             target_col = boundary_index - 1
        else: # Should not happen
             # print("Error: Vertical boundary not at left or right edge?")
             return output_grid

    # 5. Place the moving pixel at the target position
    # Ensure target position is within bounds (should be guaranteed by logic)
    if 0 <= target_row < height and 0 <= target_col < width:
        output_grid[target_row][target_col] = mover_color
    else:
        # print(f"Error: Calculated target position ({target_row}, {target_col}) is out of bounds.")
        # Revert the erase operation? Or return partially modified grid?
        # Let's revert for safety, although this indicates a logic flaw.
        output_grid[original_row][original_col] = mover_color # Put it back
        return output_grid


    return output_grid