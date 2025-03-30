import numpy as np
from typing import List, Tuple

"""
Transforms an input grid containing two colors, where one color forms separator lines (full rows or columns) and the other is the content color. 
The output grid's dimensions are determined by the number of separator lines plus one in each direction (height = horizontal lines + 1, width = vertical lines + 1). 
The output grid is filled entirely with the content color.
"""

def find_separator_and_content_colors(grid: np.ndarray) -> Tuple[int, int]:
    """
    Identifies the separator and content colors in a grid guaranteed to have exactly two colors.
    The separator color forms complete rows or columns.
    Returns:
        Tuple[int, int]: (separator_color, content_color)
    Raises:
        ValueError: If the input does not have exactly two colors or if separator/content colors cannot be determined.
    """
    unique_colors = np.unique(grid)
    if len(unique_colors) != 2:
         raise ValueError(f"Input grid expected 2 unique colors, but found {len(unique_colors)}: {unique_colors}")

    color1, color2 = unique_colors
    rows, cols = grid.shape

    separator_color = -1 # Sentinel value
    content_color = -1

    # Check rows first for potential horizontal separator lines
    for r in range(rows):
        if np.all(grid[r, :] == color1):
            separator_color = color1
            content_color = color2
            break
        if np.all(grid[r, :] == color2):
            separator_color = color2
            content_color = color1
            break

    # If no horizontal separator found, check columns for vertical separator lines
    if separator_color == -1:
        for c in range(cols):
            if np.all(grid[:, c] == color1):
                separator_color = color1
                content_color = color2
                break
            if np.all(grid[:, c] == color2):
                separator_color = color2
                content_color = color1
                break

    # If still not found (which shouldn't happen based on task description/examples)
    if separator_color == -1:
         raise ValueError("Could not determine separator and content colors based on full lines.")

    return separator_color, content_color

def count_separator_lines(grid: np.ndarray, separator_color: int) -> Tuple[int, int]:
    """
    Counts the number of horizontal and vertical separator lines of the specified color.
    Returns:
        Tuple[int, int]: (num_horizontal_separators, num_vertical_separators)
    """
    rows, cols = grid.shape
    num_h_sep = 0
    num_v_sep = 0

    # Count horizontal separators (full rows)
    for r in range(rows):
        if np.all(grid[r, :] == separator_color):
            num_h_sep += 1

    # Count vertical separators (full columns)
    for c in range(cols):
        if np.all(grid[:, c] == separator_color):
            num_v_sep += 1

    return num_h_sep, num_v_sep


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    1. Identifies separator and content colors.
    2. Counts horizontal and vertical separator lines.
    3. Calculates output dimensions: height=h_lines+1, width=v_lines+1.
    4. Creates an output grid of calculated dimensions filled with the content color.
    """
    # Convert input list of lists to a numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)

    # Step 1: Analyze the input grid to identify separator and content colors
    try:
        separator_color, content_color = find_separator_and_content_colors(grid_np)
    except ValueError as e:
        print(f"Error processing input grid: {e}")
        # Depending on requirements, might return input, empty list, or raise error
        return [] # Return empty list on error

    # Step 2: Count the number of horizontal and vertical separator lines
    num_h_sep, num_v_sep = count_separator_lines(grid_np, separator_color)

    # Step 3: Calculate the output grid dimensions
    # Height is number of horizontal separators + 1
    output_height = num_h_sep + 1
    # Width is number of vertical separators + 1
    output_width = num_v_sep + 1

    # Ensure dimensions are at least 1x1
    output_height = max(1, output_height)
    output_width = max(1, output_width)

    # Step 4: Construct the output grid filled with the content color
    output_grid_np = np.full((output_height, output_width), content_color, dtype=int)

    # Convert the numpy array back to a list of lists for the final output format
    output_grid = output_grid_np.tolist()

    return output_grid