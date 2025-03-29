import numpy as np

"""
This program simulates the movement of particles on a grid and marks their paths, including initial positions. Collisions (Magenta) persist once created.

The input grid contains initial positions of two types of particles:
- Azure (8): Moves diagonally down-right (+1 row, +1 column) per step.
- Green (3): Moves diagonally down-left (+1 row, -1 column) per step.

The simulation proceeds in discrete steps:
1. Initialize the output grid as a copy of the input grid, marking the initial particle positions.
2. Identify all initial azure and green particles and their starting velocities.
3. For a fixed number of steps (calculated as grid_height + grid_width to ensure sufficient time for traversal and bounces):
    a. For each particle, calculate its potential next position based on its current position and velocity.
    b. Check if the potential position is outside the grid boundaries.
    c. If a boundary is hit, adjust the landing position to be on the boundary and reverse the corresponding velocity component (dr or dc) for the *next* step. A particle hitting a corner reverses both components.
    d. Record the final landing position (r, c) for the current step and the color of the particle landing there. Collect all landings for the current step in a dictionary mapping `(r, c)` to a set of colors landing there.
    e. Update the output grid based on the current step's landings:
        i. If both Azure (8) and Green (3) land on the same cell (r, c) in this step, set output_grid[r, c] = 6 (Magenta).
        ii. Else if only Azure (8) particle(s) land on (r, c), set output_grid[r, c] = 8, *unless* the cell is already Magenta (6).
        iii. Else if only Green (3) particle(s) land on (r, c), set output_grid[r, c] = 3, *unless* the cell is already Magenta (6).
        (Cells not landed on in this step retain their current color. Magenta collision points persist).
    f. Update each particle's position to its landing spot for this step and update its velocity according to any bounces that occurred.
4. After all steps are simulated, return the final state of the output grid, showing the traced paths and collision points.
"""

def transform(input_grid):
    """
    Simulates particle movement and path tracing on a grid with persistent collisions.

    Args:
        input_grid (np.ndarray): The input grid containing initial particle positions (8 for Azure, 3 for Green).

    Returns:
        np.ndarray: The output grid showing the traced paths (8 or 3) and collision points (6).
    """

    # Get grid dimensions
    H, W = input_grid.shape

    # Initialize the output grid as a copy of the input grid
    # This ensures initial particle positions are marked from the start.
    output_grid = input_grid.copy()

    # Identify initial particles and their velocities
    # Each particle is a dictionary storing its state: position (r, c), color, and velocity (dr, dc).
    particles = []
    for r in range(H):
        for c in range(W):
            color = input_grid[r, c]
            if color == 8:  # Azure particle
                # Starts moving down-right
                particles.append({'r': r, 'c': c, 'color': 8, 'dr': 1, 'dc': 1})
            elif color == 3: # Green particle
                # Starts moving down-left
                particles.append({'r': r, 'c': c, 'color': 3, 'dr': 1, 'dc': -1})

    # Determine the number of simulation steps
    # Using H + W ensures particles have enough steps to traverse the grid even with bounces.
    num_steps = H + W

    # --- Simulation Loop ---
    for step in range(num_steps):
        # Dictionary to track where particles land in *this* specific step.
        # Key: (row, col) tuple, Value: set of colors landing at that position.
        landings_this_step = {}
        # List to store the calculated next state (position and velocity) for each particle.
        next_particle_states = []

        # If no particles are left (e.g., if they could be removed, though not in this spec), stop early.
        if not particles:
             break

        # --- Calculate Movement, Handle Bounces, Record Landings for each particle ---
        for i, p in enumerate(particles):
            # Current state
            r, c = p['r'], p['c']
            dr, dc = p['dr'], p['dc']

            # Calculate potential next position
            potential_r = r + dr
            potential_c = c + dc

            # Initialize the actual landing position and velocity for the *next* step
            landed_r = potential_r
            landed_c = potential_c
            next_dr = dr
            next_dc = dc

            # --- Check for and handle boundary collisions (bounces) ---
            # Check vertical boundaries (top: row 0, bottom: row H-1)
            if landed_r < 0:
                landed_r = 0    # Land on the top boundary
                next_dr = 1   # Reverse vertical velocity for next step (move down)
            elif landed_r >= H:
                landed_r = H - 1 # Land on the bottom boundary
                next_dr = -1  # Reverse vertical velocity for next step (move up)

            # Check horizontal boundaries (left: col 0, right: col W-1)
            if landed_c < 0:
                landed_c = 0    # Land on the left boundary
                next_dc = 1   # Reverse horizontal velocity for next step (move right)
            elif landed_c >= W:
                landed_c = W - 1 # Land on the right boundary
                next_dc = -1  # Reverse horizontal velocity for next step (move left)

            # Record the final landing position for this step and the particle's color
            landing_pos = (landed_r, landed_c)
            landings_this_step.setdefault(landing_pos, set()).add(p['color'])

            # Store the state (position and potentially updated velocity) this particle will have at the start of the next step
            next_particle_states.append({
                'next_r': landed_r,  # Position becomes the spot landed on this step
                'next_c': landed_c,
                'next_dr': next_dr, # Velocity might have been updated by a bounce
                'next_dc': next_dc
            })

        # --- Update the Output Grid Based on Landings in This Step ---
        for (r, c), colors_landed in landings_this_step.items():
            # Check for simultaneous Azure (8) and Green (3) landing -> Magenta (6)
            if 8 in colors_landed and 3 in colors_landed:
                output_grid[r, c] = 6 # Collision creates Magenta
            # Check for Azure (8) landing only
            elif 8 in colors_landed:
                # Mark with Azure only if the cell isn't already a collision point (Magenta)
                if output_grid[r, c] != 6:
                    output_grid[r, c] = 8
            # Check for Green (3) landing only
            elif 3 in colors_landed:
                # Mark with Green only if the cell isn't already a collision point (Magenta)
                 if output_grid[r, c] != 6:
                    output_grid[r, c] = 3
            # If neither landed here this step, or if only particles of the same color landed
            # where that color already exists, or if the cell is Magenta, the cell retains
            # its previous value.

        # --- Update Particle States for the Next Iteration ---
        # Apply the calculated next positions and velocities to each particle for the upcoming step.
        for i, p in enumerate(particles):
            p['r'] = next_particle_states[i]['next_r']
            p['c'] = next_particle_states[i]['next_c']
            p['dr'] = next_particle_states[i]['next_dr']
            p['dc'] = next_particle_states[i]['next_dc']

    # Return the final output grid after all simulation steps are completed
    return output_grid