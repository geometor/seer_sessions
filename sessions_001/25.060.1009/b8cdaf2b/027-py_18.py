import numpy as np

def analyze_transform(input_grid, output_grid):
    # initialize output_grid
    analyzed_grid = np.copy(input_grid)
    height = input_grid.shape[0]
    width = input_grid.shape[1]

    # Find all yellow pixels
    yellow_pixels = []
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 4:
                yellow_pixels.append((r, c))

    # Group yellow pixels by column
    yellow_cols = {}
    for r, c in yellow_pixels:
        if c not in yellow_cols:
            yellow_cols[c] = []
        yellow_cols[c].append(r)

    # Determine target rows and place yellow pixels
    for col, rows in yellow_cols.items():
        min_row = min(rows)
        target_row_1 = min_row - 3
        target_row_2 = min_row - 2
        print(f"Column: {col}, Yellow Rows: {rows}, Min Row: {min_row}, Target Rows: {target_row_1}, {target_row_2}")

        # Check boundaries
        if 0 <= target_row_1 < height:
            analyzed_grid[target_row_1, col] = 4
        if 0 <= target_row_2 < height:
            analyzed_grid[target_row_2, col] = 4

    print(f"Input Grid:\n{input_grid}")
    print(f"Output Grid:\n{output_grid}")
    print(f"Analyzed:\n{analyzed_grid}")
    print(f"Match: {np.array_equal(analyzed_grid, output_grid)}")
    return np.array_equal(analyzed_grid, output_grid)

# Example usage with the training data (replace with actual data)
# ... (rest of the code to load and loop through examples)

# --- Example Usage (Illustrative, will use the actual ARC task data) ---
task = {
    "train": [
        {
            "input": np.array([[0, 0, 0], [0, 4, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]),
            "output": np.array([[0, 4, 0], [0, 4, 0], [0, 4, 0], [0, 0, 0], [0, 0, 0]]),
        },
        {
            "input": np.array([[0, 0, 0, 0], [0, 0, 4, 0], [0, 0, 0, 0], [4, 0, 0, 0]]),
            "output": np.array([[4, 0, 4, 0], [4, 0, 4, 0], [0, 0, 0, 0], [4, 0, 0, 0]]),
        },
         {
            "input": np.array([[0, 0, 0, 0], [0, 0, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0]]),
            "output": np.array([[4, 0, 4, 0], [4, 0, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0]]),
        }
    ]
}
results = []
for example in task["train"]:
    results.append(analyze_transform(example["input"], example["output"]))

print(results)