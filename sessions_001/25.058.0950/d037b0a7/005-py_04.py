import numpy as np
from typing import List, Tuple
from collections import Counter

def calculate_accuracy(predicted_grid: np.ndarray, target_grid: np.ndarray) -> float:
    """Calculates the pixel-wise accuracy between two grids."""
    if predicted_grid.shape != target_grid.shape:
        return 0.0
    correct_pixels = np.sum(predicted_grid == target_grid)
    total_pixels = predicted_grid.size
    return float(correct_pixels) / float(total_pixels)

def compare_grids(grid1: np.ndarray, grid2: np.ndarray) -> List[Tuple[Tuple[int, int], int, int]]:
    """
    Compares two grids and returns a list of differing pixels.
    Each tuple in the list contains: ((row, col), value_in_grid1, value_in_grid2)
    """
    if grid1.shape != grid2.shape:
        raise ValueError("Grids must have the same dimensions to compare.")

    differences = []
    for row in range(grid1.shape[0]):
        for col in range(grid1.shape[1]):
            if grid1[row, col] != grid2[row, col]:
                differences.append(((row, col), grid1[row, col], grid2[row, col]))
    return differences

def grid_to_string(grid: np.ndarray) -> str:
    """Converts a NumPy grid to a string representation."""
    return '\n'.join([' '.join(map(str, row)) for row in grid])

def get_objects(grid: np.ndarray) -> List[np.ndarray]:
    """
    Identifies contiguous objects (regions of the same color) within a grid.
    Returns a list of masks, one for each object.
    """
    
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return

        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                current_object = []
                dfs(row, col, color, current_object)
                if current_object:
                    mask = np.zeros_like(grid, dtype=bool)
                    for r, c in current_object:
                        mask[r, c] = True
                    objects.append(mask)
    return objects

def object_stats(grid, object_mask):
    """ compute stats on a masked object"""
    pixels = grid[object_mask]
    color_counts = Counter(pixels)
    most_common_color = color_counts.most_common(1)[0][0]
    min_row, min_col = grid.shape
    max_row, max_col = -1, -1

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if object_mask[row, col]:
                min_row = min(min_row, row)
                max_row = max(max_row, row)
                min_col = min(min_col, col)
                max_col = max(max_col, col)

    width = max_col - min_col + 1
    height = max_row - min_row + 1

    return {
        'min_row':min_row,
        'min_col': min_col,
        'max_row': max_row,
        'max_col': max_col,
        'width': width,
        'height': height,
        'most_common_color': most_common_color
    }