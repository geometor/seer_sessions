import numpy as np
from typing import List, Tuple, Union

"""
Transforms a NumPy array of 12 integers based on the following rules:
1.  Identifies the last two integers (at indices 10 and 11) as parameters: param1 and param2.
2.  Examines the first 10 integers (indices 0-9, the "data segment") to find connected components 
    (adjacent sequences) of the digit 5.
3.  If exactly two such components of 5s are found:
    a.  Creates a copy of the input array.
    b.  Replaces all 5s in the first component (the one starting at the lower index) with param1 in the copy.
    c.  Replaces all 5s in the second component with param2 in the copy.
    d.  Returns the modified copy.
4.  If the number of components of 5s is not exactly two (i.e., zero or one), the original input array 
    is returned unchanged.
"""

def _find_components(data_segment: Union[List[int], np.ndarray], target_value: int) -> List[List[int]]:
    """
    Finds connected components (sequences of adjacent indices) where the value
    matches target_value within the data segment.

    Args:
        data_segment: A list or 1D NumPy array of integers to search within (e.g., first 10 elements).
        target_value: The integer value defining the components (e.g., 5).

    Returns:
        A list of components, where each component is a list of indices relative
        to the start of the data_segment. Returns an empty list if no components are found.
    """
    components = []
    current_component = []
    # Ensure we iterate over a sequence, converting ndarray if necessary
    data_list = data_segment if isinstance(data_segment, list) else data_segment.tolist()
    
    for i, val in enumerate(data_list):
        if val == target_value:
            # If the current value is the target, add its index to the current component
            current_component.append(i)
        else:
            # If the current value is not the target and we were building a component, finalize it
            if current_component:
                components.append(current_component)
                current_component = []
                
    # Add the last component if the sequence ended with the target value
    if current_component:
        components.append(current_component)
        
    return components

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_sequence: A NumPy array of shape (12,) containing integers.

    Returns:
        A NumPy array of shape (12,) containing integers after applying the transformation.
    """
    # Validate input shape
    if input_sequence.shape != (12,):
        raise ValueError("Input sequence must be a NumPy array of shape (12,)")

    # 1. Identify the parameters (last two elements).
    param1 = input_sequence[10]
    param2 = input_sequence[11]

    # 2. Extract the first 10 elements (data segment).
    data_segment = input_sequence[:10]

    # 3. Find connected components of 5s within the data segment.
    target_value = 5
    components = _find_components(data_segment, target_value)

    # 4. Count components and apply replacement logic if exactly two are found.
    if len(components) == 2:
        # Create a working copy for the output *only if* modification is needed.
        output_sequence = input_sequence.copy()

        # Components are found in order, so components[0] is the first one.
        first_component_indices = components[0]
        second_component_indices = components[1]

        # Replace 5s in the first component with param1.
        # Use NumPy's advanced indexing for efficiency.
        output_sequence[first_component_indices] = param1

        # Replace 5s in the second component with param2.
        output_sequence[second_component_indices] = param2
        
        # Return the modified copy
        return output_sequence
    else:
        # 5. If not exactly two components, return the original input array unchanged.
        # (Returning the original avoids unnecessary copying).
        return input_sequence