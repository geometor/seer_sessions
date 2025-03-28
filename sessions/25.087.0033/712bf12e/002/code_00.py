# Modification to check_connectivity_refined
# Inside the neighbor loop:
nr, nc = r + dr, c + dc
# Check bounds (must be above the bottom row)
if 0 <= nr < height - 1 and 0 <= nc < width:
    neighbor = (nr, nc)
    # Check if neighbor is white (0), not visited, AND NOT BELOW THE CURRENT CELL (nr >= r)
    # if neighbor not in visited and input_grid_np[nr, nc] == 0 and nr <= r: # Only Up/Sideways?
    # Let's test "strictly upwards or sideways" nr <= r
    # Let's test "upwards, sideways, AND downwards but only if not already visited?" no that's BFS
    # Let's test "Can only move into cells with row index <= current row index"?
    if neighbor not in visited and input_grid_np[nr, nc] == 0 and nr <= r: # Test "No downward movement"
        visited.add(neighbor)
        queue.append(neighbor)