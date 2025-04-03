import numpy as np
from typing import List, Dict, Tuple

"""
Identifies two adjacent, non-background colored objects in a 1D grid. 
One object is a single pixel, and the other is a contiguous block.
The transformation swaps the positions of these two objects while preserving 
the background.
"""

def find_contiguous_objects(grid: List[int]) -> List[Dict]:
    """
    Finds all contiguous blocks of non-background (non-zero) pixels.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys 'color', 'start' (index), 'end' (index), and 'len'.
    """
    objects = []
    current_object = None
    for i, pixel in enumerate(grid):
        if pixel != 0:
            # Non-background pixel found
            if current_object is None:
                # Start of a new object
                current_object = {'color': pixel, 'start': i, 'count': 1}
            elif pixel == current_object['color']:
                # Continuation of the current object
                current_object['count'] += 1
            else:
                # Different color, end the previous object and start a new one
                current_object['end'] = i - 1
                current_object['len'] = current_object['end'] - current_object['start'] + 1
                # sanity check count vs len
                # assert current_object['len'] == current_object['count']
                objects.append(current_object)
                current_object = {'color': pixel, 'start': i, 'count': 1}
        else:
            # Background pixel found
            if current_object is not None:
                # End of the current object
                current_object['end'] = i - 1
                current_object['len'] = current_object['end'] - current_object['start'] + 1
                # assert current_object['len'] == current_object['count']
                objects.append(current_object)
                current_object = None # Reset

    # If the last pixel was part of an object, add it
    if current_object is not None:
        current_object['end'] = len(grid) - 1
        current_object['len'] = current_object['end'] - current_object['start'] + 1
        # assert current_object['len'] == current_object['count']
        objects.append(current_object)
        
    return objects

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input grid by swapping two adjacent non-background objects.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the 1D output grid with objects swapped.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid)

    # Find the non-background objects
    objects = find_contiguous_objects(input_grid)

    # Based on the examples, we expect exactly two adjacent objects
    # Add basic validation, though ARC tasks usually guarantee valid inputs
    if len(objects) != 2:
        # Or raise an error, but returning input copy might be safer for ARC runner
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning copy.")
        return output_grid 
        
    obj1 = objects[0]
    obj2 = objects[1]

    # Check for adjacency (optional but good practice)
    if obj1['end'] + 1 != obj2['start']:
         print(f"Warning: Objects are not adjacent. Obj1 ends at {obj1['end']}, Obj2 starts at {obj2['start']}. Returning copy.")
         return output_grid

    # Determine the starting position for the swap
    swap_start_index = obj1['start']

    # Place the second object (obj2) where the first object (obj1) was
    for i in range(obj2['len']):
        output_grid[swap_start_index + i] = obj2['color']

    # Place the first object (obj1) immediately after the new position of obj2
    for i in range(obj1['len']):
        output_grid[swap_start_index + obj2['len'] + i] = obj1['color']

    return output_grid