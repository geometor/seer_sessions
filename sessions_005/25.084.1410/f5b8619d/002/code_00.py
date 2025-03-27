# ... tile ...
tiled_grid = np.tile(input_np, (2, 2))
output_grid = np.copy(tiled_grid) # Start output as a copy of tiled input

for r in range(tiled_H):
    for c in range(tiled_W):
        # Only check pixels that are white in the *original* tiled grid
        if tiled_grid[r, c] == 0:
            has_non_white_neighbor = False
            # Check neighbors in the *original* tiled grid
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    # ... bounds check ...
                        # Check if neighbor is non-white
                        if tiled_grid[nr, nc] != 0:
                            has_non_white_neighbor = True
                            break
                if has_non_white_neighbor:
                    break
            # If found, modify the *output* grid pixel
            if has_non_white_neighbor:
                output_grid[r, c] = 8
# Return output_grid