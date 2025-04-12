import copy

"""
The transformation operates on a grid divided into four sections by vertical green lines (color 3).
Sections are defined by column ranges: Sec 1 (cols 1-4), Sec 2 (cols 6-9), Sec 3 (cols 11-14), Sec 4 (cols 16-19).
The transformation rule depends on the count of yellow pixels (color 4) in Section 3 (cols 11-14) of the input grid.

Rule A (If count == 3):
- Swap Section 1 and Section 4 content using direct column translation.
- Yellow pixels from input Sec 1 move +15 columns to output Sec 4.
- Yellow pixels from input Sec 4 move -15 columns to output Sec 1.
- Sections 2 and 3 remain unchanged.

Rule B (If count != 3):
- Cycle patterns using anchor-based relative placement: 1 -> 3, 3 -> 4, 4 -> 1.
- The pattern (relative coordinates) is identified based on the top-leftmost yellow pixel (anchor) in the source section.
- The pattern is placed in the target section such that the anchor lands at its original row but in the starting column of the target section.
- Section 2 remains unchanged.
"""

# --- Helper Functions ---

def count_yellows_in_section(grid: list[list[int]], start_col: int, end_col: int) -> int:
    """Counts the number of yellow pixels (4) within the specified column bounds."""
    count = 0
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    for r in range(height):
        current_end_col = min(end_col, width - 1)
        for c in range(start_col, current_end_col + 1):
            if grid[r][c] == 4:
                count += 1
    return count

def get_yellow_pixels_coords(grid: list[list[int]], start_col: int, end_col: int) -> list[tuple[int, int]]:
    """Gets absolute coordinates (r, c) of all yellow pixels in a section."""
    coords = []
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    for r in range(height):
        current_end_col = min(end_col, width - 1)
        for c in range(start_col, current_end_col + 1):
            if grid[r][c] == 4:
                coords.append((r, c))
    return coords

def find_yellow_pattern_anchor_relative(grid: list[list[int]], start_col: int, end_col: int) -> tuple[int | None, list[tuple[int, int]]]:
    """
    Finds the top-leftmost yellow pixel's row (anchor_row) and 
    the relative coordinates of all yellow pixels in the section.
    """
    coords = []
    min_row, min_col = float('inf'), float('inf')
    found_yellow = False
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    for r in range(height):
        current_end_col = min(end_col, width - 1)
        for c in range(start_col, current_end_col + 1):
            if grid[r][c] == 4: # 4 is yellow
                coords.append((r, c))
                found_yellow = True
                if r < min_row:
                    min_row = r
                    min_col = c 
                elif r == min_row and c < min_col:
                    min_col = c 

    if not found_yellow:
        return None, []

    relative_coords = [(r - min_row, c - min_col) for r, c in coords]
    return min_row, relative_coords

def clear_section(grid: list[list[int]], start_col: int, end_col: int):
    """Sets all non-green (3) pixels within the column bounds to white (0)."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    for r in range(height):
        current_end_col = min(end_col, width - 1)
        for c in range(start_col, current_end_col + 1):
            if grid[r][c] != 3: # Don't clear green separators
                grid[r][c] = 0

def place_translated_pixels(grid: list[list[int]], source_coords: list[tuple[int, int]], col_offset: int):
    """Places yellow pixels by translating source coordinates."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    for r, c in source_coords:
        target_c = c + col_offset
        if 0 <= r < height and 0 <= target_c < width:
            grid[r][target_c] = 4

def place_relative_pattern(grid: list[list[int]], anchor_row: int | None, target_start_col: int, relative_coords: list[tuple[int, int]]):
    """Places a pattern using anchor row and relative coordinates."""
    if anchor_row is None:
        return 

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    for rel_r, rel_c in relative_coords:
        target_row = anchor_row + rel_r
        target_col = target_start_col + rel_c
        if 0 <= target_row < height and 0 <= target_col < width:
            grid[target_row][target_col] = 4


# --- Main Transform Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    
    # Define section boundaries (inclusive) and start columns
    sections = {
        # id: (start_col, end_col)
        1: (1, 4),
        2: (6, 9),
        3: (11, 14),
        4: (16, 19)
    }
    section_start_cols = {
        1: 1,
        2: 6,
        3: 11,
        4: 16
    }

    # Determine the rule based on Section 3 yellow count
    sec3_start, sec3_end = sections[3]
    sec3_yellow_count = count_yellows_in_section(input_grid, sec3_start, sec3_end)
    
    # Apply transformation rule
    if sec3_yellow_count == 3:
        # Rule A: Swap 1 <=> 4 using translation. Keep 2, 3 unchanged.
        
        # Get source pixel coordinates
        sec1_coords = get_yellow_pixels_coords(input_grid, sections[1][0], sections[1][1])
        sec4_coords = get_yellow_pixels_coords(input_grid, sections[4][0], sections[4][1])

        # Clear target sections in output grid
        clear_section(output_grid, sections[1][0], sections[1][1])
        clear_section(output_grid, sections[4][0], sections[4][1])

        # Place translated pixels
        place_translated_pixels(output_grid, sec1_coords, 15) # Sec 1 -> Sec 4 (+15)
        place_translated_pixels(output_grid, sec4_coords, -15) # Sec 4 -> Sec 1 (-15)
        
        # Sections 2 and 3 are implicitly unchanged

    else:
        # Rule B: Cycle 1 -> 3 -> 4 -> 1 using anchor/relative placement. Keep 2 unchanged.
        
        # Get source patterns (anchor row, relative coordinates)
        anchor_row1, rel_coords1 = find_yellow_pattern_anchor_relative(input_grid, sections[1][0], sections[1][1])
        anchor_row3, rel_coords3 = find_yellow_pattern_anchor_relative(input_grid, sections[3][0], sections[3][1])
        anchor_row4, rel_coords4 = find_yellow_pattern_anchor_relative(input_grid, sections[4][0], sections[4][1])

        # Clear target sections in output grid
        clear_section(output_grid, sections[1][0], sections[1][1])
        clear_section(output_grid, sections[3][0], sections[3][1])
        clear_section(output_grid, sections[4][0], sections[4][1])

        # Place patterns in cycled positions
        place_relative_pattern(output_grid, anchor_row1, section_start_cols[3], rel_coords1) # 1 -> 3
        place_relative_pattern(output_grid, anchor_row3, section_start_cols[4], rel_coords3) # 3 -> 4
        place_relative_pattern(output_grid, anchor_row4, section_start_cols[1], rel_coords4) # 4 -> 1

        # Section 2 is implicitly unchanged

    return output_grid