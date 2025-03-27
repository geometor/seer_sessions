def _find_objects(grid, color):
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col))

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = row + dr, col + dc

                            # Check if neighbor is within bounds, is the correct color, and hasn't been visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]: # <--- Potential Issue Here?
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Add the found object (list of coordinates) to the list of objects
                if current_object_coords:
                    objects.append(current_object_coords)

    return objects