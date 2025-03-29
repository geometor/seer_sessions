def flood_fill_background(grid):
    height, width = grid.shape
    reachable_mask = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add all border white pixels to the queue and mark as reachable
    for r in range(height):
        # Check if grid[r, 0] is white AND not already marked
        if grid[r, 0] == 0 and not reachable_mask[r, 0]: # Added check
            q.append((r, 0))
            reachable_mask[r, 0] = True
        # Check if grid[r, width - 1] is white AND not already marked
        if grid[r, width - 1] == 0 and not reachable_mask[r, width - 1]: # Added check
            q.append((r, width - 1))
            reachable_mask[r, width - 1] = True
    for c in range(width): # Avoid double-adding corners is implicitly handled by the check now
        # Check if grid[0, c] is white AND not already marked
        if grid[0, c] == 0 and not reachable_mask[0, c]: # Added check
             q.append((0, c))
             reachable_mask[0, c] = True
        # Check if grid[height - 1, c] is white AND not already marked
        if grid[height - 1, c] == 0 and not reachable_mask[height - 1, c]: # Added check
            q.append((height - 1, c))
            reachable_mask[height - 1, c] = True

    # Perform BFS
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and not reachable_mask[nr, nc]: # Logic seems correct
                reachable_mask[nr, nc] = True
                q.append((nr, nc))

    return reachable_mask