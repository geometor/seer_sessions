import copy

"""
The transformation identifies yellow pixel patterns within specific sections of the grid, 
defined by static vertical green lines. The grid is divided into four main 
operational sections: Section 1 (columns 1-4), Section 2 (columns 6-9), 
Section 3 (columns 11-14), and Section 4 (columns 16-19). 

The transformation rule is to swap the entire yellow pixel pattern found in 
Section 1 with the entire yellow pixel pattern found in Section 4. The patterns 
maintain their internal relative structure. The placement in the swapped section 
is anchored by the top-leftmost pixel of the original pattern. The top-leftmost 
pixel of the pattern from Section 1 moves to the same row but starts at the 
first column of Section 4 (column 16). Similarly, the top-leftmost pixel of the 
pattern from Section 4 moves to the same row but starts at the first column of 
Section 1 (column 1). The content (including yellow pixels) within Section 2 
and Section 3 remains unchanged.
"""

def find_yellow_pattern(grid: list[list[int]], start_col: int, end_col: int) -> tuple[int | None, list[tuple[int, int]]]:
    """
    Finds all yellow pixels within the specified column bounds.
    Calculates their coordinates relative to the top-leftmost yellow pixel found.

    Args:
        grid: The input grid.
        start_col: The starting column index (inclusive) of the section.
        end_col: The ending column index (inclusive) of the section.

    Returns:
        A tuple containing:
        - The row index of the top-leftmost yellow pixel (or None if no yellow pixels).
        - A list of relative coordinates (row_offset, col_offset) for all yellow pixels 
          relative to the top-leftmost pixel (or an empty list if none found).
    """
    coords = []
    min_row, min_col = float('inf'), float('inf')
    height = len(grid)
    
    for r in range(height):
        for c in range(start_col, end_col + 1):
            # Check bounds just in case, though columns should be valid
            if c < len(grid[0]) and grid[r][c] == 4: # 4 is yellow
                coords.append((r, c))
                if r < min_row:
                    min_row = r
                    min_col = c # Reset min_col when a new min_row is found
                elif r == min_row and c < min_col:
                    min_col = c # Update min_col if on the same min_row

    if not coords:
        return None, []

    # Calculate relative coordinates based on the found top-leftmost pixel
    relative_coords = [(r - min_row, c - min_col) for r, c in coords]
    
    return min_row, relative_coords

def clear_section(grid: list[list[int]], start_col: int, end_col: int):
    """
    Sets all pixels within the specified column bounds to white (0).

    Args:
        grid: The grid to modify (should be the output grid).
        start_col: The starting column index (inclusive).
        end_col: The ending column index (inclusive).
    """
    height = len(grid)
    width = len(grid[0])
    for r in range(height):
        for c in range(start_col, end_col + 1):
             if c < width: # Check bounds
                grid[r][c] = 0 # 0 is white

def place_pattern(grid: list[list[int]], anchor_row: int, target_start_col: int, relative_coords: list[tuple[int, int]]):
    """
    Places a pattern of yellow pixels onto the grid based on an anchor point and relative coordinates.

    Args:
        grid: The grid to modify (should be the output grid).
        anchor_row: The row index for the top-leftmost pixel of the pattern.
        target_start_col: The column index for the top-leftmost pixel of the pattern.
        relative_coords: A list of (row_offset, col_offset) tuples defining the pattern.
    """
    height = len(grid)
    width = len(grid[0])
    for rel_r, rel_c in relative_coords:
        target_row = anchor_row + rel_r
        target_col = target_start_col + rel_c
        # Check if the target coordinates are within the grid bounds
        if 0 <= target_row < height and 0 <= target_col < width:
            grid[target_row][target_col] = 4 # 4 is yellow

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by swapping the yellow pixel patterns between
    Section 1 (cols 1-4) and Section 4 (cols 16-19).

    Args:
        input_grid: The 2D list representing the input grid.

    Returns:
        The 2D list representing the transformed output grid.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Define section column boundaries (inclusive)
    sec1_start, sec1_end = 1, 4
    sec4_start, sec4_end = 16, 19

    # 1. Find the yellow pattern in Section 1 of the input grid
    anchor_row1, rel_coords1 = find_yellow_pattern(input_grid, sec1_start, sec1_end)

    # 2. Find the yellow pattern in Section 4 of the input grid
    anchor_row4, rel_coords4 = find_yellow_pattern(input_grid, sec4_start, sec4_end)

    # 3. Clear Section 1 and Section 4 in the output grid
    clear_section(output_grid, sec1_start, sec1_end)
    clear_section(output_grid, sec4_start, sec4_end)

    # 4. Place the pattern from original Section 1 into output Section 4
    if anchor_row1 is not None:
        place_pattern(output_grid, anchor_row1, sec4_start, rel_coords1)

    # 5. Place the pattern from original Section 4 into output Section 1
    if anchor_row4 is not None:
        place_pattern(output_grid, anchor_row4, sec1_start, rel_coords4)

    # Return the modified grid
    return output_grid