    # 4. Identify Interior region using Breadth-First Search (BFS) from edges
    visited = set()
    queue = deque()

    # Add all background pixels on the edges to the queue and visited set
    # ... code to add edge pixels ...

    # Perform BFS to find all reachable background pixels from the outside
    while queue:
        r, c = queue.popleft()

        # Check neighbors (4-directional: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is background and not visited and not part of the boundary
                # This condition: input_grid_np[nr, nc] != boundary_color is slightly wrong.
                # We SHOULD be able to visit a background pixel even if it's adjacent to a boundary pixel.
                # The key is we cannot *cross* the boundary.
                # The condition should be: We can move to (nr, nc) if it's within bounds, IS background, and NOT visited.
                # The boundary check is implicitly handled because boundary pixels are not background pixels.
                if (input_grid_np[nr, nc] == background_color and
                        (nr, nc) not in visited): # Removed boundary check here
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    # 5. Fill Interior region
    for r in range(rows):
        for c in range(cols):
            # If a pixel was originally background AND was not reached by BFS from the outside
            if input_grid_np[r, c] == background_color and (r, c) not in visited:
                 # Previous code had: if output_grid[r,c] != boundary_color:
                 # This check was problematic. Let's assume the simplified fill logic:
                 output_grid[r, c] = fill_source_color