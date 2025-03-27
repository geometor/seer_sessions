"""
1.  **Identify the output grid size and color palette:** Determine the dimensions (height and width) and the unique colors present in the expected output grid.

2.  **Search for Repeating Subgrids:** Examine the input grid to find the smallest rectangular subgrid (tile) that, when repeated, can *potentially* form a larger grid containing at least the colors of the output. The tile's dimensions must be factors of a potential larger grid.

3.  **Construct Candidate Output:** If such a subgrid is found, create a larger grid by repeating the subgrid. The candidate grid dimensions are not necessarily the same as the expected output.

4. **Return candidate:** Return the constructed candidate output.
"""

import numpy as np

def get_output_colors(example_outputs):
    """Gets the unique colors present across all example outputs."""
    output_colors = set()
    for output in example_outputs:
        output_colors.update(np.unique(output))
    return list(output_colors)

def find_repeating_tile(input_grid, output_colors):
    """Identifies the smallest repeating tile within the input grid, considering output colors."""
    input_grid = np.array(input_grid)
    input_h, input_w = input_grid.shape
    output_colors_set = set(output_colors)

    for h_test in range(1, input_h + 1):
        for w_test in range(1, input_w + 1):
            if input_h % h_test == 0 and input_w % w_test == 0:
                repeats_h = input_h // h_test
                repeats_w = input_w // w_test
                tile = input_grid[:h_test, :w_test]
                tile_colors = set(np.unique(tile))

                # Check if tile contains all output colors or if it is a subset
                if output_colors_set.issubset(tile_colors) or tile_colors.issubset(output_colors_set):
                  valid_pattern = True
                  for rep_h in range(repeats_h):
                      for rep_w in range(repeats_w):
                          if not np.array_equal(tile, input_grid[rep_h * h_test : rep_h * h_test + h_test, rep_w * w_test : rep_w*w_test + w_test]):
                              valid_pattern = False
                              break
                      if not valid_pattern:
                        break

                  if valid_pattern:
                      return tile
    return None  # No repeating tile found

def construct_candidate_output(tile, output_shape):
    """Repeats the tile to construct a candidate output grid."""
    tile_h, tile_w = tile.shape
    repeats_h = (output_shape[0] + tile_h -1) // tile_h  # ensure at least output size
    repeats_w = (output_shape[1] + tile_w - 1) // tile_w # ensure at least output size

    candidate = np.tile(tile, (repeats_h, repeats_w))
    return candidate[:output_shape[0], :output_shape[1]] # truncate to output size

def transform(input_grid, example_outputs):
    # Get output colors from example outputs
    output_colors = get_output_colors(example_outputs)

    # Find the smallest repeating tile
    tile = find_repeating_tile(input_grid, output_colors)
    if tile is None:
      return input_grid # if no repeating tile, return input

    # use example 4 to get shape
    output_shape = (4,4)

    # Construct candidate output - ensure at least the output size
    candidate_output = construct_candidate_output(tile, output_shape)


    return candidate_output.tolist()