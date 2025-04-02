```python
import numpy as np
from collections import Counter

"""
Transforms an input grid by identifying 'noise' pixels and replacing their color based on their neighbors.

1.  **Analyze Color Frequencies:** Count the occurrences of each color (0-9) in the input grid.
2.  **Identify Noise Colors:** Determine the color(s) that appear least frequently in the grid (must appear at least once). These are designated as "noise" colors.
3.  **Initialize Output Grid:** Create a new grid identical to the input grid. This will be modified to become the output.
4.  **Iterate and Replace:** Go through each pixel of the input grid, checking its color:
    *   **If the pixel's color is a noise color:**
        a.  **Examine Neighbors:** Identify the colors of its cardinal neighbors (pixels directly above, below, left, and right, staying within the grid boundaries).
        b.  **Filter Neighbors:** Ignore any neighbors whose colors are also noise colors. Consider only the "non-noise" neighbors.
        c.  **Find Majority Neighbor Color:** If there are any non-noise neighbors:
            i.  Count the occurrences of each color among the non-noise neighbors.
            ii. Identify the color(s) that appear most frequently.
            iii. **Resolve Ties:** If only one color is most frequent, select that color. If there's a tie (multiple colors share the highest frequency), select the color with the largest numerical value among the tied colors.
            iv. **Update Output:** Change the color of the corresponding pixel in the output grid to the selected replacement color.
        d.  **No Non-Noise Neighbors:** If the noise pixel has no non-noise neighbors, leave its color unchanged in the output grid.
    *   **If the pixel's color is not a noise color:** Keep its color unchanged in the output grid.
5.  **Final Output:** The modified grid, after checking and potentially replacing all noise pixels, is the final output.
"""

def transform(input_grid):
    """
    Replaces the least frequent color(s) in a grid with the most frequent
    color among their non-noise neighbors.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Step 1: Analyze Color Frequencies
    all_pixels = input_array.flatten()
    color_counts = Counter(all_pixels)

    # Filter out colors that don't appear (count = 0)
    present_color_counts = {color: count for color, count in color_counts.items() if count > 0}

    # Handle empty grid or grid with only one color type that doesn't need changing
    if not present_color_counts or len(present_color_counts) == 1:
        return output_array.tolist() # No noise possible or needed

    # Step 2: Identify Noise Colors
    min_frequency = min(present_color_counts.values())
    noise_colors = {color for color, count in present_color_counts.items() if count == min_frequency}

    # Step 3 is implicitly done by creating output_array as a copy initially

    # Step 4: Iterate and Replace
    for r in range(height):
        for c in range(width):
            current_color = input_array[r, c]

            # Check if the current pixel is a noise pixel
            if current_color in noise_colors:
                non_noise_neighbor_colors = []
                # a. Examine Neighbors & b. Filter Neighbors
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    # Check bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbor_color = input_array[nr, nc]
                        # Filter out noise colors
                        if neighbor_color not in noise_colors:
                            non_noise_neighbor_colors.append(neighbor_color)

                # c. Find Majority Neighbor Color (only if non-noise neighbors exist)
                if non_noise_neighbor_colors:
                    neighbor_counts = Counter(non_noise_neighbor_colors)
                    max_neighbor_freq = 0
                    # Find the maximum frequency among non-noise neighbors
                    for count in neighbor_counts.values():
                         if count > max_neighbor_freq:
                             max_neighbor_freq = count

                    # Identify all colors with that maximum frequency
                    most_frequent_neighbors = [
                        color for color, count in neighbor_counts.items() if count == max_neighbor_freq
                    ]

                    # iii. Resolve Ties by choosing the largest numerical color value
                    replacement_color = max(most_frequent_neighbors)

                    # iv. Update Output
                    output_array[r, c] = replacement_color
                # d. No Non-Noise Neighbors: Do nothing, color remains as copied initially

            # Else (pixel is not noise): Do nothing, color remains as copied initially

    # Step 5: Final Output
    return output_array.tolist()
```