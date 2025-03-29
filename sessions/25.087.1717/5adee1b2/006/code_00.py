q_bfs = deque([(r, c)])
visited[r,c] = True # Mark starting point visited
current_object_coords = set()
current_object_coords.add((r,c))
while q_bfs:
    row, col = q_bfs.popleft()
    # Add neighbors to queue (4-connectivity)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = row + dr, col + dc
        # Bounds check
        if not (0 <= nr < height and 0 <= nc < width): continue
        # Visited check and Color check
        if not visited[nr, nc] and input_grid[nr, nc] == object_color:
             visited[nr, nc] = True
             current_object_coords.add((nr, nc))
             q_bfs.append((nr, nc))