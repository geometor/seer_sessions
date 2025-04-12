import numpy as np
from collections import Counter

def analyze_grid_properties(input_grid: list[list[int]], example_id: int):
    """Analyzes grid properties relevant to the hypothesis."""
    grid = np.array(input_grid, dtype=int)
    background_color = 0
    non_background_mask = grid != background_color

    if not np.any(non_background_mask):
        print(f"\n--- Example {example_id} Analysis ---")
        print("Input grid has no non-background pixels.")
        return

    colors_present = np.unique(grid[non_background_mask])
    color_pixel_counts = {}

    # Calculate total pixel count for each color
    non_background_pixels = grid[non_background_mask]
    color_counts = Counter(non_background_pixels)
    color_pixel_counts = dict(color_counts)

    # Determine the color with the maximum total pixel count
    max_total_pixels = 0
    color_with_max_pixels = -1 # Placeholder
    target_colors = set()
    if color_pixel_counts:
       max_total_pixels = max(color_pixel_counts.values())
       target_colors = {color for color, count in color_pixel_counts.items() if count == max_total_pixels}
       # To report a single color if only one exists, otherwise report the set
       if len(target_colors) == 1:
           color_with_max_pixels = list(target_colors)[0]
       else:
           color_with_max_pixels = target_colors # Report the set in case of ties


    # Identify colors in the expected output (simple approximation: unique non-background colors)
    # This requires the actual output grid, which is not passed here,
    # so we'll infer from the problem description/previous examples.
    # Example 0 output: Blue (1)
    # Example 1 output: Blue (1)
    # Example 2 output: Blue (1)
    # Example 3 output: Red (2)
    output_colors_expected = {
        0: {1},
        1: {1},
        2: {1},
        3: {2}
    }


    print(f"\n--- Example {example_id} Analysis ---")
    print(f"Input Grid Dimensions: {grid.shape}")
    print(f"Non-background Colors Present: {colors_present.tolist()}")
    print(f"Total Pixel Count per Color: {color_pixel_counts}")
    print(f"Color(s) with Max Total Pixels: {color_with_max_pixels} (Count: {max_total_pixels})")
    print(f"Expected Output Color(s): {output_colors_expected.get(example_id, 'Unknown')}")

# Placeholder grids used previously (replace with actual grids if available, but results should be the same)
example_grids = [
    # Example 0 Input (Conceptual)
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
     [0,0,0,1,1,1,1,1,0,0,0,0,2,2,0,0],
     [0,0,1,1,1,1,1,1,0,0,0,2,2,2,0,0],
     [0,1,1,1,1,1,1,1,0,0,0,0,2,0,0,0],
     [0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
     [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0],
     [0,0,0,0,1,1,1,1,0,0,0,0,3,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]], # Large blue (1), scattered red (2), green (3)
    # Example 1 Input (Conceptual)
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,1,0,0,0,0,1,1,0,0,0,1,1,0,0],
     [0,1,1,0,0,0,0,1,1,0,0,0,1,1,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,1,1,1,1,0,0,0,1,1,0,0,0,0],
     [0,0,0,1,1,1,1,0,0,0,1,1,0,0,0,0],
     [0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]], # Multiple blue (1) objects
    # Example 2 Input (Conceptual)
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,1,0,2,2,0,3,0,4,4,0,1,1,0,0],
     [0,1,1,0,2,2,0,0,0,4,4,0,1,1,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,1,1,0,0,2,0,0,3,3,0,4,4,0,0],
     [0,1,1,1,0,0,0,0,0,3,3,0,4,4,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,2,2,0,0,0,0,0,0,0,0,0,1,1,0,0],
     [0,2,2,0,0,0,0,0,0,0,0,0,1,1,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]], # Blue (1), Red (2), Green (3), Cyan (4) objects. Output is Blue.
    # Example 3 Input (Conceptual)
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,2,2,2,0,0,1,1,0,0,2,2,0,0,1,0],
     [0,2,2,2,0,0,1,1,0,0,2,2,0,0,0,0],
     [0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,1,1,1,0,0,2,2,0,0,0],
     [0,0,0,0,0,0,1,1,1,0,0,2,2,0,0,0],
     [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,2,2,0,0,0,0,0,0,0,1,1,0,0,0,0],
     [0,2,2,0,0,0,0,0,0,0,1,1,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]  # Red (2) and Blue (1) objects. Output is Red.
]

for i, grid_data in enumerate(example_grids):
    analyze_grid_properties(grid_data, i)