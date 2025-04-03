"""
Transforms a 1D input grid (represented as a list within a list, or a NumPy array)
based on the following rule:
1. Identifies three key components in the input row:
    a. A single Maroon (9) pixel (Anchor).
    b. A contiguous block of a single color C (Colored_Block), where C is not White (0) and not Maroon (9).
    c. A sequence of White (0) pixels (Separator) located between the Colored_Block and the Anchor in the input.
2. Determines the index (maroon_index) of the Anchor pixel in the input. This index is preserved in the output.
3. Records the pixel sequences for the Colored_Block and the Separator.
4. Constructs an output grid of the same dimensions, initially filled with White (0).
5. Places the Anchor pixel (9) into the output grid at its original `maroon_index`.
6. Places the recorded Separator sequence immediately following the Anchor pixel in the output grid.
7. Places the recorded Colored_Block sequence immediately following the Separator sequence in the output grid.
8. Ensures that placed sequences do not exceed the grid boundaries, truncating them if necessary.
The relative order of the Colored_Block and Anchor is effectively reversed around the Separator in the output, anchored by the Anchor's original position.
"""

# No specific imports needed beyond standard Python list operations
# import numpy as np # Only needed if direct numpy operations were required

# --- Helper Functions ---

def find_maroon_pixel(row):
    """Finds the index of the single Maroon (9) pixel."""
    try:
        return row.index(9)
    except ValueError:
        return -1 # Indicate not found

def find_colored_block(row):
    """
    Finds the first contiguous block of non-White(0), non-Maroon(9) color.
    Assumes only one such block exists per row based on examples.
    Returns: tuple (sequence, start_index, end_index_exclusive) or (None, -1, -1) if not found.
    """
    sequence = []
    start_index = -1
    end_index = -1
    block_color = -1
    in_block = False
    width = len(row)

    for i, pixel in enumerate(row):
        if not in_block:
            # Look for the start of a block (non-0, non-9)
            if pixel != 0 and pixel != 9:
                in_block = True
                start_index = i
                block_color = pixel
                sequence.append(pixel)
        else: # Already in a block
            # Check if the current pixel continues the block
            if pixel == block_color:
                sequence.append(pixel)
            else:
                # Block ends here (found different color, 0, or 9)
                end_index = i
                break # Stop searching once the first block is found and ends

    # Handle case where the block extends to the end of the row
    if in_block and end_index == -1:
        end_index = width

    if not in_block: # Block never started
        return None, -1, -1
    else:
        return sequence, start_index, end_index

def find_separator(row, block_end_index, maroon_index):
    """
    Finds the sequence of White(0) pixels between the colored block and the maroon pixel.
    Assumes block appears before maroon pixel based on examples. If maroon appears first,
    or they are adjacent, or one is missing, returns an empty list.
    Returns: list (separator sequence)
    """
    # Check if both indices are valid and the block ends before the maroon pixel starts
    if block_end_index != -1 and maroon_index != -1 and block_end_index <= maroon_index:
        # Extract the slice between the end of the block and the start of the maroon pixel
        separator = row[block_end_index:maroon_index]
        # Note: Assumes these are all 0s based on problem description/examples
        return separator
    else:
        # Covers cases where block is after maroon, one component is missing, or they are adjacent
        return []

# --- Main Transformation Function ---

def transform(input_grid):
    # Handle potential NumPy array input from the testing framework
    if 'numpy' in str(type(input_grid)):
        # Convert NumPy array to list of lists
        input_grid_list = input_grid.tolist()
    else:
        # Assume it's already a list of lists
        input_grid_list = input_grid

    # Validate input format (expecting list of lists)
    if not input_grid_list or not isinstance(input_grid_list, list) or not input_grid_list or not isinstance(input_grid_list[0], list):
        print("Error: Invalid input grid format. Expected list of lists or compatible NumPy array.")
        # Return an empty structure or handle as appropriate for the framework
        return []

    input_row = input_grid_list[0]
    width = len(input_row)

    # Initialize output grid with background color (0)
    output_row = [0] * width

    # --- Step 1: Identify Components in Input ---
    # Find the anchor point: the Maroon pixel
    maroon_index = find_maroon_pixel(input_row)
    if maroon_index == -1:
        # If the core anchor is missing, cannot perform transformation as defined
        print("Warning: Maroon pixel (9) not found. Returning initial empty grid.")
        return [output_row] # Return the blank grid

    # Find the colored block
    colored_block_sequence, block_start_index, block_end_index = find_colored_block(input_row)
    if colored_block_sequence is None:
        # If the colored block is missing, cannot perform transformation as defined
        print("Warning: Colored block not found. Returning initial empty grid.")
        return [output_row] # Return the blank grid

    # Find the separator sequence between the block and the maroon pixel
    # This implementation assumes block occurs before maroon pixel, based on examples
    separator_sequence = find_separator(input_row, block_end_index, maroon_index)

    # --- Step 2: Construct the Output Grid ---
    # Place the anchor Maroon pixel at its original input index
    output_row[maroon_index] = 9

    # Define the starting position for the next element (Separator)
    current_write_index = maroon_index + 1

    # Place the Separator sequence, handling boundary conditions
    sep_len = len(separator_sequence)
    if current_write_index < width and sep_len > 0:
        # Calculate how many separator pixels actually fit within the grid bounds
        separator_length_to_place = min(sep_len, width - current_write_index)
        # Place the fitting part of the separator sequence into the output row
        output_row[current_write_index : current_write_index + separator_length_to_place] = separator_sequence[:separator_length_to_place]
        # Update the write index to the position after the placed separator
        current_write_index += separator_length_to_place
    # If separator is empty or doesn't fit, current_write_index remains unchanged

    # Place the Colored Block sequence, handling boundary conditions
    block_len = len(colored_block_sequence)
    if current_write_index < width and block_len > 0:
        # Calculate how many block pixels actually fit within the grid bounds
        block_length_to_place = min(block_len, width - current_write_index)
        # Place the fitting part of the block sequence into the output row
        output_row[current_write_index : current_write_index + block_length_to_place] = colored_block_sequence[:block_length_to_place]
        # No need to update current_write_index further as this is the last element

    # Return the constructed output row, wrapped in a list to match ARC format
    return [output_row]