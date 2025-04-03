import math

"""
Processes a grid represented as a multi-line string.
Identifies the unique non-zero integer within the grid.
Finds the middle row of the grid.
Counts the occurrences of the unique non-zero integer in the middle row.
Returns a string consisting of the unique non-zero integer repeated that many times, separated by spaces.
"""

def parse_input_string(input_str):
    """Converts a multi-line string representation of a grid into a 2D list of integers."""
    grid = []
    lines = input_str.strip().split('\n')
    for line in lines:
        row = [int(x) for x in line.split()]
        grid.append(row)
    return grid

def find_unique_non_zero(grid):
    """Finds the unique non-zero integer value present in the grid."""
    non_zero_val = 0
    for row in grid:
        for cell in row:
            if cell != 0:
                # Assume the first non-zero value found is the unique one
                # based on the problem description.
                non_zero_val = cell
                return non_zero_val 
    return non_zero_val # Should ideally not be reached if input follows pattern

def find_center_row(grid):
    """Identifies and returns the middle row of the grid."""
    num_rows = len(grid)
    center_row_index = math.floor(num_rows / 2)
    return grid[center_row_index]

def count_value_in_row(row, value):
    """Counts the occurrences of a specific value in a row (list)."""
    count = 0
    for item in row:
        if item == value:
            count += 1
    return count

def generate_output_string(value, count):
    """Generates the output string by repeating the value 'count' times, space-separated."""
    if count <= 0:
        return ""
    output_list = [str(value)] * count
    return " ".join(output_list)

def transform(input_str):
    """
    Transforms the input grid string according to the identified rule.
    """
    # Parse the input string into a 2D list of integers
    input_grid = parse_input_string(input_str)
    
    # Identify the unique non-zero target value in the grid
    target_value = find_unique_non_zero(input_grid)
    
    # Find the middle row of the grid
    center_row = find_center_row(input_grid)
    
    # Count how many times the target value appears in the center row
    repeat_count = count_value_in_row(center_row, target_value)
    
    # Generate the final output string
    output_string = generate_output_string(target_value, repeat_count)
    
    return output_string