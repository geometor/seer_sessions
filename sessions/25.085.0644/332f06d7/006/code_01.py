def transform(input_grid):
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Starts as a copy
    # ... color definitions ...
    red_objects = find_objects(grid, agent_color)
    if not red_objects: return input_grid
    red_object_coords = red_objects[0]

    white_objects = find_objects(grid, target_color)
    num_white_objects = len(white_objects)
    if num_white_objects == 0: return input_grid
    # ... white_coord_to_object_index setup ...
    # ... blue_path_coords setup ...
    # ... BFS setup and execution ...
    # ... reachable_white_object_index/coords determined ...

    if reachable_white_object_coords is not None: # A target was reached
        # Change reachable white object to blue
        for r, c in reachable_white_object_coords:
            output_grid[r, c] = result_color_target # Modifies output_grid

        # Decide fate of red object based on TOTAL white objects
        if num_white_objects == 1:
            # Change red object to white
            for r, c in red_object_coords:
                output_grid[r, c] = result_color_agent_single # Modifies output_grid
        elif num_white_objects > 1:
            # Leave red object as red (already is in output_grid copy)
            pass
    # If no target reached, output_grid remains the initial copy
    return output_grid.tolist()