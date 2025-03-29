def transform(input_grid_list):
    try:
        grid = np.array(input_grid_list, dtype=int)
        if grid.size == 0: return []
        rows, cols = grid.shape
    except Exception:
        return [] # Could malformed input trigger this?

    visited = np.zeros_like(grid, dtype=bool)
    background_color = 8
    target_color = 2

    # Step 1: Find background
    border_pixels = set()
    # ... (populate border_pixels, handles rows/cols > 0)
    background_start_coords = []
    # ... (populate background_start_coords from border_pixels if color==8)

    if not background_start_coords: # Handles case where no border Azure pixels exist
        return []

    current_region_pixels = find_contiguous_region(grid, background_start_coords, background_color, visited)
    # What if background_start_coords was non-empty, but find_contiguous_region returns empty?
    # This might happen if the start coords were somehow marked visited *before* the call? No.
    # Or if the start coords didn't actually match background_color? No, checked before adding.
    # Seems unlikely find_contiguous_region would return empty if given valid, non-visited start coords matching the target color.

    region_color_sequence = []

    while True:
        # ... find neighbor_coords ...
        if not neighbor_coords: break
        # ... populate neighbor_colors ...
        if len(neighbor_colors) != 1: break # <--- Problem must be related to this section

        next_layer_color = list(neighbor_colors)[0] # <--- Error here

        # ... add to sequence ...
        # ... find next region using next_layer_color and its start coords ...
        next_region_pixels = find_contiguous_region(grid,
                                                    neighbor_start_coords_by_color[next_layer_color],
                                                    next_layer_color,
                                                    visited)

        if not next_region_pixels: # <--- Added safeguard break
             break

        current_region_pixels = next_region_pixels

    # ... check sequence ...
    if target_color in region_color_sequence:
        return [[target_color]]
    else:
        return []