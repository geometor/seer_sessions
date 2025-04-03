import numpy as np # Although not strictly needed for list ops, good practice for potential future array needs

def find_maroon_pixel(row):
    """Finds the index of the single Maroon (9) pixel."""
    try:
        return row.index(9)
    except ValueError:
        return -1 # Indicate not found

def find_colored_block(row):
    """
    Finds the contiguous block of non-White(0), non-Maroon(9) color.
    Returns: tuple (sequence, start_index, end_index_exclusive) or (None, -1, -1) if not found.
    """
    sequence = []
    start_index = -1
    end_index = -1
    block_color = -1
    in_block = False

    for i, pixel in enumerate(row):
        if not in_block:
            if pixel != 0 and pixel != 9:
                # Start of a new block
                in_block = True
                start_index = i
                block_color = pixel
                sequence.append(pixel)
        else: # Already in a block
            if pixel == block_color:
                # Continue the block
                sequence.append(pixel)
            else:
                # End of the block (different color, 0, or 9 found)
                end_index = i
                break # Block found and ended

    # If the block runs to the very end of the row
    if in_block and end_index == -1:
        end_index = len(row)

    if not in_block: # Block never started
        return None, -1, -1
    else:
        return sequence, start_index, end_index

def find_separator(row, block_end_index, maroon_index):
    """
    Finds the sequence of White(0) pixels between the colored block and the maroon pixel.
    Assumes block appears before maroon pixel based on examples.
    Returns: list (separator sequence)
    """
    if block_end_index != -1 and maroon_index != -1 and block_end_index <= maroon_index:
        # Extract the slice between the end of the block and the start of the maroon pixel
        separator = row[block_end_index:maroon_index]
        # Verify it's all zeros (optional, based on strictness)
        # if not all(p == 0 for p in separator):
        #     print("Warning: Non-zero elements found in expected separator region.")
        return separator
    elif maroon_index != -1 and block_end_index != -1 and maroon_index < block_end_index:
        # Handle case where maroon pixel is before the block (if needed)
        # separator = row[maroon_index + 1 : block_end_index] # Assuming block_end_index is start index here
        # This case is not seen in examples, so stick to observed pattern for now.
        print("Warning: Maroon pixel found before colored block, separator logic might need adjustment.")
        return []
    else:
        # One or both components not found or adjacent
        return []

def transform(input_grid):
    """
    Transforms the input grid according to the following rule:
    1. Identifies a single Maroon (9) pixel, a contiguous block of another color (non-0, non-9),
       and a sequence of White (0) pixels separating them in the input.
    2. Constructs the output grid by placing the Maroon pixel at its original index,
       followed immediately by the separator sequence, followed immediately by the colored block sequence.
    3. All other positions are filled with White (0).
    """
    # Input grid is expected as [[row_elements...]]
    if not input_grid or not isinstance(input_grid[0], list):
        print("Error: Invalid input grid format.")
        return [] # Return empty list for invalid input

    input_row = input_grid[0]
    width = len(input_row)

    # Initialize output grid with background color (0)
    output_row = [0] * width

    # --- Identify Components ---
    maroon_index = find_maroon_pixel(input_row)
    if maroon_index == -1:
        print("Error: Maroon pixel (9) not found.")
        return [output_row] # Return default grid if essential component missing

    colored_block_sequence, block_start_index, block_end_index = find_colored_block(input_row)
    if colored_block_sequence is None:
        print("Error: Colored block not found.")
        return [output_row] # Return default grid if essential component missing

    # Find separator based on the relative positions found
    separator_sequence = find_separator(input_row, block_end_index, maroon_index)
    # Note: find_separator currently assumes block is before maroon pixel.

    # --- Construct Output Grid ---

    # Place Maroon pixel (anchor point)
    # Boundary check already implicitly done by find_maroon_pixel finding a valid index
    output_row[maroon_index] = 9

    # Place Separator sequence after Maroon pixel
    current_index = maroon_index + 1
    sep_len = len(separator_sequence)
    if current_index < width: # Check if there's space to start placing separator
        # Calculate how many separator pixels actually fit
        fit_len = min(sep_len, width - current_index)
        output_row[current_index : current_index + fit_len] = separator_sequence[:fit_len]
        current_index += fit_len # Update index to position after placed separator

    # Place Colored Block sequence after Separator sequence
    block_len = len(colored_block_sequence)
    if current_index < width: # Check if there's space to start placing block
        # Calculate how many block pixels actually fit
        fit_len = min(block_len, width - current_index)
        output_row[current_index : current_index + fit_len] = colored_block_sequence[:fit_len]
        # No need to update current_index further as this is the last element placed

    # Return the output row wrapped in a list
    return [output_row]