import numpy as np
from typing import List, Tuple, Dict, Set, Optional

"""
Transforms an input grid based on the following rules:

1.  **Identify Blocks:** The grid is divided into horizontal blocks separated by rows consisting entirely of the number 4 (SeparatorRows).
2.  **Analyze First Block:** Determine the set of unique non-zero, non-1, non-4 numbers ('characteristic numbers') within the first content block.
3.  **Determine Mode:**
    *   **Mode 1:** If the first block contains exactly one unique characteristic number.
    *   **Mode 2:** If the first block contains zero or more than one unique characteristic number.
4.  **Apply Transformation:**
    *   **Mode 1:** For each content block, find its own unique characteristic number. Replace all instances of '1' (PlaceholderCells) within that block with its characteristic number. If a block doesn't have exactly one characteristic number, its '1's remain unchanged.
    *   **Mode 2:**
        *   The first block remains unchanged.
        *   Identify vertical regions defined by columns containing 4s (SeparatorColumns).
        *   For each vertical region in the first block, find its characteristic number.
        *   For all subsequent blocks, replace each '1' with the characteristic number found in the corresponding vertical region of the first block. If a '1' is in a SeparatorColumn or a region with no characteristic number, it remains unchanged.
5.  **Reconstruct Grid:** The transformation is applied directly to a copy of the input grid.
"""

# === Helper Functions ===

def find_separator_rows(grid: np.ndarray) -> List[int]:
    """Finds the indices of rows consisting entirely of the number 4."""
    separator_indices = []
    if grid.ndim != 2 or grid.shape[1] == 0: # Handle empty or 1D arrays
        return []
    for r_idx, row in enumerate(grid):
        if np.all(row == 4):
            separator_indices.append(r_idx)
    return separator_indices

def get_content_blocks(grid: np.ndarray, separator_indices: List[int]) -> List[Tuple[int, int, np.ndarray]]:
    """
    Splits the grid into content blocks based on separator row indices.
    Returns a list of tuples: (start_row, end_row, block_data).
    Excludes the separator rows themselves.
    """
    blocks = []
    start_row = 0
    grid_height = grid.shape[0]

    for sep_idx in separator_indices:
        # Add block before the separator if it's not empty
        if start_row < sep_idx:
            blocks.append((start_row, sep_idx - 1, grid[start_row:sep_idx, :]))
        # Move start row past the separator
        start_row = sep_idx + 1

    # Add the last block if any rows remain after the last separator
    if start_row < grid_height:
        blocks.append((start_row, grid_height - 1, grid[start_row:, :]))

    return blocks

def find_characteristic_numbers(block: np.ndarray) -> Set[int]:
    """Finds unique non-zero, non-1, non-4 numbers in a given block."""
    if block.size == 0:
        return set()
    unique_nums = np.unique(block)
    # Filter out 0, 1, and 4
    mask = (unique_nums != 0) & (unique_nums != 1) & (unique_nums != 4)
    characteristic_nums = set(unique_nums[mask])
    return characteristic_nums

def find_vertical_separators_and_regions(grid: np.ndarray) -> Tuple[List[int], List[Tuple[int, int]]]:
    """
    Finds columns containing 4s (SeparatorColumns) and defines the
    column ranges (start_col, end_col) for vertical regions between them.
    Returns a tuple: (separator_col_indices, region_definitions).
    """
    num_cols = grid.shape[1]
    if num_cols == 0:
        return [], []

    separator_cols_set = set()
    # A column is a separator if it contains a 4
    for c_idx in range(num_cols):
         if np.any(grid[:, c_idx] == 4):
              separator_cols_set.add(c_idx)

    separator_cols_list = sorted(list(separator_cols_set))

    regions = []
    start_col = 0
    for sep_c_idx in separator_cols_list:
        # Define region before the separator column
        if start_col < sep_c_idx:
            regions.append((start_col, sep_c_idx - 1))
        # Move start to after the separator column
        start_col = sep_c_idx + 1

    # Add the last region if any columns remain after the last separator
    if start_col < num_cols:
        regions.append((start_col, num_cols - 1))

    # If no separators were found, the whole width is one region
    # (Technically handled by the loop logic if separator_cols_list is empty)
    # Add explicit check for clarity / edge case where grid has columns but no separators
    if not separator_cols_list and num_cols > 0 and not regions:
         regions.append((0, num_cols -1))


    return separator_cols_list, regions

