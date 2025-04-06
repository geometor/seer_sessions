import collections
import copy

def get_neighbors(grid: list[list[int]], r: int, c: int) -> list[int]:
    """
    Gets the values of the 8 neighbors for a given cell (r, c).
    Handles boundary conditions.
    """
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append(grid[nr][nc])
    return neighbors

def find_most_frequent(grid: list[list[int]]) -> int:
    """Finds the most frequent value in the grid."""
    counts = collections.Counter(val for row in grid for val in row)
    # Find the maximum frequency
    max_freq = 0
    if counts:
        max_freq = max(counts.values())
    
    # Find values with the maximum frequency
    most_frequent_values = [val for val, freq in counts.items() if freq == max_freq]
    
    # Tie-breaking: return the smallest value if there's a tie
    return min(most_frequent_values) if most_frequent_values else -1 # Or handle case with no elements? Assume grid is non-empty.


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the following rules:
    1. Find the globally most frequent number in the input grid (target_value).
    2. Iterate through each cell of the grid.
    3. If a cell's value is the target_value:
       a. Examine its 8 neighbors.
       b. Collect the values of neighbors that are *not* the target_value.
       c. Find the most frequent value among these valid neighbors (local_mode).
       d. If there is a unique local_mode:
          i. Apply a specific mapping based on the target_value and local_mode to get the replacement_value.
             - If target_value is 4: {2: 6, 5: 2, 6: 5}
             - If target_value is 0: {3: 9, 4: 3, 9: 4}
          ii. Replace the cell's value with the replacement_value.
       e. If there is no unique local_mode (no valid neighbors, or a tie for mode), the cell's value remains unchanged.
    4. Cells whose initial value is not the target_value remain unchanged.
    """
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = copy.deepcopy(input_grid)

    # Find the globally most frequent value (target_value)
    target_value = find_most_frequent(input_grid)

    # Define the replacement mappings based on target_value
    replacement_map = {}
    if target_value == 4:
        replacement_map = {2: 6, 5: 2, 6: 5}
    elif target_value == 0:
        replacement_map = {3: 9, 4: 3, 9: 4}
    # Add more mappings here if needed for other potential target values

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell's value is the target value
            if input_grid[r][c] == target_value:
                # Get neighbors
                all_neighbors = get_neighbors(input_grid, r, c)

                # Filter out neighbors that are the target value
                valid_neighbors = [n for n in all_neighbors if n != target_value]

                if not valid_neighbors:
                    continue # No valid neighbors, cell remains unchanged

                # Find the mode of the valid neighbors
                neighbor_counts = collections.Counter(valid_neighbors)
                max_freq = 0
                if neighbor_counts:
                    max_freq = max(neighbor_counts.values())

                modes = [val for val, freq in neighbor_counts.items() if freq == max_freq]

                # Check if there is a unique mode
                if len(modes) == 1:
                    local_mode = modes[0]
                    # Check if this local_mode has a mapping defined
                    if local_mode in replacement_map:
                        replacement_value = replacement_map[local_mode]
                        output_grid[r][c] = replacement_value
                # If there's a tie for mode or no valid neighbors, the cell value remains unchanged (already copied)

    return output_grid