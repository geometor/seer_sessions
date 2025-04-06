# Hybrid check
            # Check if neighbor is valid and not visited
            if is_valid(nr, nc, rows, cols) and (nr, nc) not in visited:
                # Check if neighbor is potentially fillable (was originally 7)
                if input_grid[nr][nc] == fillable_value:
                     # Check if the path is currently open (neighbor is still 7 in output)
                     # This check seems redundant if we start fill from 3s only
                    # if output_grid[nr][nc] == fillable_value: ? No.

                    # If the source cell (r,c) is 3 (either initial or filled)
                    # and the neighbor was originally 7... fill it.
                    visited.add((nr, nc))
                    output_grid[nr][nc] = source_value
                    queue.append((nr, nc))