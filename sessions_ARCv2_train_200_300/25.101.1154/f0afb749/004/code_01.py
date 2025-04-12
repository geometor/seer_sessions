import numpy as np

# Function to safely get pixel color, returning -1 for Out Of Bounds (OOB)
def get_pixel(grid, r, c):
    h, w = grid.shape
    if 0 <= r < h and 0 <= c < w:
        return grid[r, c]
    return -1 # Indicate OOB

def analyze_white_pixel(r, c, input_np, output_np):
    """Analyzes a white input pixel and its expected output pattern."""
    input_height, input_width = input_np.shape
    output_height, output_width = output_np.shape
    
    if input_np[r, c] != 0:
        return None # Only analyze white pixels

    pixel_info = {
        "coord": (r, c),
        "expected_pattern": "Unknown",
        "all_cardinal_white": True,
        "all_moore_white": True,
        "cardinal_neighbors": [],
        "moore_neighbors": []
    }

    # Determine Expected Output Pattern
    out_r, out_c = 2 * r, 2 * c
    if out_r + 1 < output_height and out_c + 1 < output_width:
        block = output_np[out_r:out_r+2, out_c:out_c+2]
        if block[0, 0] == 1 and block[1, 1] == 1 and block[0, 1] == 0 and block[1, 0] == 0:
            pixel_info["expected_pattern"] = "Blue"
        elif block[0, 0] == 0 and block[1, 1] == 0 and block[0, 1] == 0 and block[1, 0] == 0:
             pixel_info["expected_pattern"] = "White"
        # else: could be part of a larger non-white block override, ignore pattern check
        # Need to handle cases where the output block is overwritten by a non-white pixel expansion
        # Example: If I[r,c]=0 but I[r-1,c]=5, then O[2r-2:2r, 2c:2c+2]=5, overwriting O[2r, 2c].
        # A better check: If the original input I[r,c] was 0, then check the expected output O[2r,2c] and O[2r+1,2c+1]
        if input_np[r,c] == 0:
             if output_np[out_r, out_c] == 1 and output_np[out_r+1, out_c+1] == 1:
                  pixel_info["expected_pattern"] = "Blue"
             elif output_np[out_r, out_c] == 0 and output_np[out_r+1, out_c+1] == 0:
                 # Ensure other corners are also 0 if they exist
                 corner10 = output_np[out_r+1, out_c] if out_r+1 < output_height else 0
                 corner01 = output_np[out_r, out_c+1] if out_c+1 < output_width else 0
                 if corner10 == 0 and corner01 == 0:
                     pixel_info["expected_pattern"] = "White"


    # Analyze Neighbours
    neighbour_coords = [
        # Cardinal
        (r-1, c), (r+1, c), (r, c-1), (r, c+1),
        # Diagonal
        (r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)
    ]
    
    cardinal_indices = {0, 1, 2, 3}

    for i, (nr, nc) in enumerate(neighbour_coords):
        color = get_pixel(input_np, nr, nc)
        neighbour_info = ((nr, nc), color)
        pixel_info["moore_neighbors"].append(neighbour_info)

        is_cardinal = (i in cardinal_indices)
        if is_cardinal:
             pixel_info["cardinal_neighbors"].append(neighbour_info)

        # Check if valid neighbour (not OOB) is non-white
        if color > 0: # Non-white neighbour found
             pixel_info["all_moore_white"] = False
             if is_cardinal:
                 pixel_info["all_cardinal_white"] = False
        elif color == -1: # OOB neighbour
             pass # Doesn't count as non-white


    # Filter out analyses where pattern remained Unknown
    if pixel_info["expected_pattern"] == "Unknown":
        return None
        
    return pixel_info

