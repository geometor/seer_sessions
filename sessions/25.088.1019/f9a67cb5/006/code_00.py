# output_grid is modified
output_grid = np.copy(input_grid)
# queue stores coords to process
queue = deque([start_coord])
# visited tracks coords added to queue or processed
visited = set([start_coord])

while queue:
    r, c = queue.popleft() # P is (r,c), output_grid[r,c] is Red

    for dr, dc in directions:
        nr, nc = r + dr, c + dc # N is (nr, nc)

        if 0 <= nr < rows and 0 <= nc < cols: # N is in bounds
            neighbor_coord = (nr, nc)

            # Check neighbor in *ORIGINAL* grid AND not visited yet
            if input_grid[nr, nc] == background_color and neighbor_coord not in visited:
                visited.add(neighbor_coord)
                output_grid[nr, nc] = fill_color # Fill N in output
                queue.append(neighbor_coord)    # Add N to queue for later expansion