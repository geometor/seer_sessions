```python
"""
Identify the set of "character colors" present in the input grid by checking which of the colors {Blue(1), Red(2), Green(3), Yellow(4), Azure(8)} exist in the input.
Determine the initial order of rows for the output grid by taking the canonical sequence [Azure(8), Blue(1), Red(2), Yellow(4), Green(3)] and keeping only the colors identified in step 1.
Apply a special ordering rule: If *neither* Azure(8) *nor* Yellow(4) were present in the input grid, *and* if both Red(2) and Green(3) *are* present, swap the positions of Red(2) and Green(3) in the initial order. This gives the final output row order.
Identify the "noise color" for the grid. This is the most frequently occurring color in the input grid, excluding White(0) and the character colors identified. If there's a tie in frequency, choose the color with the smaller numerical value. If no such noise color exists, default to Gray(5).
Construct the output grid, which will have 4 columns and one row for each character color in the final order.
For each character color in the final order, at position `idx` (starting from 0):
  a. Calculate the number of times the character color should repeat (`n_repeats`) after the first column:
     * If this is the *last* color in the order *and* its index `idx` is 2 or greater, `n_repeats` is 3.
     * Otherwise, `n_repeats` is equal to the index `idx`, but capped at a maximum of 3.
  b. Create the output row: Start with the character color, followed by `n_repeats` copies of the character color, followed by `(3 - n_repeats)` copies of the noise color.
Assemble these rows into the final output grid, maintaining the order determined.
"""

import numpy as np
from collections import Counter

def find_noise_color(grid: np.ndarray, character_colors: set) -> int:
    """
    Finds the most frequent color in the grid, excluding background (0)
    and the provided character colors.

    Args:
        grid: The input numpy array grid.
        character_colors: A set of integers representing the colors identified as characters.

    Returns:
        The integer color value identified as the noise color.
        Defaults to 5 (gray) if no suitable noise color is found.
        Ties in frequency are broken by choosing the lower color value.
    """
    counts = Counter(grid.flatten())

    noise_candidate_counts = {}
    for color, count in counts.items():
        # Include only colors that are not background and not character colors
        if color != 0 and color not in character_colors:
            noise_candidate_counts[color] = count

    if not noise_candidate_counts:
        # No non-background, non-character colors found. Default to gray.
        return 5

    # Find the maximum frequency among candidates
    max_count = 0
    if noise_candidate_counts:
       max_count = max(noise_candidate_counts.values())

    # Get all candidates that have the maximum frequency
    candidates_with_max_count = [
        color for color, count in noise_candidate_counts.items() if count == max_count
    ]

    # Tie-break by choosing the minimum color value among the top candidates
    if candidates_with_max_count:
        noise_color = min(candidates_with_max_count)
    else:
        # This case should theoretically not be reached if noise_candidate_counts was not empty,
        # but provides a fallback.
        noise_color = 5

    return noise_color


def transform(input_grid: list) -> list:
    """
    Transforms the input grid based on identified character colors, a noise color,
    and specific ordering and fill rules.
    """
    input_grid_np = np.array(input_grid, dtype=int)

    # Define potential character colors and their canonical order
    potential_character_colors = {1, 2, 3, 4, 8} # blue, red, green, yellow, azure
    canonical_order = [8, 1, 2, 4, 3] # azure, blue, red, yellow, green

    # 1. Identify which potential character colors are actually present.
    present_colors = set(np.unique(input_grid_np))
    present_character_colors = potential_character_colors.intersection(present_colors)

    # Handle edge case: If no character colors are found, return an empty grid.
    if not present_character_colors:
        return np.empty((0, 4), dtype=int).tolist()

    # 2. Determine the initial order based on canonical order and presence.
    initial_output_order = [color for color in canonical_order if color in present_character_colors]

    # Handle edge case: If filtering resulted in an empty list (unlikely here, but defensive)
    if not initial_output_order:
         return np.empty((0, 4), dtype=int).tolist()

    # 3. Apply conditional swap for Red(2) and Green(3).
    final_output_order = list(initial_output_order) # Make a copy to modify
    azure_present = 8 in present_character_colors
    yellow_present = 4 in present_character_colors
    red_present = 2 in present_character_colors
    green_present = 3 in present_character_colors

    if not azure_present and not yellow_present and red_present and green_present:
        try:
            idx_red = final_output_order.index(2)
            idx_green = final_output_order.index(3)
            # Swap elements at the identified indices
            final_output_order[idx_red], final_output_order[idx_green] = final_output_order[idx_green], final_output_order[idx_red]
        except ValueError:
            # This should not happen if red_present and green_present are True,
            # but handles potential errors.
            pass

    # 4. Identify the noise color.
    noise_color = find_noise_color(input_grid_np, present_character_colors)

    # 5. & 6. Construct the output rows based on the final order and fill rules.
    output_rows = []
    num_output_rows = len(final_output_order)

    for idx, char_color in enumerate(final_output_order):
        # Calculate N - the number of times the character color repeats after the first cell.
        is_last_element = (idx == num_output_rows - 1)

        if is_last_element and idx >= 2:
            n_repeats = 3 # Fill all remaining 3 cells with character color
        else:
            # Otherwise, the number of repeats is the index, capped at 3.
            n_repeats = min(idx, 3)

        # Build the row: [CharColor] + [CharColor * N] + [NoiseColor * (3-N)]
        row = [char_color]                     # Start with the character color
        row.extend([char_color] * n_repeats)   # Add N repeats of the character color
        row.extend([noise_color] * (3 - n_repeats)) # Fill the rest with noise color

        output_rows.append(row)

    # 7. Convert the list of rows into the final output format (list of lists).
    output_grid = np.array(output_rows, dtype=int)

    return output_grid.tolist()
```