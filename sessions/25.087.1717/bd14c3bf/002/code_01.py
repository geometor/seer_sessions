def has_hole(grid, obj_pixels, background_reachable_mask):
    """Checks if a blue object borders any unreachable white pixels (holes)."""
    height, width = grid.shape
    obj_pixel_set = set(obj_pixels) # Optimization removed for clarity

    for r, c in obj_pixels:
        # Check all 4 neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is white (0) AND was NOT reached by the background flood fill
                if grid[nr, nc] == 0 and not background_reachable_mask[nr, nc]:
                    # We found a white pixel adjacent to the object that is part of a hole
                    return True # This object borders a hole

    return False # No adjacent hole pixels found