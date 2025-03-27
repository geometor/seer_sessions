# Original code snippet from provided listing:
    # 5. Fill Interior region
    for r in range(rows):
        for c in range(cols):
            # If a pixel was originally background AND was not reached by BFS from the outside
            if input_grid_np[r, c] == background_color and (r, c) not in visited:
                 # Check it's not part of the boundary itself (shouldn't happen if BFS logic is correct, but as safety)
                 if output_grid[r,c] != boundary_color: # <-- CHECKING OUTPUT GRID
                    output_grid[r, c] = fill_source_color