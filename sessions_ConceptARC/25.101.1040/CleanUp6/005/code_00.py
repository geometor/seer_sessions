import collections
import copy

"""
Transform the input grid based on the following rules:

1. Analyze the input grid to identify all non-background colors (pixels with value > 0) and count their occurrences.
2. If there are two or more non-background colors:
    a. Designate the color with the highest count as the 'primary color' (P). If there's a tie in counts, the color with the lower numerical value is P.
    b. Designate the color with the lowest count as the 'secondary color' (S). If there's a tie in counts, the color with the higher numerical value is S. (This assumes exactly two non-background colors based on examples).
3. If there is only one non-background color, designate it as the primary color (P), and there is no secondary color (S).
4. If there are no non-background colors, the output is identical to the input (all background).
5. Create a new output grid of the same dimensions as the input grid, initialized entirely with the background color (white, 0).
6. Iterate through each cell `(r, c)` of the input grid:
    a. If the input cell color is the primary color (P):
        i. Check its eight neighbors (including diagonals) in the input grid.
        ii. Count how many neighbors are also the primary color (P).
        iii. If this count is 1 or more (i.e., the pixel is not isolated), set the output cell `(r, c)` to P.
    b. If the input cell color is the secondary color (S) (only applicable if S was defined):
        i. Check its four cardinal neighbors (up, down, left, right) in the input grid.
        ii. Count how many of these cardinal neighbors are the primary color (P).
        iii. If this count is 2 or more, set the output cell `(r, c)` to the primary color (P).
    c. (Implicitly) If the input cell is background (0), an isolated P pixel (neighbor count = 0), or an S pixel not meeting the conversion condition (neighbor count < 2), the output cell `(r, c)` remains background (0).
7. Return the completed output grid.
"""

def get_neighbor_coords(r, c, height, width, connectivity=8):
    """
    Yields valid coordinates of neighbors for a cell (r, c) within grid bounds.
    
    Args:
        r: Row index of the cell.
        c: Column index of the cell.
        height: Grid height.
        width: Grid width.
        connectivity: 8 for diagonal neighbors, 4 for cardinal neighbors.
    """
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            # Skip diagonals if connectivity is 4 (cardinal)
            if connectivity == 4 and abs(dr) + abs(dc) != 1:
                continue
                
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                yield nr, nc

def count_neighbor_color(grid, r, c, target_color, connectivity=8):
    """
    Counts the number of neighbors of a specific color around cell (r, c).
    
    Args:
        grid: The input grid (list of lists).
        r: Row index of the cell.
        c: Column index of the cell.
        target_color: The color value to count in the neighborhood.
        connectivity: 8 for diagonal neighbors, 4 for cardinal neighbors.
        
    Returns:
        The count of neighbors with the target_color.
    """
    count = 0
    height = len(grid)
    width = len(grid[0])
    for nr, nc in get_neighbor_coords(r, c, height, width, connectivity):
        if grid[nr][nc] == target_color:
            count += 1
    return count

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation rules to the input grid.
    """
    height = len(input_grid)
    width = len(input_grid[0])

    # Step 1 & 2: Identify non-background colors and their counts.
    color_counts = collections.Counter()
    for r in range(height):
        for c in range(width):
            color = input_grid[r][c]
            if color != 0: # Ignore background
                color_counts[color] += 1

    # Step 2, 3 & 4: Determine primary (P) and secondary (S) colors.
    primary_color = -1  # Use -1 to indicate no color assigned yet
    secondary_color = -1 
    
    if len(color_counts) == 0:
         # Step 4: No non-background colors, return grid of zeros
         return [[0 for _ in range(width)] for _ in range(height)]
    elif len(color_counts) == 1:
         # Step 3: Only one non-background color, it's primary
         primary_color = list(color_counts.keys())[0]
         # secondary_color remains -1
    else: 
        # Step 2: Two or more colors (examples suggest exactly two)
        # Sort by count (descending), then by color value (ascending) for tie-breaking
        sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))
        primary_color = sorted_colors[0][0]
        # Find the least frequent for secondary. If tie, pick highest value.
        # Since examples have 2, just take the second element after sorting.
        if len(sorted_colors) > 1:
             secondary_color = sorted_colors[1][0]

    # Step 5: Create an output grid initialized with background color (0).
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Step 6: Iterate through each cell of the input grid.
    for r in range(height):
        for c in range(width):
            cell_color = input_grid[r][c]

            # Step 6a: Process primary color pixels
            if cell_color == primary_color:
                # Check 8 neighbors for primary color
                p_neighbor_count_8way = count_neighbor_color(input_grid, r, c, primary_color, connectivity=8)
                # Keep P if it has at least one P neighbor (is not isolated)
                if p_neighbor_count_8way > 0:
                    output_grid[r][c] = primary_color
                # Else: output remains 0 (isolated P is removed)

            # Step 6b: Process secondary color pixels
            elif cell_color == secondary_color and secondary_color != -1: # Check if secondary color exists
                # Check 4 cardinal neighbors for primary color
                p_neighbor_count_4way = count_neighbor_color(input_grid, r, c, primary_color, connectivity=4)
                # Convert S to P if >= 2 cardinal P neighbors
                if p_neighbor_count_4way >= 2:
                    output_grid[r][c] = primary_color
                # Else: output remains 0 (S is removed)

            # Step 6c: Process background pixels (implicitly handled)
            # If cell_color == 0, output_grid[r][c] remains 0.

    # Step 7: Return the final output grid.
    return output_grid