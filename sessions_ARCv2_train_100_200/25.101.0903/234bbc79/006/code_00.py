import numpy as np

def get_neighbors(grid: np.ndarray, r: int, c: int, connectivity=8):
    """Gets neighbours (value, row, col) of a pixel at (r, c)."""
    neighbours = []
    rows, cols = grid.shape
    if connectivity == 8:
        deltas = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    else: # connectivity 4
        deltas = [(-1,0), (0,-1), (0,1), (1,0)]

    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbours.append((grid[nr, nc], nr, nc))
    return neighbours

def analyze_bridging(name: str, grid_list: list[list[int]], expected_removed_cols: set[int]):
    print(f"--- {name} ---")
    input_array = np.array(grid_list, dtype=int)
    rows, cols = input_array.shape

    predicted_removed_cols = set()
    gray_pixels_info = []

    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == 5: # Gray pixel
                # Find unique DIRECT non-white/non-gray neighbor color C
                direct_neighbors = get_neighbors(input_array, r, c, connectivity=8)
                colored_direct_neighbors = [n for n in direct_neighbors if n[0] != 0 and n[0] != 5]
                distinct_direct_colors = set(n[0] for n in colored_direct_neighbors)

                unique_neighbor_color = -1 # Sentinel value for no single unique color / isolated
                if len(distinct_direct_colors) == 1:
                    unique_neighbor_color = list(distinct_direct_colors)[0]
                elif len(distinct_direct_colors) > 1:
                     # This case didn't happen before, but flag if it does
                     unique_neighbor_color = -99 # Error/unexpected case flag
                # If len is 0, unique_neighbor_color remains -1

                # Bridging Check: Is GP adjacent (conn=8) to ANY pixel P whose color Cp is non-white/non-gray AND Cp != unique_neighbor_color?
                is_bridging = False
                for val_p, r_p, c_p in direct_neighbors:
                    # Check if neighbor P itself is colored and different from C
                    # Handle case where C might be -1 (GP has no colored neighbors)
                    if val_p != 0 and val_p != 5:
                        if unique_neighbor_color == -1 or val_p != unique_neighbor_color:
                             is_bridging = True
                             break

                if is_bridging:
                    predicted_removed_cols.add(c)

                gray_pixels_info.append({
                    "pos": (r, c),
                    "direct_neighbor_color": unique_neighbor_color,
                    "is_bridging": is_bridging
                })

    print("Gray Pixels Bridging Analysis:")
    for info in gray_pixels_info:
        print(f"  G({info['pos'][0]},{info['pos'][1]}): DirectColor={info['direct_neighbor_color']}, Bridging={info['is_bridging']}")

    print(f"Predicted Removed Cols (Bridging Rule): {predicted_removed_cols}")
    print(f"Expected Removed Cols: {expected_removed_cols}")
    print(f"Match: {predicted_removed_cols == expected_removed_cols}")
    print("-" * (len(name) + 8))

# Define training examples and expected removals
train_examples = {
    "Example 1": {"in": [[0,0,0,0,0,0,5,0,0,0,0], [2,2,2,0,5,8,8,0,0,0,0], [0,0,5,0,0,0,0,0,5,6,6]], "remove": {4, 8}},
    "Example 2": {"in": [[0,0,0,5,1,5,0,0,0,0,0], [2,2,0,0,0,0,0,0,3,3,3], [0,5,0,0,0,0,0,5,3,0,0]], "remove": {3, 5}},
    "Example 3": {"in": [[0,1,5,0,0,0,0,0,2,2,0], [1,1,0,0,5,2,0,5,2,0,0], [0,0,0,0,0,5,0,0,0,0,0]], "remove": {4, 5, 7}},
    "Example 4": {"in": [[0,5,0,0,0,0,0,0,0], [2,2,0,5,1,0,5,2,2], [0,0,0,0,5,0,0,0,0]], "remove": {3, 6}}
}

# Run analysis
for name, data in train_examples.items():
    analyze_bridging(name, data["in"], data["remove"])