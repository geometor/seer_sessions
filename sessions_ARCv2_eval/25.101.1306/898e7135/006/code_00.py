import numpy as np
from collections import Counter

# --- Constants based on H6 ---
BASE_CONTENT_COLORS = {1, 2, 3, 4, 5, 6, 9}
ORANGE_COLOR = 7
AZURE_COLOR = 8
BACKGROUND_PIXEL = 0

# --- Input Data ---
grid1_str = """
2 2 2 2 2 2 0 0 7 0 0 0 0 0 0
2 0 0 2 0 2 0 0 0 0 0 0 0 0 0
2 0 2 2 2 2 0 0 0 0 0 0 0 0 0
2 2 2 2 0 2 0 0 0 8 8 0 0 7 0
2 2 0 0 0 2 0 0 0 8 8 0 0 0 0
2 2 2 2 2 2 0 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 0 7 0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 7 0 0 0 0 0 0 3 3 0 0 0 7
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 0 0
"""
grid1 = np.array([list(map(int, row.split())) for row in grid1_str.strip().split('\n')])
expected_output_colors1 = {1, 2, 3, 8} # Including background

grid2_str = """
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 3 3 3 3
0 0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 5 5 0 0 3 0 3 3 3 0 0 0 0 3
0 8 0 0 0 1 1 1 1 1 1 1 1 0 0 0 5 5 0 0 3 3 3 3 3 3 3 3 0 3
0 0 0 0 0 0 0 1 1 0 0 1 1 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 1 1 0 0 1 1 0 0 0 0 0 0 0 3 3 3 3 3 0 3 3 3 3
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 3 3 3 3
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 4 4 0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 0 3 0 0 3 3 3 3 3 3 3
0 0 0 0 6 6 0 0 0 0 0 4 4 4 4 4 4 4 4 0 3 0 3 3 3 3 3 3 3 3
0 0 0 0 6 6 0 0 0 0 0 4 4 4 4 4 4 4 4 0 3 0 0 3 3 3 3 0 3 3
0 0 6 6 6 6 6 6 0 0 0 4 4 0 0 0 0 0 0 0 3 0 3 3 3 3 3 3 3 3
0 0 6 6 6 6 6 6 0 0 0 4 4 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0 0 0 0 0 0 5 5 0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
"""
grid2 = np.array([list(map(int, row.split())) for row in grid2_str.strip().split('\n')])
expected_output_colors2 = {1, 3, 4, 5, 6} # Including background

# --- Helper: Determine Background Color (Simplified from previous code) ---
def determine_background_color_h6(grid: np.ndarray, base_content_colors: set) -> int:
    h, w = grid.shape
    if h == 0 or w == 0: return BACKGROUND_PIXEL
    top_left_color = grid[0, 0]
    if top_left_color in base_content_colors:
        return int(top_left_color)
    else:
        flat_grid = grid.flatten()
        content_pixels = [p for p in flat_grid if p in base_content_colors]
        if not content_pixels: return BACKGROUND_PIXEL
        counts = Counter(content_pixels)
        max_count = counts.most_common(1)[0][1]
        modes = sorted([color for color, count in counts.items() if count == max_count])
        return int(modes[0])

# --- Metrics Calculation Function ---
def calculate_metrics_h6(grid: np.ndarray, name: str, expected_colors: set):
    print(f"\n--- Metrics for {name} (Hypothesis H6) ---")

    # 1. Background Color
    bg_color = determine_background_color_h6(grid, BASE_CONTENT_COLORS)
    print(f"Determined Background Color: {bg_color}")

    # 2. Check for Orange(7)
    orange_present = ORANGE_COLOR in grid
    print(f"Orange(7) Present: {orange_present}")

    # 3. Determine Actual Content Colors
    if orange_present:
        actual_content_colors = BASE_CONTENT_COLORS.union({AZURE_COLOR})
    else:
        actual_content_colors = BASE_CONTENT_COLORS
    print(f"Actual Content Colors Set: {actual_content_colors}")

    # 4. Identify All Non-Zero, Non-Background Objects
    #    (Simpler: just get unique colors for verification)
    present_colors = set(np.unique(grid)) - {BACKGROUND_PIXEL}
    print(f"Present Colors in Input (excluding 0): {present_colors}")

    # 5. Determine Selected Colors (excluding background)
    selected_colors = set()
    for color in present_colors:
        if color == bg_color: # Skip background color object itself
            continue
        if color in actual_content_colors:
             selected_colors.add(color)
    print(f"Predicted Selected Content Colors: {selected_colors}")

    # 6. Compare with Expected Output
    predicted_output_colors = selected_colors.union({bg_color})
    print(f"Predicted Output Colors (incl. background): {predicted_output_colors}")
    print(f"Expected Output Colors: {expected_colors}")
    print(f"Match: {predicted_output_colors == expected_colors}")

# --- Run Metrics ---
calculate_metrics_h6(grid1, "Example 1", expected_output_colors1)
calculate_metrics_h6(grid2, "Example 2", expected_output_colors2)
