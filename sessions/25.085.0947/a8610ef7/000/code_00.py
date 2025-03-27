import numpy as np

def count_neighbors_detailed(grid, r, c):
    rows, cols = grid.shape
    cardinal_count = 0
    diagonal_count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 8:
                if dr == 0 or dc == 0: # Cardinal
                    cardinal_count += 1
                else: # Diagonal
                    diagonal_count += 1
    return cardinal_count, diagonal_count

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
            cardinal, diagonal = count_neighbors_detailed(input1, r, c)
            results.append(((r, c), cardinal, diagonal, output1[r, c]))

print("Example 1:")
print(results)

# Example 4 (for brevity)
input4 = np.array([
    [8, 8, 8, 0, 0, 0],
    [0, 0, 8, 8, 0, 8],
    [0, 8, 0, 0, 0, 0],
    [8, 8, 0, 0, 8, 8],
    [8, 0, 8, 8, 8, 8],
    [0, 0, 0, 0, 8, 8]
])

output4 = np.array([
    [5, 5, 5, 0, 0, 0],
    [0, 0, 2, 2, 0, 2],
    [0, 2, 0, 0, 0, 0],
    [5, 2, 0, 0, 5, 5],
    [5, 0, 2, 2, 5, 2],
    [0, 0, 0, 0, 5, 5]
])

results4 = []
rows, cols = input4.shape
for r in range(rows):
    for c in range(cols):
        if input4[r, c] == 8:
            cardinal, diagonal = count_neighbors_detailed(input4, r, c)
            results4.append(((r, c), cardinal, diagonal, output4[r, c]))

print("\nExample 4:")
print(results4)