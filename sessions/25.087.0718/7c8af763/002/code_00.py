# Proposed BFS modification:
while q:
    r, c = q.popleft()
    current_dist = distance_grid[r, c]
    source_color = color_grid[r, c] # Original color from the source

    for dr, dc in moves:
        nr, nc = r + dr, c + dc

        if 0 <= nr < height and 0 <= nc < width and input_grid[nr, nc] != GRAY:
            new_dist = current_dist + 1
            existing_dist = distance_grid[nr, nc]
            existing_color_source = color_grid[nr, nc]

            should_update = False
            if new_dist < existing_dist:
                should_update = True
            elif new_dist == existing_dist:
                # Tie-break: Prefer Red (2) over Blue (1)
                if existing_color_source == BLUE and source_color == RED:
                    # Overwrite Blue with Red if distances are equal
                    should_update = True
                # If existing is Red and new is Blue, or both same color, do nothing for tie

            if should_update:
                distance_grid[nr, nc] = new_dist
                color_grid[nr, nc] = source_color # Assign color of the winning source path
                # Add to queue only if it's a path to an unvisited/shorter path cell,
                # OR if it's a tie-breaking update.
                # The standard BFS structure handles this: if we update dist/color, we add to queue
                # to propagate the change. Check if already in queue? No, BFS handles cycles via distance check.
                q.append((nr, nc))
