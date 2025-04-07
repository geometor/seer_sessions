import copy

"""
Transforms an input grid of integers based on row index and the value of the first element in odd-indexed rows.

1.  Iterate through each row of the input grid along with its index.
2.  If the row index is even, the row remains unchanged.
3.  If the row index is odd:
    a.  Check the value of the first element (at index 0).
    b.  If the first element is 7, perform a right circular shift on the elements at indices 1, 2, and 3. The element originally at index 3 moves to 1, 1 moves to 2, and 2 moves to 3. Other elements remain in place.
    c.  If the first element is 5, perform a right circular shift on the elements at indices 0, 1, and 2. The element originally at index 2 moves to 0, 0 moves to 1, and 1 moves to 2. Other elements remain in place.
4.  Construct the output grid using the original even rows and the modified odd rows.
"""

def right_circular_shift(segment: list[int]) -> list[int]:
    """Performs a right circular shift on a list segment."""
    if not segment:
        return []
    # Take the last element and put it at the front, followed by the rest
    return [segment[-1]] + segment[:-1]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = [] # Initialize an empty list for the output grid

    # Iterate through each row and its index in the input grid
    for i, row in enumerate(input_grid):
        # Create a copy of the current row to potentially modify
        # This ensures the original input_grid is not changed if it's mutable
        current_output_row = list(row) 

        # Check if the row index is odd
        if i % 2 != 0:
            # Handle odd rows based on the value of the first element
            if len(row) > 0: # Ensure row is not empty
                first_element = row[0]

                if first_element == 7:
                    # Check if row is long enough for the shift (indices 1, 2, 3)
                    if len(row) >= 4:
                        # Extract the segment to be shifted
                        segment_to_shift = [row[1], row[2], row[3]]
                        # Perform the right circular shift
                        shifted_segment = right_circular_shift(segment_to_shift)
                        # Update the current output row with the shifted segment
                        current_output_row[1] = shifted_segment[0]
                        current_output_row[2] = shifted_segment[1]
                        current_output_row[3] = shifted_segment[2]
                elif first_element == 5:
                     # Check if row is long enough for the shift (indices 0, 1, 2)
                    if len(row) >= 3:
                         # Extract the segment to be shifted
                        segment_to_shift = [row[0], row[1], row[2]]
                        # Perform the right circular shift
                        shifted_segment = right_circular_shift(segment_to_shift)
                        # Update the current output row with the shifted segment
                        current_output_row[0] = shifted_segment[0]
                        current_output_row[1] = shifted_segment[1]
                        current_output_row[2] = shifted_segment[2]
            # If the odd row doesn't meet conditions (e.g., too short, first element not 5 or 7), 
            # it remains unchanged (as per current_output_row initialization)
            
        # Append the (potentially modified) row to the output grid
        output_grid.append(current_output_row)
        # If the row index was even, current_output_row is just a copy of the original row

    # Return the completed output grid
    return output_grid
