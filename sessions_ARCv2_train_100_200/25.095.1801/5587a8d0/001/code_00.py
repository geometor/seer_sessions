import collections
import numpy as np

def get_background_value(grid: list[list[int]]) -> int:
    """Finds the most frequent value in the grid."""
    counts = collections.Counter(item for row in grid for item in row)
    # Find the element with the maximum count
    if not counts:
        # Handle empty grid case if necessary, though examples suggest non-empty
        return -1 # Or raise an error
    background_val = counts.most_common(1)[0][0]
    return background_val

def get_foreground_counts(grid: list[list[int]], background_val: int) -> dict[int, int]:
    """Counts the frequency of non-background values."""
    counts = collections.Counter()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            val = grid[r][c]
            if val != background_val:
                counts[val] += 1
    return dict(counts)

def sort_foreground_values(foreground_counts: dict[int, int]) -> list[int]:
    """
    Sorts foreground values.
    Primary sort key: count (descending).
    Secondary sort key: value (descending).
    """
    # Create a list of tuples (value, count)
    items = list(foreground_counts.items())
    # Sort the list: first by count descending (-x[1]), then by value descending (-x[0])
    items.sort(key=lambda x: (-x[1], -x[0]))
    # Return just the sorted values
    return [item[0] for item in items]

def fill_layer(grid: np.ndarray, layer_index: int, value: int):
    """Fills the specified concentric layer of the grid with the given value."""
    n = grid.shape[0]
    # Top row
    for c in range(layer_index, n - layer_index):
        grid[layer_index, c] = value
    # Bottom row
    for c in range(layer_index, n - layer_index):
        grid[n - 1 - layer_index, c] = value
    # Left column (excluding corners already filled)
    for r in range(layer_index + 1, n - 1 - layer_index):
        grid[r, layer_index] = value
    # Right column (excluding corners already filled)
    for r in range(layer_index + 1, n - 1 - layer_index):
        grid[r, n - 1 - layer_index] = value


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the frequency and value of non-background numbers.

    1.  Find the most frequent number (background).
    2.  Count frequencies of all other (foreground) numbers.
    3.  Sort foreground numbers: descending by frequency, then descending by value.
    4.  Create an output grid of size N = 2 * k - 1, where k is the number of unique foreground numbers.
    5.  Fill the output grid with concentric square layers using the sorted foreground numbers,
        starting with the first sorted number for the outermost layer and moving inwards.
    """
    if not input_grid or not input_grid[0]:
        return []

    # 1. Find the background value
    background_val = get_background_value(input_grid)

    # 2. Count foreground values
    foreground_counts = get_foreground_counts(input_grid, background_val)

    # Handle case where there are no foreground elements
    if not foreground_counts:
         # Decide on behavior: empty grid, grid of background, etc.
         # Based on examples, seems there's always foreground. Let's assume k >= 1.
         # If k=0 was possible, we'd need a specific rule. Returning 1x1 grid of background?
         # For now, assume k>=1 as per examples.
         # Or maybe return a single cell with the most common element if *only* one exists?
         # Let's proceed assuming k >= 1 based on given examples.
         # If we only had background, maybe return [[background_val]]? Let's handle that edge case.
         all_values = [item for row in input_grid for item in row]
         if len(set(all_values)) <= 1:
             return [[background_val]] # Or based on specific requirement for this case


    # 3. Sort foreground values
    sorted_foreground_values = sort_foreground_values(foreground_counts)
    num_foreground = len(sorted_foreground_values)

    # Handle the edge case again if sorting resulted in empty list (shouldn't happen if foreground_counts wasn't empty)
    if num_foreground == 0:
         # This case implies only background exists.
         return [[background_val]]


    # 4. Determine output grid size
    output_size = 2 * num_foreground - 1

    # 5. Create and fill the output grid
    # Initialize with a placeholder, e.g., -1, or the innermost value immediately
    # The innermost value is the last one in the sorted list
    innermost_value = sorted_foreground_values[-1]
    output_grid_np = np.full((output_size, output_size), innermost_value, dtype=int)

    # Fill layers from outermost (index 0) inwards
    num_layers = num_foreground # Same as the number of unique foreground values
    for layer_index in range(num_layers):
        value_for_layer = sorted_foreground_values[layer_index]
        fill_layer(output_grid_np, layer_index, value_for_layer)

    # Convert numpy array back to list of lists
    output_grid = output_grid_np.tolist()

    return output_grid