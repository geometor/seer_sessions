import numpy as np
from typing import List, Tuple, Dict, Set, Optional

"""
Transforms an input grid based on the following rules:

1.  **Identify Blocks:** The grid is divided into horizontal blocks separated by rows consisting entirely of the number 4.
2.  **Analyze First Block:** Determine the set of unique non-zero, non-4 numbers ('characteristic numbers') within the first block.
3.  **Determine Mode:**
    *   **Mode 1:** If the first block contains exactly one unique characteristic number.
    *   **Mode 2:** If the first block contains zero or more than one unique characteristic number.
4.  **Apply Transformation:**
    *   **Mode 1:** For each block, find its unique characteristic number. Replace all instances of '1' within that block with its characteristic number.
    *   **Mode 2:**
        *   The first block remains unchanged.
        *   Identify vertical regions defined by columns containing 4s.
        *   For each vertical region in the first block, find its characteristic number (if any).
        *   For all subsequent blocks, replace each '1' with the characteristic number found in the corresponding vertical region of the first block.
5.  **Reconstruct Grid:** Combine the modified blocks and original separator rows to form the output grid.
"""

def find_separator_rows(grid: np.ndarray) -> List[int]:
    """Finds the indices of rows consisting entirely of the number 4."""
    separator_indices = []
    for r_idx, row in enumerate(grid):
        if np.all(row == 4):
            separator_indices.append(r_idx)
    return separator_indices

def get_blocks(grid: np.ndarray, separator_indices: List[int]) -> List[Tuple[int, int, np.ndarray]]:
    """Splits the grid into blocks based on separator row indices."""
    blocks = []
    start_row = 0
    for sep_idx in separator_indices:
        if start_row < sep_idx: # Avoid empty blocks if separators are consecutive
             blocks.append((start_row, sep_idx -1, grid[start_row:sep_idx, :]))
        # Add the separator row itself as a "block" to preserve it
        blocks.append((sep_idx, sep_idx, grid[sep_idx:sep_idx+1, :]))
        start_row = sep_idx + 1
    # Add the last block if any rows remain after the last separator
    if start_row < grid.shape[0]:
        blocks.append((start_row, grid.shape[0] - 1, grid[start_row:, :]))
    return blocks

def find_characteristic_numbers(block: np.ndarray) -> Set[int]:
    """Finds unique non-zero, non-4 numbers in a given block."""
    # Flatten the block, filter out 0s and 4s, and find unique values
    unique_nums = np.unique(block)
    # characteristic_nums = set(num for num in unique_nums if num != 0 and num != 4)
    # Use explicit filtering compatible with numpy arrays
    mask = (unique_nums != 0) & (unique_nums != 4)
    characteristic_nums = set(unique_nums[mask])

    return characteristic_nums

def find_vertical_separators_and_regions(grid: np.ndarray) -> List[Tuple[int, int]]:
    """Finds columns with 4s and defines the column ranges for vertical regions."""
    num_cols = grid.shape[1]
    separator_cols = set()
    for c_idx in range(num_cols):
         # Check if the column contains any 4s (often aligned with horizontal separators)
         # A stricter definition might be needed if 4s can appear elsewhere non-structurally
         # For now, assume any 4 indicates a potential boundary
         if np.any(grid[:, c_idx] == 4):
              separator_cols.add(c_idx)

    regions = []
    start_col = 0
    sorted_sep_cols = sorted(list(separator_cols))

    for sep_c_idx in sorted_sep_cols:
        if start_col < sep_c_idx: # Define region before the separator
            regions.append((start_col, sep_c_idx - 1))
        start_col = sep_c_idx + 1 # Start next region after the separator

    # Add the last region if any columns remain after the last separator
    if start_col < num_cols:
        regions.append((start_col, num_cols - 1))

    # If no separators were found, the whole width is one region
    if not regions and num_cols > 0:
         regions.append((0, num_cols -1))

    return regions


