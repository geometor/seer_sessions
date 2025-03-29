    # Seed the queue with all border pixels of the background color
    for r in range(height):
        if grid[r, 0] == background_color and not reachable_mask[r, 0]:
            q.append((r, 0))
            reachable_mask[r, 0] = True
        if grid[r, width - 1] == background_color and not reachable_mask[r, width - 1]:
            q.append((r, width - 1))
            reachable_mask[r, width - 1] = True
    for c in range(width): # Use range(width) to include corners correctly
        if grid[0, c] == background_color and not reachable_mask[0, c]:
             q.append((0, c))
             reachable_mask[0, c] = True
        if grid[height - 1, c] == background_color and not reachable_mask[height - 1, c]:
            q.append((height - 1, c))
            reachable_mask[height - 1, c] = True