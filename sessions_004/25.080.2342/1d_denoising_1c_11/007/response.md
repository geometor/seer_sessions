```python
"""
1. Scan the input grid: Traverse the 1-dimensional grid (list) of digits.
2. Identify Runs:  Find "runs" of consecutive, identical, non-zero digits. A run is defined by its starting index, ending index, and the digit value.
3. Boundary Check:** For each identified run, check if it is "bounded."  A run is bounded if:
   - It is immediately preceded by a zero, or it starts at the beginning of the grid.
   - It is immediately followed by a zero, or it ends at the end of the grid.
4. Conditional Removal:** If a run is bounded, remove the entire run from the grid.
5. Output:** The modified grid, after removing all bounded runs, constitutes the output grid.
"""

def get_runs(grid):
    """Identifies runs of consecutive, identical, non-zero digits."""
    runs = []
    current_run = []
    for i, x in enumerate(grid):
        if x != 0:
            current_run.append((i, x))  # Store index and value
        else:
            if current_run:
                runs.append(current_run)
                current_run = []
    if current_run:  # Handle runs at the very end
        runs.append(current_run)
    return runs

def is_bounded(run, grid_length):
    """Checks if a run is bounded by zeros or grid edges."""
    start_index = run[0][0]
    end_index = run[-1][0]

    if start_index > 0 and grid_length > 0:
        if grid[start_index -1] != 0:
            return False
    if end_index < grid_length -1 and grid_length > 0:
        if grid[end_index + 1] !=0:
            return False
    return True

def transform(input_grid):
    """Transforms the input grid by removing bounded runs of non-zero digits."""

    # 1. & 2. Identify Runs
    runs = get_runs(input_grid)

    # Initialize output grid with all elements from the input (we'll remove elements later)
    output_grid = input_grid[:]  # Create a copy to avoid modifying the original

    # 3. & 4. Boundary Check and Conditional Removal
    offset = 0  # Keep track of how many elements we've removed
    for run in runs:
        if is_bounded(run, len(input_grid)):
            start_index = run[0][0]
            end_index = run[-1][0]
            # Adjust indices based on previously removed elements
            start_index -= offset
            end_index -= offset

            # Remove the run from the output_grid
            del output_grid[start_index : end_index + 1]
            # Update the offset
            offset += (end_index - start_index + 1)

    # 5. Output
    return output_grid
```