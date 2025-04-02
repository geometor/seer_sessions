                            # Check if neighbor is within grid bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is not visited and is not a barrier (magenta)
                                if not visited[nr, nc] and input_grid[nr, nc] != magenta:
                                    # If it's not a barrier and not visited, add it to the queue
                                    visited[nr, nc] = True
                                    queue.append((nr, nc))