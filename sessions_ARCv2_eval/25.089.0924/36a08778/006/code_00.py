                            # Check if neighbor is within grid bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is not visited and is not a boundary (magenta)
                                if not visited[nr, nc] and input_grid[nr, nc] != magenta:
                                     # Check if neighbor is part of the component (orange or red) # <-- PROBLEM HERE
                                     if input_grid[nr, nc] == orange or input_grid[nr, nc] == red:
                                        visited[nr, nc] = True
                                        queue.append((nr, nc))