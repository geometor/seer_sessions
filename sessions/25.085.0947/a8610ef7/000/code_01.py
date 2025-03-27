import numpy as np

def count_neighbors_detailed(grid, r, c):
    rows, cols = grid.shape
    azure_neighbors = 0
    white_neighbors = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr, nc] == 8:
                    azure_neighbors += 1
                elif grid[nr, nc] == 0:
                    white_neighbors += 1
            # Implicitly handle boundary as non-neighbor
    return azure_neighbors, white_neighbors

# Example 1
input1 = np.array([
    [0, 8, 0, 8, 8, 8],
    [8, 8, 8, 8, 8, 0],
    [8, 0, 8, 0, 8, 0],
    [0, 8, 8, 8, 0, 8],
    [8, 8, 0, 8, 8, 0],
    [8, 8, 0, 0, 0, 8]
])

output1 = np.array([
    [0, 2, 0, 5, 5, 2],
    [2, 2, 5, 2, 2, 0],
    [5, 0, 2, 0, 5, 0],
    [0, 5, 2, 5, 0, 5],
    [2, 2, 0, 2, 2, 0],
    [5, 2, 0, 0, 0, 2]
])

results = []
rows, cols = input1.shape
for r in range(rows):
    for c in range(cols):
        if input1[r, c] == 8:
            azure_n, white_n = count_neighbors_detailed(input1, r, c)
            # Total neighbors = 8 - edge neighbors
            total_neighbors = 0
            for dr in [-1, 0, 1]:
                 for dc in [-1, 0, 1]:
                      if dr == 0 and dc == 0: continue
                      nr, nc = r + dr, c + dc
                      if 0 <= nr < rows and 0 <= nc < cols:
                           total_neighbors += 1

            # Check if sum matches
            # assert azure_n + white_n == total_neighbors
            results.append(((r, c), azure_n, white_n, output1[r, c]))

print("Example 1:")
print(results)