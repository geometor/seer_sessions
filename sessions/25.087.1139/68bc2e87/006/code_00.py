    current_region_pixels = find_contiguous_region(grid, background_start_coords, background_color, visited)
    # What if current_region_pixels is empty here? Let's assume BFS failed for some reason.

    region_color_sequence = []

    while True:
        neighbor_coords = set()
        # If current_region_pixels is empty, this loop doesn't run
        for r, c in current_region_pixels:
            # ...
            neighbor_coords.add((nr, nc))

        # neighbor_coords remains empty
        if not neighbor_coords:
            break # Loop breaks immediately

    # region_color_sequence is empty. Returns []. Seems okay.