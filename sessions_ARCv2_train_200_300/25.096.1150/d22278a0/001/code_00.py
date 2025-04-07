"""
Transforms an input grid by "painting" cells based on the nearest non-zero source cell from the input, subject to a column parity constraint.

1. Identifies all non-zero "source" cells in the input grid, noting their value, coordinates, and column parity.
2. Initializes an output grid of the same dimensions as the input, filled with zeros.
3. For each cell in the grid:
   a. Calculates the Manhattan distance to all source cells.
   b. Finds the minimum distance.
   c. Identifies all source cells at that minimum distance.
   d. If exactly one source cell is closest:
      i. Checks if the current cell's column index has the same parity (even/odd) as the closest source cell's column index.
      ii. If the parities match, the output cell takes the value of the closest source cell.
   e. If there's a tie for the closest source cell, or if the single closest source doesn't match the column parity, the output cell remains zero.
4. Returns the painted output grid.
"""

import math

def manhattan_distance(r1: int, c1: int, r2: int, c2: int) -> int:
    """Calculates the Manhattan distance between two points."""
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the nearest-source painting rule with column parity constraint.
    """
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Find all source cells (non-zero values in input)
    # Store as (row, col, value, column_parity)
    sources = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] != 0:
                sources.append((r, c, input_grid[r][c], c % 2))

    # If there are no sources, return the zero grid
    if not sources:
        return output_grid

    # Iterate through each cell in the grid to determine its output value
    for tr in range(rows):
        for tc in range(cols):
            min_dist = float('inf')
            closest_sources = [] # Stores (value, source_col_parity) for tied sources

            # Calculate distance to each source
            for sr, sc, sv, sparity in sources:
                dist = manhattan_distance(tr, tc, sr, sc)

                # If this source is closer than the current minimum
                if dist < min_dist:
                    min_dist = dist
                    closest_sources = [(sv, sparity)] # Reset list with this source
                # If this source is equally close as the current minimum
                elif dist == min_dist:
                    closest_sources.append((sv, sparity)) # Add to list

            # Determine the output value based on closest sources and parity
            if len(closest_sources) == 1:
                source_value, source_col_parity = closest_sources[0]
                target_col_parity = tc % 2
                # Check if target column parity matches the unique closest source's column parity
                if target_col_parity == source_col_parity:
                    output_grid[tr][tc] = source_value
            # If there's a tie (len > 1) or no sources found (len == 0, though unlikely after initial check),
            # or if the unique closest source parity doesn't match, the cell remains 0 (already initialized).

    return output_grid