def get_region_reference_numbers(block: np.ndarray, regions: List[Tuple[int, int]]) -> Dict[Tuple[int, int], Optional[int]]:
    """Maps vertical regions to the characteristic number found in that region within the given block."""
    reference_map = {}
    for start_col, end_col in regions:
        region_slice = block[:, start_col : end_col + 1]
        char_nums = find_characteristic_numbers(region_slice)
        # Assume only one characteristic number per region in the reference block for Mode 2
        reference_map[(start_col, end_col)] = list(char_nums)[0] if len(char_nums) == 1 else None
    return reference_map


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the identified mode derived from the first block's properties.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np) # Start with a copy to modify

    # 1. Identify separator rows
    separator_indices = find_separator_rows(input_np)

    # 2. Split grid into blocks (including separator rows as blocks)
    all_blocks_info = get_blocks(input_np, separator_indices)

    # Filter out separator blocks to get actual content blocks
    content_blocks_info = [(s, e, b) for s, e, b in all_blocks_info if not np.all(b == 4)]

    if not content_blocks_info: # Handle grids with only separators or empty grids
        return output_np.tolist()

    # 3. Analyze First Block
    first_block_start, first_block_end, first_block_data = content_blocks_info[0]
    first_block_char_nums = find_characteristic_numbers(first_block_data)
    num_unique_chars_first_block = len(first_block_char_nums)

    # 4. Determine Mode and Apply Transformation
    if num_unique_chars_first_block == 1:
        # Execute Mode 1
        mode1_char_num = list(first_block_char_nums)[0] # Get the single characteristic number

        for start_row, end_row, block_data in content_blocks_info:
            # Find the characteristic number for *this* block
            current_block_char_nums = find_characteristic_numbers(block_data)
            if len(current_block_char_nums) == 1:
                replace_value = list(current_block_char_nums)[0]
                # Iterate through cells in the current block of the *output* grid
                for r in range(start_row, end_row + 1):
                    for c in range(output_np.shape[1]):
                        if output_np[r, c] == 1:
                            output_np[r, c] = replace_value
            # else: Block might not have a unique char num, leave 1s as is? Rule unclear, assume replace only if unique char found.
            # Current implementation replaces based on first block's char num for all blocks in Mode 1
            # Reread NL Program: Mode 1 says "each block finds *its own* unique characteristic number"
            # Correction: Find char num per block.

            # Find characteristic number for *this* block
            current_block_char_nums = find_characteristic_numbers(block_data)
            # If this block has *exactly one* characteristic number, use it for replacement
            if len(current_block_char_nums) == 1:
                 replace_value = list(current_block_char_nums)[0]
                 for r in range(start_row, end_row + 1):
                     for c in range(output_np.shape[1]):
                         # Check original input value was 1 before replacing in output
                         if input_np[r, c] == 1:
                             output_np[r, c] = replace_value
            # If the block doesn't have exactly one char num, its 1s remain unchanged per rule.


    else:
        # Execute Mode 2
        # First block remains unchanged (already handled by copying to output_np)

        # Identify vertical regions based on the *entire* grid's structure
        vertical_regions = find_vertical_separators_and_regions(input_np)

        # Find reference numbers from the first block for each region
        region_reference_map = get_region_reference_numbers(first_block_data, vertical_regions)


        # Process subsequent blocks (skip the first content block)
        for i in range(1, len(content_blocks_info)):
            start_row, end_row, block_data = content_blocks_info[i]

            # Iterate through cells in the current block of the *output* grid
            for r in range(start_row, end_row + 1):
                for c in range(output_np.shape[1]):
                    # Check original input value was 1 before replacing
                    if input_np[r, c] == 1:
                        # Determine which vertical region this cell belongs to
                        found_region = False
                        for region_start_col, region_end_col in vertical_regions:
                            if region_start_col <= c <= region_end_col:
                                # Find the reference number for this region
                                reference_num = region_reference_map.get((region_start_col, region_end_col))
                                if reference_num is not None:
                                    output_np[r, c] = reference_num
                                found_region = True
                                break
                        # If cell '1' is in a separator column (not in any defined region), it might remain unchanged.
                        # Current logic implies it remains 1 if no reference number is found or it's not in a region.

    # 5. Convert back to list of lists and return
    return output_np.tolist()
