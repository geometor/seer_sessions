    pixels_to_change = set()
    for r_orig, c_orig in target_object_coords:
         # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r_orig + dr, c_orig + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if the neighbor is NOT already the target color
                    if grid_np[nr, nc] != target_color: # <-- Reads from INPUT grid
                         pixels_to_change.add((nr, nc))

    # Change the color of the identified pixels in the output grid
    for r, c in pixels_to_change:
        output_grid[r, c] = target_color # <-- Writes to OUTPUT grid