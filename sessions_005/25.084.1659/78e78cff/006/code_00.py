            if 0 <= nr < height and 0 <= nc < width and neighbor_loc not in visited:
                # Crucially, only spread through allowed_color and don't cross boundary
                if grid[nr, nc] == allowed_color: # <--- Check the NEIGHBOR
                    visited.add(neighbor_loc)
                    queue.append(neighbor_loc)