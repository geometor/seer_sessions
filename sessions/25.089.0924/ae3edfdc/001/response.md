```python
import numpy as np
from typing import List, Tuple, Dict, Set

"""
Transformation Rule Description:

The transformation moves specific 'mover' pixels (orange=7, green=3) to positions adjacent (North, South, East, West) to specific 'attractor' pixels (blue=1 for orange, red=2 for green). The movement is based on proximity.

1.  **Initialization:** Create an output grid of the same size as the input, filled with the background color (white=0).
2.  **Static Placement:** Identify all blue (1) and red (2) pixels in the input. Place them in the output grid at their original locations.
3.  **Mover Assignment:**
    *   For each orange (7) pixel in the input, find the *closest* blue (1) pixel using Manhattan distance. If there are multiple blue pixels at the same minimum distance, choose the one with the smallest row index, then the smallest column index. Assign the orange pixel to this chosen blue pixel.
    *   Perform the same assignment process for green (3) pixels, assigning each to its closest red (2) pixel using the same distance calculation and tie-breaking rules.
4.  **Mover Placement:**
    *   For each blue (1) pixel:
        *   Consider all orange (7) pixels assigned to it.
        *   Sort these assigned orange pixels based on their Manhattan distance *to this blue pixel* (ascending). Use the orange pixel's original row, then column index for tie-breaking.
        *   Identify the four adjacent cells (N, S, E, W) to the blue pixel.
        *   Iterate through the sorted assigned orange pixels. For each orange pixel:
            *   Find the adjacent cells around the blue pixel that are currently white (0) in the output grid and within the grid bounds.
            *   If there are no such available adjacent cells, skip this orange pixel.
            *   Calculate the Manhattan distance from the *original position* of the current orange pixel to each *available* adjacent cell.
            *   Choose the available adjacent cell with the minimum distance to the orange pixel. Use the adjacent cell's row, then column index for tie-breaking.
            *   Place an orange (7) pixel in the chosen adjacent cell in the output grid. Mark this cell as occupied for this blue pixel (so it cannot be used again by other oranges assigned to the same blue).
    *   Repeat the placement process for each red (2) pixel and its assigned green (3) pixels, following the same sorting and proximity rules.
5.  **Final Output:** The resulting grid with static attractors and moved pixels is the final output.
"""

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates Manhattan distance between two points (row, col)."""
    r1, c1 = p1
    r2, c2 = p2
    return abs(r1 - r2) + abs(c1 - c2)

def get_valid_adjacent_cells(grid_shape: Tuple[int, int], point: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Gets valid (within bounds) N, S, E, W adjacent cells."""
    r, c = point
    h, w = grid_shape
    potential_neighbors = [
        (r - 1, c), # North
        (r + 1, c), # South
        (r, c + 1), # East
        (r, c - 1), # West
    ]
    valid_neighbors = []
    for nr, nc in potential_neighbors:
        if 0 <= nr < h and 0 <= nc < w:
            valid_neighbors.append((nr, nc))
    return valid_neighbors

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule: moves orange pixels adjacent to the nearest blue,
    and green pixels adjacent to the nearest red, based on proximity rules.
    """
    h, w = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Initialize with white (0)

    # Find all relevant pixel locations from the input grid
    blue_targets = find_pixels(input_grid, 1)
    red_targets = find_pixels(input_grid, 2)
    orange_sources = find_pixels(input_grid, 7)
    green_sources = find_pixels(input_grid, 3)

    # Place static attractor pixels (blue and red)
    for r, c in blue_targets:
        output_grid[r, c] = 1
    for r, c in red_targets:
        output_grid[r, c] = 2

    # --- Step 1: Assign Movers to Targets ---

    # Assign Orange (7) to nearest Blue (1)
    blue_assignments: Dict[Tuple[int, int], List[Tuple[int, int]]] = {bt: [] for bt in blue_targets}
    if blue_targets: # Proceed only if blue targets exist
        for os_coord in orange_sources:
            min_dist = float('inf')
            closest_targets = []
            for bt_coord in blue_targets:
                dist = manhattan_distance(os_coord, bt_coord)
                if dist < min_dist:
                    min_dist = dist
                    closest_targets = [bt_coord]
                elif dist == min_dist:
                    closest_targets.append(bt_coord)

            # Tie-breaking for closest target: min row, then min col
            closest_targets.sort()
            chosen_target = closest_targets[0]
            blue_assignments[chosen_target].append(os_coord)

    # Assign Green (3) to nearest Red (2)
    red_assignments: Dict[Tuple[int, int], List[Tuple[int, int]]] = {rt: [] for rt in red_targets}
    if red_targets: # Proceed only if red targets exist
        for gs_coord in green_sources:
            min_dist = float('inf')
            closest_targets = []
            for rt_coord in red_targets:
                dist = manhattan_distance(gs_coord, rt_coord)
                if dist < min_dist:
                    min_dist = dist
                    closest_targets = [rt_coord]
                elif dist == min_dist:
                    closest_targets.append(rt_coord)

            # Tie-breaking for closest target: min row, then min col
            closest_targets.sort()
            chosen_target = closest_targets[0]
            red_assignments[chosen_target].append(gs_coord)

    # --- Step 2: Place Assigned Movers ---

    # Place Orange (7) pixels around their assigned Blue (1) targets
    for bt_coord, assigned_oranges in blue_assignments.items():
        # Sort assigned oranges by distance to this blue target (then source row, col)
        assigned_oranges.sort(key=lambda os: (manhattan_distance(os, bt_coord), os[0], os[1]))

        potential_destinations = get_valid_adjacent_cells((h, w), bt_coord)
        occupied_destinations: Set[Tuple[int, int]] = set()

        for os_coord in assigned_oranges:
            available_destinations = []
            # Find adjacent cells that are valid, white, and not yet occupied for this target
            for dest_coord in potential_destinations:
                if output_grid[dest_coord[0], dest_coord[1]] == 0 and dest_coord not in occupied_destinations:
                     available_destinations.append(dest_coord)

            if not available_destinations:
                continue # No place left around this target for this orange

            # Find the closest available destination *to the orange source*
            available_destinations.sort(key=lambda dest: (manhattan_distance(os_coord, dest), dest[0], dest[1]))
            chosen_dest = available_destinations[0]

            # Place the orange pixel and mark the destination as occupied
            output_grid[chosen_dest[0], chosen_dest[1]] = 7
            occupied_destinations.add(chosen_dest)

    # Place Green (3) pixels around their assigned Red (2) targets
    for rt_coord, assigned_greens in red_assignments.items():
        # Sort assigned greens by distance to this red target (then source row, col)
        assigned_greens.sort(key=lambda gs: (manhattan_distance(gs, rt_coord), gs[0], gs[1]))

        potential_destinations = get_valid_adjacent_cells((h, w), rt_coord)
        occupied_destinations: Set[Tuple[int, int]] = set()

        for gs_coord in assigned_greens:
            available_destinations = []
            # Find adjacent cells that are valid, white, and not yet occupied for this target
            for dest_coord in potential_destinations:
                 if output_grid[dest_coord[0], dest_coord[1]] == 0 and dest_coord not in occupied_destinations:
                     available_destinations.append(dest_coord)

            if not available_destinations:
                continue # No place left around this target for this green

            # Find the closest available destination *to the green source*
            available_destinations.sort(key=lambda dest: (manhattan_distance(gs_coord, dest), dest[0], dest[1]))
            chosen_dest = available_destinations[0]

            # Place the green pixel and mark the destination as occupied
            output_grid[chosen_dest[0], chosen_dest[1]] = 3
            occupied_destinations.add(chosen_dest)

    return output_grid
```