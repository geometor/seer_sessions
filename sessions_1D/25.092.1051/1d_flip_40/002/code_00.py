    # ... (block identification) ...
    
    # Check if the block has more than one element to shift
    if start_index == end_index: #<<< THIS CONDITION IS THE PROBLEM
        # Single element block, no shift needed
        return output_grid 
        
    # ... (extraction, shift, replacement) ...