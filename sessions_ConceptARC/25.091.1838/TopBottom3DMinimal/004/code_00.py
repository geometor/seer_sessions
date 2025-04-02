import numpy as np

def get_neighbors_coords(grid_shape, r, c):
    """Gets the coordinates of the 8 neighbors of a cell within grid bounds."""
    height, width = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def count_dominant_neighbors(grid, r, c, dominant_color):
    """Counts how many neighbors of (r, c) have the dominant color."""
    count = 0
    neighbor_coords = get_neighbors_coords(grid.shape, r, c)
    for nr, nc in neighbor_coords:
        if grid[nr, nc] == dominant_color:
            count += 1
    return count

# Example 1 Data
input1 = np.array([
    [2, 2, 2, 2, 2, 0, 0, 0],
    [2, 0, 3, 3, 2, 3, 3, 0],
    [2, 0, 3, 3, 2, 3, 3, 0],
    [2, 0, 3, 3, 2, 3, 3, 0],
    [2, 2, 2, 2, 2, 3, 3, 0],
    [0, 0, 3, 3, 3, 3, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
output1 = np.array([
    [2, 2, 2, 2, 2, 0, 0, 0],
    [2, 0, 3, 3, 3, 3, 3, 0],
    [2, 0, 3, 3, 3, 3, 3, 0],
    [2, 0, 3, 3, 3, 3, 3, 0],
    [2, 2, 3, 3, 3, 3, 3, 0],
    [0, 0, 3, 3, 3, 3, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
dominant1 = 3 # Green
recessive1 = 2 # Red
print("--- Example 1 Analysis (Dominant=3, Recessive=2) ---")
print(f"Pixels changed: {np.count_nonzero(input1 != output1)}")
changed_coords1 = np.argwhere(input1 != output1)
for r, c in changed_coords1:
     neighbors_count = count_dominant_neighbors(input1, r, c, dominant1)
     print(f"  Changed pixel ({r},{c}) [Color {input1[r,c]}->{output1[r,c]}]: Had {neighbors_count} dominant neighbors in input.")

print("\nChecking some non-changed recessive pixels:")
non_changed_coords1 = [(0,1), (0,2), (0,3), (0,4), (4,1)] # Add more if needed
for r, c in non_changed_coords1:
     if input1[r,c] == recessive1:
        neighbors_count = count_dominant_neighbors(input1, r, c, dominant1)
        print(f"  Non-changed pixel ({r},{c}) [Color {input1[r,c]}]: Had {neighbors_count} dominant neighbors in input.")


# Example 2 Data
input2 = np.array([
    [0, 0, 0, 0, 6, 6, 6, 6],
    [0, 0, 7, 7, 7, 7, 7, 6],
    [0, 0, 7, 0, 6, 6, 7, 6],
    [0, 0, 7, 7, 7, 7, 7, 6],
    [0, 0, 0, 0, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
output2 = np.array([
    [0, 0, 0, 0, 6, 6, 6, 6],
    [0, 0, 7, 7, 6, 6, 6, 6],
    [0, 0, 7, 0, 6, 6, 6, 6],
    [0, 0, 7, 7, 6, 6, 6, 6],
    [0, 0, 0, 0, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
dominant2 = 6 # Magenta
recessive2 = 7 # Orange
print("\n--- Example 2 Analysis (Dominant=6, Recessive=7) ---")
print(f"Pixels changed: {np.count_nonzero(input2 != output2)}")
changed_coords2 = np.argwhere(input2 != output2)
for r, c in changed_coords2:
     neighbors_count = count_dominant_neighbors(input2, r, c, dominant2)
     print(f"  Changed pixel ({r},{c}) [Color {input2[r,c]}->{output2[r,c]}]: Had {neighbors_count} dominant neighbors in input.")

print("\nChecking some non-changed recessive pixels:")
non_changed_coords2 = [(1,2), (1,3), (1,6), (2,2), (2,6), (3,2), (3,3), (3,6)] # Add more if needed
for r, c in non_changed_coords2:
     if input2[r,c] == recessive2:
        neighbors_count = count_dominant_neighbors(input2, r, c, dominant2)
        print(f"  Non-changed pixel ({r},{c}) [Color {input2[r,c]}]: Had {neighbors_count} dominant neighbors in input.")
