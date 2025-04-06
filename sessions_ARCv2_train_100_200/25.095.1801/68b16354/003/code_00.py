import math
import numpy as np
from collections import Counter, defaultdict

"""
The transformation rule reverses the order of the rows in the input grid. 
The first row of the input becomes the last row of the output, the second row 
becomes the second-to-last row, and so on. The content and order of elements 
within each row remain unchanged.
"""

def parse_grid(grid_str: str) -> list[list[int]]:
    """Parses a string representation of a grid into a list of lists of integers."""
    # Split the input string into lines, handling potential leading/trailing whitespace.
    lines = grid_str.strip().split('\n')
    # For each line, split by space and convert each element to an integer.
    grid = [[int(x) for x in row.split()] for row in lines]
    return grid

def format_grid(grid: list[list[int]]) -> str:
    """Formats a list of lists of integers into a string representation."""
    # Convert each integer in a row to a string and join with spaces.
    # Join all formatted rows with newline characters.
    return '\n'.join([' '.join(map(str, row)) for row in grid])

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Reverses the order of rows in the input grid.

    Args:
        input_grid: A list of lists representing the input grid, where each inner 
                    list is a row of integers.

    Returns:
        A new list of lists representing the grid with the rows reversed.
    """
    # The input is a list of lists (rows).
    # Slicing with [::-1] creates a new list containing the elements
    # (rows in this case) of the original list in reverse order.
    output_grid = input_grid[::-1] 

    # Return the grid with rows reversed.
    return output_grid

# Note: In a typical execution environment for this type of problem,
# the main script would handle calling parse_grid, then transform,
# and finally format_grid. The transform function itself usually
# works directly with the parsed data structure (like list of lists).

# Example of how it might be used (for testing purposes):
if __name__ == "__main__":
    input_str_1 = """
7 3 3 1 2
1 8 2 4 1
2 7 8 7 2
7 7 4 1 8
8 1 7 7 1
"""
    expected_output_str_1 = """
8 1 7 7 1
7 7 4 1 8
2 7 8 7 2
1 8 2 4 1
7 3 3 1 2
"""
    # 1. Parse
    parsed_input_1 = parse_grid(input_str_1)
    
    # 2. Transform
    transformed_grid_1 = transform(parsed_input_1)
    
    # 3. Format
    output_str_1 = format_grid(transformed_grid_1)
    
    print("Input 1:\n", input_str_1.strip())
    print("Output 1:\n", output_str_1)
    print("Expected Output 1:\n", expected_output_str_1.strip())
    assert output_str_1 == expected_output_str_1.strip()

    input_str_2 = """
8 1 2 1 4
4 4 2 4 8
3 7 2 4 8
2 7 7 8 7
8 7 7 4 8
"""
    expected_output_str_2 = """
8 7 7 4 8
2 7 7 8 7
3 7 2 4 8
4 4 2 4 8
8 1 2 1 4
"""
    parsed_input_2 = parse_grid(input_str_2)
    transformed_grid_2 = transform(parsed_input_2)
    output_str_2 = format_grid(transformed_grid_2)
    print("\nInput 2:\n", input_str_2.strip())
    print("Output 2:\n", output_str_2)
    print("Expected Output 2:\n", expected_output_str_2.strip())
    assert output_str_2 == expected_output_str_2.strip()