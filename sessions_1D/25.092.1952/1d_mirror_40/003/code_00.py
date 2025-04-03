import numpy as np # Although core logic uses lists, numpy might be useful for grid operations if needed later.

"""
Reposition a sequence of colored pixels within a 1D array based on its spatial relationship to a fixed maroon pixel. The operation resembles reflecting the sequence's end position across the maroon pixel to determine its new start position.

1. Assume the input is a one-dimensional array (list) of pixels.
2. Create a new output array of the same size as the input, initially filled with white pixels (0).
3. Find the index of the single maroon pixel (9) in the input array; let this be `maroon_index`. Place a maroon pixel (9) at `maroon_index` in the output array.
4. Identify the contiguous sequence of non-white (0), non-maroon (9) pixels in the input array. Record its color (`sequence_color`), its ending index (`input_end_index`), and its length (`sequence_length`).
5. Calculate the spatial distance (`d`) between the end of the input sequence and the maroon pixel: `d = maroon_index - input_end_index`. This represents the number of pixels strictly between the sequence and the pivot.
6. Calculate the starting index for the sequence in the output array (`output_start_index`) by adding this distance `d` to the maroon pixel's index: `output_start_index = maroon_index + d`.
7. Place the colored sequence into the output array: starting at `output_start_index`, fill the next `sequence_length` positions with the `sequence_color`. Ensure array bounds are respected and that the maroon pixel at `maroon_index` is not overwritten if an overlap were theoretically possible.
"""


def find_pivot(grid_list):
    """Finds the index of the pivot marker (9)."""
    for i, pixel in enumerate(grid_list):
        if pixel == 9:
            return i
    return -1 # Pivot not found


def find_colored_sequence(grid_list):
    """Finds the color, start index, end index, and length of the colored sequence."""
    start_index = -1
    end_index = -1
    sequence_color = -1
    length = 0
    in_sequence = False

    for i, pixel in enumerate(grid_list):
        # Detect start of a potential sequence
        if not in_sequence and pixel != 0 and pixel != 9:
            start_index = i
            sequence_color = pixel
            length = 1
            in_sequence = True
        # Continue the current sequence
        elif in_sequence and pixel == sequence_color:
            length += 1
        # End the sequence if a different pixel is found
        elif in_sequence and pixel != sequence_color:
            end_index = i - 1
            return sequence_color, start_index, end_index, length

    # Handle case where sequence runs to the end of the grid
    if in_sequence:
        end_index = len(grid_list) - 1
        return sequence_color, start_index, end_index, length

    # Sequence not found
    return -1, -1, -1, 0


def transform(input_grid):
    """
    Transforms the input grid by repositioning the colored sequence relative
    to the maroon pivot marker.
    """
    # Ensure input is treated as a flat list
    # If input_grid is a numpy array (e.g., shape (1, N)), flatten it.
    if hasattr(input_grid, 'flatten'):
         input_list = list(input_grid.flatten())
    else:
         # Assume it's already list-like
         input_list = list(input_grid)

    grid_size = len(input_list)

    # Initialize output_grid with white (0)
    output_grid = [0] * grid_size

    # Locate the pivot marker (maroon, 9)
    maroon_index = find_pivot(input_list)
    if maroon_index == -1:
        # If no pivot, maybe return original or empty grid? Returning initialized grid for now.
        print("Warning: Pivot marker (9) not found.")
        return output_grid 
    
    # Place the pivot marker in the output
    output_grid[maroon_index] = 9

    # Locate the colored sequence
    sequence_color, input_start_index, input_end_index, sequence_length = find_colored_sequence(input_list)

    # Proceed only if a sequence was found
    if sequence_color != -1:
        # Calculate the distance from the end of the input sequence to the pivot
        # This is the number of cells *between* the sequence end and the pivot
        distance = maroon_index - input_end_index

        # Calculate the new start index for the sequence in the output
        # The sequence starts 'distance' cells *after* the pivot
        output_start_index = maroon_index + distance

        # Place the colored sequence in the output grid
        for i in range(sequence_length):
            current_output_index = output_start_index + i
            # Check array bounds before writing
            if 0 <= current_output_index < grid_size:
                # Check if the target cell is currently empty (white)
                # This prevents overwriting the pivot if they would overlap
                if output_grid[current_output_index] == 0:
                    output_grid[current_output_index] = sequence_color
                # else: # Optional: handle potential overlap case if needed
                #    print(f"Warning: Skipped writing sequence color {sequence_color} at index {current_output_index} due to existing pixel {output_grid[current_output_index]}.")
            # else: # Optional: handle out-of-bounds case if needed
            #    print(f"Warning: Skipped writing sequence color {sequence_color} at index {current_output_index} - out of bounds.")

    # Return the resulting grid as a list
    return output_grid