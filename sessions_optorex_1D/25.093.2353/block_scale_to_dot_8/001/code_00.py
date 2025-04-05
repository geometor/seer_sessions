import math 
import collections 

def transform(input_grid):
    """
    Transforms the input sequence by finding a boundary marker '2' and a contiguous block
    of another non-zero digit ('fill_number'). It then fills any zeros ('0') located
    strictly between the '2' and the edge of the 'fill_number' block closest to '2'
    with the 'fill_number'. If the block is already adjacent to '2' or if no such
    block exists, the sequence remains unchanged.
    """
    # Initialize output_grid as a mutable copy (list) of the input
    # Assuming input_grid is already a list or tuple of integers
    output_grid = list(input_grid)
    n = len(output_grid)

    # 1. Locate the unique boundary marker digit '2'
    try:
        marker_index = output_grid.index(2)
    except ValueError:
        # If marker '2' is not found, return the original grid unchanged
        # This case might not occur based on examples, but good for robustness.
        return output_grid

    # 2. Identify the 'fill_number' and its edge index closest to the marker
    fill_number = None
    fill_edge_index = -1 # Index of the digit in the fill block closest to the marker
    min_distance = float('inf')

    # Search left of the marker for the nearest non-zero, non-2 digit
    # Iterate from the index immediately left of the marker towards the beginning
    for i in range(marker_index - 1, -1, -1):
        # Check if the current element is a potential fill number
        if output_grid[i] != 0 and output_grid[i] != 2:
            # Found the first relevant digit block edge to the left
            distance = marker_index - i
            # Since we search outwards, this is automatically the closest on this side
            min_distance = distance
            fill_number = output_grid[i] # Record the fill number
            fill_edge_index = i          # Record the index of this edge
            break # Stop searching left once the first block edge is found

    # Search right of the marker for the nearest non-zero, non-2 digit
    # Iterate from the index immediately right of the marker towards the end
    for i in range(marker_index + 1, n):
         # Check if the current element is a potential fill number
         if output_grid[i] != 0 and output_grid[i] != 2:
            # Found the first relevant digit block edge to the right
            distance = i - marker_index
            # Check if this block on the right is closer than the one found on the left (if any)
            # If a block was found on the left, min_distance holds its distance.
            # If no block was found left, min_distance is still inf.
            if distance < min_distance:
                min_distance = distance      # Update minimum distance
                fill_number = output_grid[i] # Update the fill number
                fill_edge_index = i          # Update the edge index
            # Stop searching right once the first block edge is found, 
            # regardless of distance comparison result. We only care about the first block encountered
            # on each side and then compare their distances.
            break 

    # 3. If no fill number was found nearby (i.e., fill_number is still None), 
    # return the grid unchanged.
    if fill_number is None:
        return output_grid

    # 4. Determine the range of indices to fill.
    # This range is strictly *between* the marker and the identified fill edge.
    # The start index is one position after the element closer to the beginning of the list.
    # The end index is the index of the element further down the list (exclusive for range()).
    start_fill = min(marker_index, fill_edge_index) + 1
    end_fill = max(marker_index, fill_edge_index)

    # 5. Iterate through the determined range and fill zeros with the fill_number.
    # The loop range(start_fill, end_fill) will be empty if start_fill >= end_fill,
    # which correctly handles cases where the fill block is already adjacent to the marker.
    for i in range(start_fill, end_fill):
        # If the element within the gap is a zero, replace it with the fill number
        if output_grid[i] == 0:
            output_grid[i] = fill_number

    # 6. Return the modified sequence
    return output_grid