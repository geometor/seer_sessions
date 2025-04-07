# Seed the queue with white border cells
for r in range(height):
    for c in [0, width - 1]: # Left and right borders
        # PROBLEM: This condition checks the *barrier_locations* set
        # It SHOULD check the *input_grid* value at (r,c)
        if (r, c) not in barrier_locations and (r,c) not in visited:
            queue.append((r, c))
            visited.add((r, c))
            output_grid[r, c] = 8 # Mark reachable cell in output
# ... similar logic for top/bottom ...

# Perform the flood fill (BFS)
while queue:
    r, c = queue.popleft()
    # Explore neighbors
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            # PROBLEM: This condition ALSO checks the *barrier_locations* set
            # It SHOULD check the *input_grid* value at (nr, nc)
            if (nr, nc) not in barrier_locations and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
                output_grid[nr, nc] = 8