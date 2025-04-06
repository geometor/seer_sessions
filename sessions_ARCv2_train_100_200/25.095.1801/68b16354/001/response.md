```python
import numpy as np

def parse_grid(grid_str: str) -> list[list[int]]:
    """Parses a string representation of a grid into a list of lists of integers."""
    return [[int(x) for x in row.split()] for row in grid_str.strip().split('\n')]

def format_grid(grid: list[list[int]]) -> str:
    """Formats a list of lists of integers into a string representation."""
    return '\n'.join([' '.join(map(str, row)) for row in grid])

def transform_grid(grid: list[list[int]]) -> list[list[int]]:
    """
    Reverses the order of rows in the input grid.
    """
    # The input is a list of lists (rows).
    # Reversing the outer list effectively reverses the order of rows.
    # Slicing with [::-1] creates a reversed copy of the list.
    output_grid = grid[::-1]
    return output_grid

# Example usage (optional, for testing)
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
    input_grid_1 = parse_grid(input_str_1)
    output_grid_1 = transform_grid(input_grid_1)
    output_str_1 = format_grid(output_grid_1)
    print("Input 1:\n", input_str_1)
    print("Output 1:\n", output_str_1)
    print("Expected Output 1:\n", expected_output_str_1)
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
    input_grid_2 = parse_grid(input_str_2)
    output_grid_2 = transform_grid(input_grid_2)
    output_str_2 = format_grid(output_grid_2)
    print("Input 2:\n", input_str_2)
    print("Output 2:\n", output_str_2)
    print("Expected Output 2:\n", expected_output_str_2)
    assert output_str_2 == expected_output_str_2.strip()

    input_str_3 = """
2 7 4 3 4 8 3
2 3 7 1 2 3 3
8 7 4 3 2 2 4
1 1 2 1 4 4 7
2 4 3 1 1 4 1
4 8 7 4 4 8 2
7 3 8 4 3 2 8
"""
    expected_output_str_3 = """
7 3 8 4 3 2 8
4 8 7 4 4 8 2
2 4 3 1 1 4 1
1 1 2 1 4 4 7
8 7 4 3 2 2 4
2 3 7 1 2 3 3
2 7 4 3 4 8 3
"""
    input_grid_3 = parse_grid(input_str_3)
    output_grid_3 = transform_grid(input_grid_3)
    output_str_3 = format_grid(output_grid_3)
    print("Input 3:\n", input_str_3)
    print("Output 3:\n", output_str_3)
    print("Expected Output 3:\n", expected_output_str_3)
    assert output_str_3 == expected_output_str_3.strip()

```