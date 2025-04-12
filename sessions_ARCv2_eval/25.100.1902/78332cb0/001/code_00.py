import copy

"""
Transforms an input grid of integers based on its structure and the arrangement of '6' separators.

The transformation performs one of three operations:

1.  **Quadrant Reordering:** If the input is an 11x11 grid with a central cross of '6's (row 5 and column 5), it extracts the four 5x5 quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right) and stacks them vertically in the order TL, BR, TR, BL, separated by rows of five '6's. The output is 23x5.
2.  **Vertical to Horizontal:** If the input has 5 columns and consists of 5x5 blocks stacked vertically, separated by rows of '6's, it rearranges these blocks horizontally in reverse order, separated by columns of five '6's.
3.  **Horizontal to Vertical:** If the input has 5 rows and consists of 5x5 blocks arranged horizontally, separated by columns of '6's, it rearranges these blocks vertically in their original order, separated by rows of five '6's.
"""

def _get_grid_dimensions(grid: list[list[int]]) -> tuple[int, int]:
    """Gets the height and width of the grid."""
    if not grid:
        return 0, 0
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    return height, width

def _extract_subgrid(grid: list[list[int]], r_start: int, r_end: int, c_start: int, c_end: int) -> list[list[int]]:
    """Extracts a subgrid from the input grid."""
    return [row[c_start:c_end] for row in grid[r_start:r_end]]

def _is_separator_row(row: list[int], separator: int) -> bool:
    """Checks if a list consists entirely of the separator value."""
    if not row:
        return False
    return all(cell == separator for cell in row)

def _is_separator_col(grid: list[list[int]], col_index: int, separator: int) -> bool:
    """Checks if a column consists entirely of the separator value."""
    height, width = _get_grid_dimensions(grid)
    if col_index < 0 or col_index >= width:
        return False
    return all(grid[r][col_index] == separator for r in range(height))

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the input grid structure.
    """
    output_grid = []
    height, width = _get_grid_dimensions(input_grid)
    separator = 6
    block_size = 5
    separator_row_content = [separator] * block_size

    # --- Check for Case 1: Quadrant Reordering (11x11 grid) ---
    if height == 11 and width == 11:
        is_case_1 = True
        # Check for separator row at index 5
        if not _is_separator_row(input_grid[5], separator):
            is_case_1 = False
        # Check for separator column at index 5
        if not _is_separator_col(input_grid, 5, separator):
            is_case_1 = False

        if is_case_1:
            # Extract the four 5x5 quadrants
            tl = _extract_subgrid(input_grid, 0, 5, 0, 5)
            tr = _extract_subgrid(input_grid, 0, 5, 6, 11)
            bl = _extract_subgrid(input_grid, 6, 11, 0, 5)
            br = _extract_subgrid(input_grid, 6, 11, 6, 11)

            # Construct the output grid by stacking TL, BR, TR, BL vertically
            output_grid.extend(tl)
            output_grid.append(separator_row_content)
            output_grid.extend(br)
            output_grid.append(separator_row_content)
            output_grid.extend(tr)
            output_grid.append(separator_row_content)
            output_grid.extend(bl)
            return output_grid # Return immediately as this case is identified

    # --- Check for Case 2: Vertical Stack to Horizontal Row (Width = 5) ---
    if width == block_size:
        blocks = []
        current_block_start_row = 0
        is_case_2 = False
        for r in range(height):
            # Check if it's a separator row
            if r > 0 and (r + 1) % (block_size + 1) == 0:
                 if _is_separator_row(input_grid[r], separator):
                     block = _extract_subgrid(input_grid, current_block_start_row, r, 0, width)
                     if len(block) == block_size: # Check if the extracted block is 5x5
                         blocks.append(block)
                         current_block_start_row = r + 1
                         is_case_2 = True # Mark as potentially case 2
                 else:
                     is_case_2 = False # Invalid separator pattern
                     break # Exit check if separator is not found where expected
            # Check end of grid for last block
            elif r == height - 1:
                block = _extract_subgrid(input_grid, current_block_start_row, height, 0, width)
                if len(block) == block_size:
                    blocks.append(block)
                    # Only confirm Case 2 if at least one separator was found or only one block exists
                    is_case_2 = is_case_2 or len(blocks) == 1 
                else:
                     is_case_2 = False # Last segment is not a valid block size

        if is_case_2 and blocks:
            # Reverse the order of blocks
            blocks.reverse()

            # Construct the horizontal output grid
            output_grid = [[] for _ in range(block_size)]
            num_blocks = len(blocks)
            for i, block in enumerate(blocks):
                for r in range(block_size):
                    output_grid[r].extend(block[r])
                # Add separator column if not the last block
                if i < num_blocks - 1:
                    for r in range(block_size):
                        output_grid[r].append(separator)
            return output_grid # Return immediately

    # --- Check for Case 3: Horizontal Row to Vertical Stack (Height = 5) ---
    if height == block_size:
        blocks = []
        current_block_start_col = 0
        is_case_3 = False
        for c in range(width):
             # Check if it's a separator column
            if c > 0 and (c + 1) % (block_size + 1) == 0:
                if _is_separator_col(input_grid, c, separator):
                    block = _extract_subgrid(input_grid, 0, height, current_block_start_col, c)
                    if block and len(block[0]) == block_size: # Check if block has width 5
                         blocks.append(block)
                         current_block_start_col = c + 1
                         is_case_3 = True # Mark as potentially case 3
                else:
                    is_case_3 = False # Invalid separator pattern
                    break # Exit check
            # Check end of grid for last block
            elif c == width - 1:
                 block = _extract_subgrid(input_grid, 0, height, current_block_start_col, width)
                 if block and len(block[0]) == block_size:
                     blocks.append(block)
                     is_case_3 = is_case_3 or len(blocks) == 1 # Confirm if separator found or only 1 block
                 else:
                     is_case_3 = False # Last segment not valid block size

        if is_case_3 and blocks:
            # Construct the vertical output grid (order is preserved)
            output_grid = []
            num_blocks = len(blocks)
            for i, block in enumerate(blocks):
                output_grid.extend(block)
                # Add separator row if not the last block
                if i < num_blocks - 1:
                    output_grid.append(separator_row_content)
            return output_grid # Return immediately

    # If none of the cases matched, return the input grid or an empty one (adjust as needed)
    # For this problem, it seems one of the transformations should always apply based on examples.
    # If no case matches, it might indicate an unexpected input format.
    # Returning the original grid might be a safe default, but could hide errors.
    # Let's return an empty list to signify failure or an unhandled case for now.
    # print("Warning: No transformation rule matched the input grid structure.")
    return output_grid # Return empty if no case matched explicitly