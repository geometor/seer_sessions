# Tool Code Block Start - Metric Gathering (using previously defined function and inputs)
import copy
from collections import deque

# Function definition (copied from prompt)
def find_source_cells(grid: list[list[int]], source_value: int) -> list[tuple[int, int]]:
    sources = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == source_value:
                sources.append((r, c))
    return sources

def is_valid(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    if not input_grid or not input_grid[0]: return []
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = copy.deepcopy(input_grid)
    source_value = 3
    fillable_value = 7
    source_cells = find_source_cells(input_grid, source_value)
    queue = deque(source_cells)
    visited = set(source_cells)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc, rows, cols) and \
               (nr, nc) not in visited and \
               input_grid[nr][nc] == fillable_value:
                visited.add((nr, nc))
                output_grid[nr][nc] = source_value
                queue.append((nr, nc))
    return output_grid

# Inputs (copied from prompt)
input1 = [
    [8, 7, 7, 8, 7, 8, 7], [7, 8, 8, 7, 7, 7, 8], [7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8], [7, 7, 7, 7, 7, 8, 7], [3, 3, 7, 7, 8, 7, 7],
    [7, 7, 7, 8, 7, 7, 7]
]
input2 = [
    [7, 8, 7, 8, 7], [8, 7, 7, 7, 8], [7, 7, 7, 7, 7],
    [7, 3, 7, 7, 8], [7, 3, 7, 8, 7]
]
expected1 = [
    [8, 7, 7, 8, 7, 8, 7], [7, 8, 8, 3, 3, 3, 8], [7, 7, 7, 3, 7, 3, 7],
    [3, 3, 3, 3, 3, 3, 8], [7, 7, 7, 3, 7, 8, 7], [3, 3, 3, 3, 8, 7, 7],
    [7, 7, 7, 8, 7, 7, 7]
]
expected2 = [
    [7, 8, 7, 8, 7], [8, 3, 3, 3, 8], [7, 3, 7, 3, 7],
    [3, 3, 3, 3, 8], [7, 3, 7, 8, 7]
]

# Execute transformations
actual_output1 = transform(input1)
actual_output2 = transform(input2)

# Helper to count values
def count_values(grid):
    counts = {}
    for row in grid:
        for cell in row:
            counts[cell] = counts.get(cell, 0) + 1
    return counts

# Compare and print metrics
print("--- Example 1 Metrics ---")
print(f"Input Dimensions: {len(input1)}x{len(input1[0])}")
print(f"Output Dimensions: {len(actual_output1)}x{len(actual_output1[0])}")
print(f"Input Counts: {count_values(input1)}")
print(f"Expected Counts: {count_values(expected1)}")
print(f"Actual Counts: {count_values(actual_output1)}")
print(f"Matches Expected: {actual_output1 == expected1}")

print("\n--- Example 2 Metrics ---")
print(f"Input Dimensions: {len(input2)}x{len(input2[0])}")
print(f"Output Dimensions: {len(actual_output2)}x{len(actual_output2[0])}")
print(f"Input Counts: {count_values(input2)}")
print(f"Expected Counts: {count_values(expected2)}")
print(f"Actual Counts: {count_values(actual_output2)}")
print(f"Matches Expected: {actual_output2 == expected2}")

# Tool Code Block End