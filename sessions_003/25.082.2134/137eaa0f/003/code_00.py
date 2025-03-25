"""
Extracts colored pixels along diagonals from the input grid, consolidates
adjacent pixels of the same color, and arranges these consolidated sequences
into a 3x3 output grid, preserving diagonal order and padding with zeros if
necessary.
"""

import numpy as np

def get_diagonals(input_grid):
    """
    Extracts diagonals from the input grid.
    """
    diagonals = []
    rows, cols = input_grid.shape
    for i in range(rows + cols - 1):
        diagonal = []
        for j in range(max(0, i - rows + 1), min(i + 1, cols)):
            row = i - j
            col = j
            diagonal.append(input_grid[row, col])
        diagonals.append(diagonal)
    return diagonals

def consolidate_diagonal(diagonal):
    """
    Consolidates adjacent pixels of the same color in a diagonal.
    """
    consolidated = []
    if diagonal:
        current_pixel = diagonal[0]
        current_sequence = [current_pixel]
        for pixel in diagonal[1:]:
            if pixel == current_pixel:
                current_sequence.append(pixel)
            else:
                consolidated.append(current_sequence)
                current_pixel = pixel
                current_sequence = [current_pixel]
        consolidated.append(current_sequence)  # Add the last sequence
    return consolidated

def transform(input_grid):
    """
    Transforms the input grid by extracting and consolidating diagonals.
    """
    # Initialize the output grid as a 3x3 array filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Extract diagonals from the input grid
    diagonals = get_diagonals(input_grid)
    
    # Get first three non-zero starting diagonals
    
    output_diagonals = []
    
    for diag in diagonals:
        if any(pixel != 0 for pixel in diag):
            output_diagonals.append(diag)
            if len(output_diagonals) >= 3:
              break;

    # Consolidate each diagonal
    consolidated_diagonals = [consolidate_diagonal(d) for d in output_diagonals]

    # Flatten consolidated lists and keep non-zero pixels, respecting original order within diagonals, and remove empty lists
    consolidated_diag_pixels = []

    for diag in consolidated_diagonals:
      for sublist in diag:
        if any(pixel != 0 for pixel in sublist):
          consolidated_diag_pixels.append([pixel for pixel in sublist if pixel != 0])


    # Fill the output grid
    row = 0
    for diag_pixels in consolidated_diag_pixels:
        if row < 3:
          col = 0
          for pixel in diag_pixels:
            if col < 3:
                output_grid[row, col] = pixel
            col += 1

        row += 1
    return output_grid