# --- Load Data ---
# Example 1
input_1 = np.array([[2, 0], [0, 0]])
output_1 = np.array([[2, 2, 0, 0], [2, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
# Example 2
input_2 = np.array([[0,0,0,5,0],[0,5,0,0,0],[0,0,0,0,0],[0,5,0,0,0],[0,0,0,0,0]])
output_2 = np.array([[1,0,0,0,0,0,5,5,0,0],[0,1,0,0,0,0,5,5,0,0],[0,0,5,5,0,0,0,0,1,0],[0,0,5,5,0,0,0,0,0,1],[1,0,0,0,1,0,0,0,0,0],[0,1,0,0,0,1,0,0,0,0],[0,0,5,5,0,0,1,0,0,0],[0,0,5,5,0,0,0,1,0,0],[0,0,0,0,1,0,0,0,1,0],[0,0,0,0,0,1,0,0,0,1]])
# Example 3
input_3 = np.array([[0,0,0,0,0,3],[0,0,0,0,0,0],[0,3,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]])
output_3 = np.array([[0,0,0,0,0,0,0,0,0,0,3,3],[0,0,0,0,0,0,0,0,0,0,3,3],[1,0,0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0,0,0],[0,0,3,3,0,0,0,0,0,0,0,0],[0,0,3,3,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,0,1,0,0]])

datasets = {
    "Ex1": (input_1, output_1),
    "Ex2": (input_2, output_2),
    "Ex3": (input_3, output_3)
}

# --- Analyze ---
results = {}
for name, (input_grid, output_grid) in datasets.items():
    h, w = input_grid.shape
    results[name] = []
    for r in range(h):
        for c in range(w):
             analysis = analyze_white_pixel(r, c, input_grid, output_grid)
             if analysis: # Add only if analysis was successful (white input, known pattern)
                 results[name].append(analysis)

# --- Report ---
print("White Pixel Analysis Summary:")
for name, analyses in results.items():
    print(f"\n--- {name} ---")
    blue_pattern_pixels = [info for info in analyses if info["expected_pattern"] == "Blue"]
    white_block_pixels = [info for info in analyses if info["expected_pattern"] == "White"]

    print(f"  Pixels resulting in BLUE pattern ({len(blue_pattern_pixels)}):")
    print(f"    Coords: {[info['coord'] for info in blue_pattern_pixels]}")
    print(f"    All Cardinal White?: {[info['all_cardinal_white'] for info in blue_pattern_pixels]}")
    print(f"    All Moore White?:    {[info['all_moore_white'] for info in blue_pattern_pixels]}")
    
    print(f"  Pixels resulting in WHITE block ({len(white_block_pixels)}):")
    print(f"    Coords: {[info['coord'] for info in white_block_pixels]}")
    print(f"    All Cardinal White?: {[info['all_cardinal_white'] for info in white_block_pixels]}")
    print(f"    All Moore White?:    {[info['all_moore_white'] for info in white_block_pixels]}")

    # Highlight contradictions to simple rules
    blue_with_non_white_cardinal = [p['coord'] for p in blue_pattern_pixels if not p['all_cardinal_white']]
    white_with_all_white_cardinal = [p['coord'] for p in white_block_pixels if p['all_cardinal_white']]
    blue_with_all_white_moore = [p['coord'] for p in blue_pattern_pixels if p['all_moore_white']]
    white_with_all_white_moore = [p['coord'] for p in white_block_pixels if p['all_moore_white']]

    if blue_with_non_white_cardinal:
        print(f"    (!) Blue pattern despite non-white Cardinal neighbour(s): {blue_with_non_white_cardinal}")
    if white_with_all_white_cardinal:
         print(f"    (!) White block despite all Cardinal neighbours being white: {white_with_all_white_cardinal}")
    # Separating Moore analysis for clarity
    print(f"    (i) Blue pattern details (All Moore White?):")
    for p in blue_pattern_pixels:
        print(f"      {p['coord']}: {p['all_moore_white']}")
    print(f"    (i) White block details (All Moore White?):")
    for p in white_block_pixels:
         print(f"      {p['coord']}: {p['all_moore_white']}")