def get_region_reference_numbers(block: np.ndarray, regions: List[Tuple[int, int]]) -> Dict[Tuple[int, int], Optional[int]]:
    """
    Maps vertical regions (col_start, col_end) to the single characteristic
    number found within that region in the given reference block.
    Returns None for regions with zero or multiple characteristic numbers.
    """
    reference_map = {}
    if block.size == 0: # Handle empty block case
        for region in regions:
            reference_map[region] = None
        return reference_map

    num_cols_block = block.shape[1]

    for start_col, end_col in regions:
        # Ensure column indices are within the block's bounds
        actual_start_col = max(0, start_col)
        actual_end_col = min(num_cols_block - 1, end_col)

        # Check if the adjusted region is valid
        if actual_start_col > actual_end_col:
            reference_map[(start_col, end_col)] = None
            continue

        # Extract the slice for the region
        region_slice = block[:, actual_start_col : actual_end_col + 1]

        if region_slice.size == 0:
             reference_map[(start_col, end_col)] = None
             continue

        # Find characteristic numbers within this specific region slice
        char_nums_in_region = find_characteristic_numbers(region_slice)

        # Store the number only if there's exactly one
        if len(char_nums_in_region) == 1:
            reference_map[(start_col, end_col)] = list(char_nums_in_region)[0]
        else:
            reference_map[(start_col, end_col)] = None # 0 or >1 characteristic numbers

    return reference_map

# === Main Transformation Function ===

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic based on the analysis of the first block.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)

    # Handle empty input grid
    if input_np.size == 0:
        return []

    # 1. Identify horizontal separator rows
    separator_indices = find_separator_rows(input_np)

    # 2. Get content blocks (excluding separator rows)
    content_blocks_info = get_content_blocks(input_np, separator_indices)

    # Handle case with no content blocks (e.g., grid is all 4s or empty after separators)
    if not content_blocks_info:
        return output_np.tolist()

    # 3. Analyze the first content block
    first_block_start, first_block_end, first_block_data = content_blocks_info[0]
    first_block_char_nums = find_characteristic_numbers(first_block_data)
    num_unique_chars_first_block = len(first_block_char_nums)

    # 4. Determine Mode and Apply Transformation
    if num_unique_chars_first_block == 1:
        # --- Execute Mode 1 ---
        # For each content block...
        for start_row, end_row, block_data in content_blocks_info:
            # Find the characteristic number(s) for *this* current block
            current_block_char_nums = find_characteristic_numbers(block_data)

            # Replace '1's only if this block has exactly one characteristic number
            if len(current_block_char_nums) == 1:
                replace_value = list(current_block_char_nums)[0]
                # Iterate through cells within this block's bounds
                for r in range(start_row, end_row + 1):
                    for c in range(output_np.shape[1]):
                        # Check the *original* input value at this position
                        if input_np[r, c] == 1:
                            # Modify the *output* grid
                            output_np[r, c] = replace_value
            # If block has 0 or >1 characteristic numbers, '1's remain unchanged (handled by initial copy)

    else:
        # --- Execute Mode 2 ---
        # First block remains unchanged (already handled by copying to output_np)

        # Identify vertical separator columns and regions based on the *entire* grid
        separator_cols, vertical_regions = find_vertical_separators_and_regions(input_np)

        # Get reference numbers from the first block for each vertical region
        region_reference_map = get_region_reference_numbers(first_block_data, vertical_regions)

        # Process subsequent blocks (skip the first content block at index 0)
        for i in range(1, len(content_blocks_info)):
            start_row, end_row, block_data = content_blocks_info[i]

            # Iterate through cells within this block's bounds
            for r in range(start_row, end_row + 1):
                for c in range(output_np.shape[1]):
                    # Check the *original* input value at this position
                    if input_np[r, c] == 1:
                        # Determine which vertical region this cell belongs to
                        found_region = False
                        for region_start_col, region_end_col in vertical_regions:
                            if region_start_col <= c <= region_end_col:
                                # Find the reference number associated with this region
                                reference_num = region_reference_map.get((region_start_col, region_end_col))
                                # If a valid reference number exists, replace '1' in the output
                                if reference_num is not None:
                                    output_np[r, c] = reference_num
                                found_region = True
                                break
                        # If cell '1' is in a separator column (i.e., c is in separator_cols)
                        # or in a region without a reference number, it remains '1' (handled by initial copy).

    # 5. Convert the final numpy array back to a list of lists and return
    return output_np.tolist()