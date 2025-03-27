```python
import numpy as np
import math

"""
Identify the dominant non-white colors in the input grid. 
Calculate the average position (centroid) for each color.
Determine if the primary arrangement of these colors is vertical or horizontal by comparing the spread (range) of the average row coordinates versus the average column coordinates.
Sort the colors based on their average coordinates according to the determined orientation (top-to-bottom for vertical, left-to-right for horizontal).
Construct the output grid as a single column (Nx1 for vertical) or a single row (1xN for horizontal) containing the sorted colors.
"""

def get_unique_colors(grid):
    """Finds unique non-white colors in the grid."""
    unique_vals = np.unique(grid)
    return [color for color in unique_vals if color != 0]

def calculate_centroids(grid, colors):
    """Calculates the centroid (average row, average column) for each color."""
    centroids = {}
    for color in colors:
        coords = np.argwhere(grid == color)
        if coords.size > 0:
            avg_row = np.mean(coords[:, 0])
            avg_col = np.mean(coords[:, 1])
            centroids[color] = (avg_row, avg_col)
        else:
             # Should not happen if colors are derived from the grid, but safe fallback
             centroids[color] = (0, 0)
    return centroids

def determine_orientation(centroids):
    """Determines if the layout is primarily vertical or horizontal based on centroid spread."""
    if len(centroids) <= 1:
        # Default to vertical if only one color or no colors
        return 'vertical'

    rows = [centroid[0] for centroid in centroids.values()]
    cols = [centroid[1] for centroid in centroids.values()]

    row_range = np.ptp(rows) if len(rows) > 1 else 0 # Peak-to-peak (max - min)
    col_range = np.ptp(cols) if len(cols) > 1 else 0

    # If row spread is significantly larger than column spread, it's vertical.
    # Use a small epsilon to handle cases where one range is zero or very small.
    epsilon = 1e-6
    if row_range > col_range + epsilon:
        return 'vertical'
    # Otherwise, it's horizontal (including cases where ranges are equal or col_range is larger).
    else:
        return 'horizontal'


def transform(input_grid):
    """
    Transforms the input grid based on the spatial arrangement of dominant colors.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)

    # 1. Identify Unique Colors (excluding white/0)
    unique_colors = get_unique_colors(grid)

    # Handle edge cases: no non-white colors or only one
    if not unique_colors:
        # Or maybe return [[0]]? Task examples don't specify. Returning empty seems safer.
        return [] 
    if len(unique_colors) == 1:
        # Return a 1x1 grid with the single color
        return [[unique_colors[0]]]

    # 2. Calculate Centroids for each color
    centroids = calculate_centroids(grid, unique_colors)

    # 3. Determine Orientation (Vertical or Horizontal)
    orientation = determine_orientation(centroids)

    # 4. Sort Colors based on orientation
    if orientation == 'vertical':
        # Sort by average row index (top-to-bottom)
        sorted_colors = sorted(centroids.keys(), key=lambda color: centroids[color][0])
    else: # orientation == 'horizontal'
        # Sort by average column index (left-to-right)
        sorted_colors = sorted(centroids.keys(), key=lambda color: centroids[color][1])

    # 5. Construct Output Grid
    if orientation == 'vertical':
        # Create an Nx1 column vector
        output_grid_np = np.array(sorted_colors).reshape(-1, 1)
    else: # orientation == 'horizontal'
        # Create a 1xN row vector
        output_grid_np = np.array(sorted_colors).reshape(1, -1)

    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid
```