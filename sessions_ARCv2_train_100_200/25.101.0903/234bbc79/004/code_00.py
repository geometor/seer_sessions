import numpy as np

def get_neighbors(grid: np.ndarray, r: int, c: int) -> list[tuple[int, int, int]]:
    neighbours = []
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbours.append((grid[nr, nc], nr, nc))
    return neighbours

def analyze_example(name: str, grid_list: list[list[int]], expected_removed_cols: set[int]):
    print(f"--- {name} ---")
    input_array = np.array(grid_list, dtype=int)
    rows, cols = input_array.shape

    # Find bounding box
    non_white_coords = np.argwhere(input_array != 0)
    min_r, min_c, max_r, max_c = -1, -1, -1, -1
    has_bb = False
    if non_white_coords.size > 0:
        min_r = non_white_coords[:, 0].min()
        min_c = non_white_coords[:, 1].min()
        max_r = non_white_coords[:, 0].max()
        max_c = non_white_coords[:, 1].max()
        has_bb = True
        print(f"Bounding Box: r={min_r}-{max_r}, c={min_c}-{max_c}")
    else:
        print("No bounding box found.")

    predicted_removed_cols = set()
    gray_pixels_info = []

    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == 5: # Gray pixel
                neighbours = get_neighbors(input_array, r, c)
                colored_neighbours = [n for n in neighbours if n[0] != 0 and n[0] != 5]
                distinct_colors = set(n[0] for n in colored_neighbours)
                neighbor_color = 0
                if len(distinct_colors) == 1:
                     neighbor_color = list(distinct_colors)[0]
                
                is_strictly_inside = False
                if has_bb and min_r < r < max_r and min_c < c < max_c:
                    is_strictly_inside = True
                    predicted_removed_cols.add(c)
                
                gray_pixels_info.append({
                    "pos": (r, c),
                    "neighbor_color": neighbor_color,
                    "strictly_inside_bb": is_strictly_inside
                })

    print("Gray Pixels Analysis:")
    for info in gray_pixels_info:
        print(f"  G({info['pos'][0]},{info['pos'][1]}): NeighborColor={info['neighbor_color']}, StrictlyInsideBB={info['strictly_inside_bb']}")
    
    print(f"Predicted Removed Cols (Strictly Inside BB): {predicted_removed_cols}")
    print(f"Expected Removed Cols: {expected_removed_cols}")
    print(f"Match: {predicted_removed_cols == expected_removed_cols}")
    print("-" * (len(name) + 8))

# Define training examples and expected removals
train_examples = {
    "Example 1": {"in": [[0,0,0,0,0,0,5,0,0,0,0], [2,2,2,0,5,8,8,0,0,0,0], [0,0,5,0,0,0,0,0,5,6,6]], "remove": {4, 8}},
    "Example 2": {"in": [[0,0,0,5,1,5,0,0,0,0,0], [2,2,0,0,0,0,0,0,3,3,3], [0,5,0,0,0,0,0,5,3,0,0]], "remove": {3, 5}},
    "Example 3": {"in": [[0,1,5,0,0,0,0,0,2,2,0], [1,1,0,0,5,2,0,5,2,0,0], [0,0,0,0,0,5,0,0,0,0,0]], "remove": {4, 5, 7}}, # Assuming 4,5,7 removed
    "Example 4": {"in": [[0,5,0,0,0,0,0,0,0], [2,2,0,5,1,0,5,2,2], [0,0,0,0,5,0,0,0,0]], "remove": {3, 6}}
}

# Run analysis
for name, data in train_examples.items():
    analyze_example(name, data["in"], data["remove"])
