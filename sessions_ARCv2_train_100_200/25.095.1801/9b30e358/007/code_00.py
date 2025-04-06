import math # Not strictly needed here, but good practice to import potential libraries

"""
Transforms an input grid (provided as a list of lists of integers) based on the 
parity of its height (number of rows).

If the input grid's height (H) is odd, the output grid is formed by 
vertically stacking the input grid on top of itself.

If the input grid's height (H) is even, the grid is conceptually split into a 
top half (first H/2 rows) and a bottom half (last H/2 rows). The output grid 
is constructed by vertically stacking these halves in the sequence: 
BottomHalf, TopHalf, BottomHalf, TopHalf, BottomHalf.
"""

# No specific imports needed beyond standard list operations

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the height-parity based stacking transformation to the input grid.

    Args:
        input_grid: A list of lists of integers representing the grid.

    Returns:
        A new list of lists of integers representing the transformed grid.
    """
    # Initialize output_grid as an empty list
    output_grid = []

    # Determine the height (number of rows) of the input grid
    h = len(input_grid)

    # Handle the edge case of an empty input grid
    if h == 0:
        return [] # Return an empty list if the input is empty

    # Check if the height H is odd or even
    if h % 2 != 0:
        # --- Odd height case ---
        # Vertically stack the input_grid with itself
        # List concatenation achieves vertical stacking for list of lists
        output_grid = input_grid + input_grid
    else:
        # --- Even height case ---
        # Calculate the midpoint row index (integer division)
        midpoint = h // 2
        
        # Create the TopHalf by slicing the input grid
        top_half = input_grid[:midpoint]
        
        # Create the BottomHalf by slicing the input grid
        bottom_half = input_grid[midpoint:]

        # Construct the OutputGrid by concatenating the halves in the sequence:
        # BottomHalf, TopHalf, BottomHalf, TopHalf, BottomHalf
        output_grid = bottom_half + top_half + bottom_half + top_half + bottom_half

    # Return the final constructed output grid
    return output_grid