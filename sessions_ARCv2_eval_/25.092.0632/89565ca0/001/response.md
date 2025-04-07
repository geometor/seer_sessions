```python
import numpy as np
from collections import Counter
import operator # Consider using if more complex sorting/filtering needed

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
    Identifies specific character colors present in the input grid, determines a 'noise' color,
    and constructs an output grid based on a fixed canonical order of character colors.

    The output grid has one row for each character color present in the input, ordered according
    to the canonical sequence [8, 1, 2, 4, 3]. Each output row is 4 cells wide.
    The first cell contains the character color.
    The remaining three cells are filled with a mix of the character color and the noise color.
    The number of cells filled with the character color (N) depends on the character's position (0-based index 'idx')
    in the output sequence for this specific grid:
    - If it's the last character in the sequence AND its index 'idx' is 2 or greater, N = 3.
    - Otherwise, N = min(idx, 3).
    The remaining (3 - N) cells are filled with the noise color.

    The noise color is the most frequent color in the input grid, excluding background (0)
    and the identified character colors. Ties are broken by choosing the lowest color value.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """

    input_grid_np = np.array(input_grid, dtype=int) # Work with numpy array

    # Define potential character colors and their canonical order
    # These are the colors that form the main shapes/objects to be represented.
    potential_character_colors = {1, 2, 3, 4, 8} # blue, red, green, yellow, azure
    # This specific order determines the row order in the output.
    canonical_order = [8, 1, 2, 4, 3] # azure, blue, red, yellow, green

    # 1. Identify which potential character colors are actually present in the input grid.
    present_colors = set(np.unique(input_grid_np))
    present_character_colors = potential_character_colors.intersection(present_colors)

    # If no character colors are found, return an empty grid (0 rows, 4 columns).
    # This follows the pattern of creating an Nx4 output.
    if not present_character_colors:
        return np.empty((0, 4), dtype=int).tolist() # Return as list of lists

    # 2. Determine the order of characters for the output grid by filtering the
    #    canonical order based on presence in the input.
    output_order = [color for color in canonical_order if color in present_character_colors]

    # If the filtering resulted in an empty list (should be caught by the check above, but defensive check)
    if not output_order:
         return np.empty((0, 4), dtype=int).tolist()

    # 3. Identify the noise color using the helper function.
    noise_color = find_noise_color(input_grid_np, present_character_colors)

    # 4. Construct the output rows according to the rules.
    output_rows = []
    num_output_rows = len(output_order)

    for idx, char_color in enumerate(output_order):
        # Calculate N - the number of times the character color repeats after the first cell.
        # Special rule for the last element if its index is high enough.
        is_last_element = (idx == num_output_rows - 1)

        if is_last_element and idx >= 2:
            n_repeats = 3 # Fill all remaining 3 cells with character color
        else:
            # Otherwise, the number of repeats is the index, capped at 3.
            n_repeats = min(idx, 3)

        # Build the row: [CharColor, CharColor * N, NoiseColor * (3-N)]
        row = [char_color] # Start with the character color
        row.extend([char_color] * n_repeats) # Add N repeats of the character color
        row.extend([noise_color] * (3 - n_repeats)) # Fill the rest with noise color

        output_rows.append(row)

    # 5. Convert the list of rows into the final output format (list of lists).
    #    Numpy array was used internally for convenience.
    output_grid = np.array(output_rows, dtype=int)

    return output_grid.tolist()
```