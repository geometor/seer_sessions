```python
import numpy as np
from collections import Counter

"""
Transformation Rule:

1.  Identify the background color (BG) as the most frequent pixel color in the input grid.
2.  Identify source colors (S) as non-background colors adjacent to BG. Determine orthogonal adjacencies between different source colors.
3.  Derive a source-to-fill map (M) using Hypothesis 20:
    a. For each source color s:
        i. If s is adjacent to any source color s' where s' > s, map s to the highest such adjacent s'.
        ii. Otherwise, map s to itself.
4.  Initialize the output grid as a copy of the input grid.
5.  Perform an iterative flood fill using the derived map M until no changes occur:
    a. In each iteration, calculate the next grid state based on the current state.
    b. For each pixel (r, c):
        i. Get its current color `current_color`.
        ii. Examine orthogonal neighbors in the current grid state.
        iii. Collect "fill influences":
            - If a neighbor has color `C_n` which is a source `s` in map M, the influence is `M[s]`.
            - If a neighbor has color `C_n` which is a fill color `f` (a value in M), the influence is `f`.
        iv. If influences exist, find the `winning_fill` color (the influence with the lowest index/highest priority).
        v. Update the pixel in the *next* grid state to `winning_fill` if:
            - `current_color` is BG, OR
            - `winning_fill` has a higher priority (lower index) than `current_color`.
    c. Update the current grid with the next grid state.
6.  Return the final stabilized grid.

(Caveat): The map derivation rule (Hypothesis 20) is the best fit found during analysis but is known not to perfectly replicate the mapping for all provided training examples (specifically Examples 1 and 3).
"""

def find_background_color(grid_np: np.ndarray) -> int:
    """ Finds the most frequent color in the grid. """
    if grid_np.size == 0:
        return 0 # Default assumption
    colors, counts = np.unique(grid_np, return_counts=True)
    if len(colors) == 0:
        return 0 # Default assumption
    return colors[np.argmax(counts)]

def get_neighbors(h: int, w: int, r: int, c: int) -> list[tuple[int, int]]:
    """ Get orthogonal neighbor coordinates within grid bounds. """
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < h - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < w - 1: neighbors.append((r, c + 1))
    return neighbors

def get_sources_and_adjacency(grid_np: np.ndarray, background_color: int) -> tuple[set[int], dict[int, set[int]]]:
    """
    Identifies source colors (non-BG adjacent to BG) and
    inter-source adjacencies.
    Returns:
        - set of source colors (S)
        - dict mapping S -> set of adjacent different source colors
    """
    h, w = grid_np.shape
    sources = set()
    source_pixel_coords = {} # Store coords for adjacency check
    all_non_bg_colors = set(np.unique(grid_np)) - {background_color}

    # First pass: identify all non-BG pixel locations and which colors are sources
    for color in all_non_bg_colors:
         source_pixel_coords[color] = []

    processed_sources = set() # Track colors checked for BG adjacency
    for r in range(h):
        for c in range(w):
            color = grid_np[r, c]
            if color != background_color:
                source_pixel_coords[color].append((r,c))
                # Check adjacency to background only once per color type
                if color not in processed_sources:
                    is_adj_to_bg = False
                    for nr, nc in get_neighbors(h, w, r, c):
                        if grid_np[nr, nc] == background_color:
                            is_adj_to_bg = True
                            break
                    if is_adj_to_bg:
                        sources.add(color)
                    processed_sources.add(color) # Mark as checked

    # Second pass: determine adjacencies between source colors
    source_adjacencies = {s: set() for s in sources}
    for s_color in sources:
        if s_color not in source_pixel_coords: continue
        for r, c in source_pixel_coords[s_color]:
            for nr, nc in get_neighbors(h, w, r, c):
                neighbor_color = grid_np[nr, nc]
                # Check if neighbor is a *different* source color
                if neighbor_color in sources and neighbor_color != s_color:
                    source_adjacencies[s_color].add(neighbor_color)

    return sources, source_adjacencies


def derive_map_hypothesis20(sources: set[int], source_adjacencies: dict[int, set[int]]) -> dict[int, int]:
    """
    Derives Source-to-Fill map (M) using Hypothesis 20.
    Maps S -> max(adjacent S') if adjacent S' > S exists, else S -> S.
    """
    mapping = {}
    for s in sources:
        map_target = s # Default: map to self
        max_higher_adj = -1
        # Check adjacent sources
        if s in source_adjacencies:
            for adj_s in source_adjacencies[s]:
                if adj_s > s: # Found adjacent source with higher index
                    max_higher_adj = max(max_higher_adj, adj_s)

        # If a higher adjacent source was found, map to the highest one
        if max_higher_adj != -1:
             map_target = max_higher_adj

        mapping[s] = map_target
    return mapping

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule described above.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    h, w = input_grid_np.shape

    # Handle edge cases: empty or uniform grid
    if h == 0 or w == 0:
        return input_grid
    unique_colors_input = np.unique(input_grid_np)
    if len(unique_colors_input) <= 1:
        return input_grid

    # 1. Identify Background Color
    background_color = find_background_color(input_grid_np)

    # 2. Identify Sources and Adjacencies
    sources, source_adjacencies = get_sources_and_adjacency(input_grid_np, background_color)

    # Handle edge case: no sources found
    if not sources:
        return input_grid # No fill can happen

    # 3. Derive Source-to-Fill Map (Hypothesis 20)
    source_fill_map = derive_map_hypothesis20(sources, source_adjacencies)
    fill_colors_set = set(source_fill_map.values()) # Set of colors used for filling

    # 4. Initialize Working Grid
    working_grid_np = np.copy(input_grid_np)

    # 5. Iterative Filling using Map
    while True:
        changed = False
        next_grid_np = np.copy(working_grid_np)

        # Iterate through each pixel
        for r in range(h):
            for c in range(w):
                current_color = working_grid_np[r, c]
                influences = []

                # Collect influences from neighbors based on the map
                for nr, nc in get_neighbors(h, w, r, c):
                    neighbor_color = working_grid_np[nr, nc]

                    if neighbor_color == background_color:
                        continue # Background neighbors don't influence

                    # Check if neighbor is a source in our map
                    if neighbor_color in source_fill_map:
                        influences.append(source_fill_map[neighbor_color])
                    # Check if neighbor is already a fill color
                    elif neighbor_color in fill_colors_set:
                         influences.append(neighbor_color)
                    # Else: neighbor is non-BG, non-source, non-fill - acts as barrier only

                # If influenced, determine winning fill and update if needed
                if influences:
                    winning_fill = min(influences) # Lowest index = highest priority

                    update_pixel = False
                    if current_color == background_color:
                        update_pixel = True
                    elif winning_fill < current_color: # Priority check
                        update_pixel = True

                    # Apply update to next state grid if value changes
                    if update_pixel and next_grid_np[r, c] != winning_fill:
                        next_grid_np[r, c] = winning_fill
                        changed = True

        # Update working grid for next iteration
        working_grid_np = next_grid_np

        # Check for stabilization
        if not changed:
            break

    # 6. Return final grid
    return working_grid_np.tolist()
```