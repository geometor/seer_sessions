import numpy as np

"""
Identifies solid, monochromatic rectangular blocks (excluding white, color 0) in the input grid. 
For each identified block with both height and width greater than or equal to 3, applies a 
checkerboard pattern to its interior pixels (the area excluding the 1-pixel thick border). 
The checkerboard pattern uses white (0) and the block's original color. Specifically, 
interior pixels at absolute grid coordinates (r, c) are changed to white (0) if the sum 
of their *relative* coordinates within the interior (rel_r, rel_c) is even. The relative 
coordinates (rel_r, rel_c) are calculated starting from (0, 0) at the top-left corner 
of the interior region. Pixels where (rel_r + rel_c) is odd retain the block's original color. 
Pixels belonging to the background (white), the borders of modified blocks, blocks smaller 
than 3x3, or non-rectangular shapes remain unchanged.
"""

def find_solid_rectangles(grid):
    """
    Finds all solid, monochromatic rectangular blocks (excluding white) in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a block
              and contains 'color' (int), 'bbox' (tuple: min_r, min_c, max_r, max_c),
              'height' (int), and 'width' (int).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    for r in range(rows):
        for c in range(cols):
            # Skip background color (0) or already visited pixels
            if grid[r, c] == 0 or visited[r, c]:
                continue

            color = grid[r, c]
            
            # Find the maximum horizontal extent of the same color starting from (r, c)
            # only considering unvisited cells in this row.
            max_c_initial = c
            while max_c_initial + 1 < cols and grid[r, max_c_initial + 1] == color and not visited[r, max_c_initial + 1]:
                max_c_initial += 1
            
            initial_width = max_c_initial - c + 1
            
            # Find the maximum vertical extent, ensuring each row matches the initial width and color
            # and consists of unvisited cells.
            max_r_final = r
            valid_rectangle = True
            while max_r_final + 1 < rows:
                is_valid_row = True
                # Check if the entire row segment below matches the color and width, and is unvisited
                for col_check in range(c, c + initial_width):
                    if col_check >= cols or grid[max_r_final + 1, col_check] != color or visited[max_r_final + 1, col_check]:
                        is_valid_row = False
                        break
                
                if is_valid_row:
                    max_r_final += 1
                else:
                    break # Stop expanding downwards if the row doesn't match

            final_height = max_r_final - r + 1
            
            # Double-check: Verify that this shape wasn't already claimed by a BFS-like expansion from a higher row
            # This check is implicitly handled by the visited array and the row-by-row scan,
            # but we must ensure that the *entire* found rectangle area is indeed unvisited
            # before marking it.
            
            # Check every cell within the determined bounding box (r, c) to (max_r_final, c + initial_width - 1)
            # This also helps catch cases where the initial horizontal scan might have been too long
            # if a row below it had a shorter width of the same color starting at the same column c.
            
            # Re-determine the actual width based on consistency across all rows found
            actual_width = initial_width
            for rr_check in range(r + 1, max_r_final + 1):
                current_row_width = 0
                for cc_check in range(c, cols):
                     if grid[rr_check, cc_check] == color and not visited[rr_check, cc_check]:
                         current_row_width += 1
                     else:
                         break
                actual_width = min(actual_width, current_row_width)

            final_min_r, final_min_c = r, c
            final_max_r, final_max_c = max_r_final, c + actual_width - 1
            final_height = final_max_r - final_min_r + 1 # Recalculate height based on final bounds

            # Final verification: Ensure all cells within the *final* bounds are the correct color and unvisited
            is_solid = True
            pixels_to_visit = []
            if actual_width <= 0: # Handle cases where width determination failed
                 is_solid = False
            else:
                for rr in range(final_min_r, final_max_r + 1):
                    for cc in range(final_min_c, final_max_c + 1):
                        # Check bounds just in case, although logic should prevent out-of-bounds
                        if rr >= rows or cc >= cols or grid[rr, cc] != color or visited[rr, cc]:
                            is_solid = False
                            break
                        pixels_to_visit.append((rr, cc))
                    if not is_solid:
                        break

            # If it is a solid, unvisited rectangle, mark its pixels as visited and add to list
            if is_solid:
                for pr, pc in pixels_to_visit:
                    visited[pr, pc] = True
                blocks.append({
                    'color': color,
                    'bbox': (final_min_r, final_min_c, final_max_r, final_max_c),
                    'height': final_height,
                    'width': actual_width
                })

    return blocks


def transform(input_grid):
    """
    Applies a checkerboard pattern to the interior of solid rectangular blocks.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # 1. Identify all distinct, solid, monochromatic rectangular blocks (excluding white)
    blocks = find_solid_rectangles(input_np)

    # 2. Iterate through each identified block
    for block in blocks:
        min_r, min_c, max_r, max_c = block['bbox']
        height = block['height']
        width = block['width']
        # color = block['color'] # Original color is implicitly kept unless overwritten

        # 3. Check if the block's height and width are both >= 3
        if height >= 3 and width >= 3:
            
            # 4.a Determine the interior bounding box
            interior_min_r = min_r + 1
            interior_min_c = min_c + 1
            # The loops will go up to, but not include, max_r and max_c
            # So, the interior range is correct with range(interior_min_r, max_r) 
            # and range(interior_min_c, max_c)
            
            # 4.b Iterate through each pixel (r, c) within the interior
            for r in range(interior_min_r, max_r): 
                for c in range(interior_min_c, max_c): 
                    
                    # 4.c Calculate relative coordinates within the interior
                    rel_r = r - interior_min_r
                    rel_c = c - interior_min_c
                    
                    # 4.d & 4.e Check if the sum (rel_r + rel_c) is even and apply transformation
                    if (rel_r + rel_c) % 2 == 0:
                        # Set pixel to white (0) in the output grid
                        output_grid[r, c] = 0
                        
    # 5. Convert the result back to a list of lists format and return
    return output_grid.tolist()