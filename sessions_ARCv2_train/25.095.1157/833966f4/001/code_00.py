import math

"""
Takes a list of lists (representing rows of single integers) and rearranges the rows by swapping adjacent pairs. If the number of rows is odd, the last row remains in its position after the pairs are swapped.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rearranges the rows of the input grid by swapping adjacent pairs.

    Args:
        input_grid: A list of lists, where each inner list represents a row
                      containing a single integer.

    Returns:
        A new list of lists representing the grid with adjacent rows swapped.
    """
    
    # Initialize the output grid
    output_grid = []
    
    # Get the number of rows in the input grid
    num_rows = len(input_grid)
    
    # Initialize the index for iteration
    i = 0
    
    # Iterate through the input grid rows with a step of 2
    while i < num_rows:
        # Check if there is a next row to form a pair (i + 1 exists)
        if i + 1 < num_rows:
            # Select the pair of rows
            row1 = input_grid[i]
            row2 = input_grid[i+1]
            
            # Swap the pair and append to the output grid
            output_grid.append(row2) # Append the second element of the pair first
            output_grid.append(row1) # Append the first element of the pair second
            
            # Move the index forward by 2 to process the next pair
            i += 2
        else:
            # Handle the last row if the total number of rows is odd
            # This row has no pair to swap with
            last_row = input_grid[i]
            output_grid.append(last_row)
            
            # Move the index forward by 1 to exit the loop
            i += 1
            
    # Return the transformed grid
    return output_grid
