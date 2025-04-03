import math

"""
Transformation Rule:
1. Identify the single maroon (9) pixel (the "pivot") in the input row.
2. Identify the contiguous block of pixels of a single color (not white 0 and not maroon 9) (the "colored block").
3. Identify the sequence of white (0) pixels (the "spacing") directly between the colored block and the pivot pixel.
4. Determine if the colored block is initially to the left or right of the pivot.
5. Construct an output row of the same length, initialized with white (0) pixels.
6. Place the pivot pixel (9) in the output row at its original index.
7. Place the identified spacing sequence and the colored block into the output row on the *opposite* side of the pivot compared to their input position, maintaining the same content and relative order (i.e., if spacing was between block and pivot, it remains between block and pivot on the other side). Handle boundary conditions: if the moved elements don't fit, return the original input grid.
"""

# Helper Functions

def find_pivot(row):
    """Finds the index of the first occurrence of the pivot pixel (color 9)."""
    try:
        return row.index(9)
    except ValueError:
        # Pivot not found
        return -1

def find_colored_block(row):
    """
    Finds the start index, end index (inclusive), color, 
    and content (list of pixel values) of the first contiguous colored block 
    (non-0 and non-9).
    Returns: (start_idx, end_idx, content) or (-1, -1, []) if not found.
    """
    block_start = -1
    block_end = -1
    block_color = -1
    block_content = []

    for i, pixel in enumerate(row):
        # Start searching for a non-background, non-pivot pixel
        if block_start == -1:
            if pixel != 0 and pixel != 9:
                block_start = i
                block_color = pixel
                block_end = i # Initialize end index
        # If already found the start of a block
        else:
            # Check if the current pixel continues the block (same color)
            if pixel == block_color:
                block_end = i # Extend the block
            # If the pixel is different, the block ends here (or before)
            else:
                break # Found the end of the contiguous block

    # If a block was successfully identified
    if block_start != -1:
        block_content = row[block_start : block_end + 1]
        return block_start, block_end, block_content
    else:
        # No block found
        return -1, -1, []

def extract_spacing(row, block_start, block_end, pivot_index):
    """
    Extracts the sequence of pixels between the block and the pivot.
    Returns the spacing sequence (list of pixels).
    """
    spacing_pixels = []
    if block_end < pivot_index: # Block is left
        spacing_start_idx = block_end + 1
        spacing_end_idx = pivot_index # Exclusive index for slicing
        if spacing_start_idx < spacing_end_idx:
             # Ensure only background pixels are considered spacing
             segment = row[spacing_start_idx:spacing_end_idx]
             if all(p == 0 for p in segment):
                 spacing_pixels = segment
             # else: could handle unexpected content here if needed
    elif block_start > pivot_index: # Block is right
        spacing_start_idx = pivot_index + 1
        spacing_end_idx = block_start # Exclusive index for slicing
        if spacing_start_idx < spacing_end_idx:
             # Ensure only background pixels are considered spacing
             segment = row[spacing_start_idx:spacing_end_idx]
             if all(p == 0 for p in segment):
                spacing_pixels = segment
             # else: could handle unexpected content here if needed
             
    # If block is adjacent, spacing is empty, which is handled by the conditions
    return spacing_pixels

# Main Transformation Function

def transform(input_grid):
    """
    Applies the transformation rule to move the colored block and spacing
    across the pivot pixel.
    """
    # --- Input Validation ---
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle invalid input format, maybe return input or raise error
        # Returning original grid seems safest for ARC tasks if unsure
        return input_grid 

    input_row = input_grid[0]
    row_len = len(input_row)

    # Handle empty row case
    if row_len == 0:
        return input_grid # Return original empty grid

    # --- Step 1 & 2: Locate Pivot and Block ---
    pivot_index = find_pivot(input_row)
    if pivot_index == -1:
        # Pivot not found, cannot perform transformation
        return input_grid 

    block_start, block_end, block_content = find_colored_block(input_row)
    if block_start == -1:
        # Colored block not found, cannot perform transformation
        return input_grid 

    block_len = len(block_content)

    # --- Step 3 & 4: Extract Spacing and Determine Side ---
    spacing_content = extract_spacing(input_row, block_start, block_end, pivot_index)
    spacing_len = len(spacing_content)
    
    # Determine if the block is to the left of the pivot
    is_left = block_end < pivot_index 

    # --- Step 5: Initialize Output Grid ---
    output_row = [0] * row_len # Fill with background color (0)

    # --- Step 6: Place Pivot ---
    output_row[pivot_index] = 9

    # --- Step 7: Place Spacing and Block on Opposite Side ---
    if is_left:
        # Block was left, move to right: Config = Pivot | Spacing | Block
        # Calculate start index for spacing (immediately after pivot)
        new_spacing_start = pivot_index + 1
        # Calculate start index for block (immediately after spacing)
        new_block_start = new_spacing_start + spacing_len
        
        # Calculate end indices (exclusive for slicing)
        new_spacing_end = new_spacing_start + spacing_len
        new_block_end = new_block_start + block_len

        # Bounds check: Ensure the entire moved structure fits within the grid
        if new_block_end <= row_len:
            # Place spacing
            output_row[new_spacing_start:new_spacing_end] = spacing_content
            # Place block
            output_row[new_block_start:new_block_end] = block_content
        else:
            # Does not fit, return original grid as per refined requirement
            return input_grid 
            
    else: # Block was right, move to left: Config = Block | Spacing | Pivot
        # Calculate start index for block (ends spacing_len before pivot)
        new_block_start = pivot_index - spacing_len - block_len
        # Calculate start index for spacing (starts immediately after block)
        new_spacing_start = new_block_start + block_len
        
        # Calculate end indices (exclusive for slicing)
        new_block_end = new_block_start + block_len
        new_spacing_end = new_spacing_start + spacing_len
        
        # Bounds check: Ensure the entire moved structure fits within the grid
        if new_block_start >= 0:
             # Place block
            output_row[new_block_start:new_block_end] = block_content
            # Place spacing
            output_row[new_spacing_start:new_spacing_end] = spacing_content
        else:
            # Does not fit, return original grid
            return input_grid

    # --- Finalize: Return the transformed grid ---
    # Wrap the output row in a list to match ARC grid format
    return [output_row]