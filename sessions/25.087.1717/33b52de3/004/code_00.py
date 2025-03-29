# ... BFS setup ...
while component_q:
    row, col = component_q.popleft()
    # If a non-gray pixel somehow got into the queue (shouldn't happen if we only add gray neighbors)
    # Or if the *starting* pixel wasn't gray (handled by outer loop check)
    if grid[row,col] != gray:
         is_potential_template = False # This seems okay

    current_component_pixels.add((row, col))
    # ... update bounds ...

    # Explore neighbors (4-connectivity)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < h and 0 <= nc < w and not visited[nr, nc]:
            neighbor_color = grid[nr,nc]
            if neighbor_color == gray: # ONLY add gray neighbors to queue
                visited[nr, nc] = True
                component_q.append((nr, nc))
            # This 'elif' might be the problem
            elif neighbor_color != 0: # Check non-background, non-gray connection
                 is_potential_template = False # <<<<< PROBLEM: Adjacent non-gray pixel disqualifies template