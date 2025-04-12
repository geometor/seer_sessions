        import numpy as np
        
        expected_output = np.array([
            [4, 0, 0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 7, 7, 7, 7, 7],
            [0, 0, 0, 4, 7, 4, 4, 4, 7], [4, 4, 4, 4, 4, 4, 4, 4, 7], [4, 4, 4, 4, 4, 4, 4, 4, 7],
            [4, 4, 4, 4, 4, 4, 4, 4, 7], [0, 0, 0, 4, 7, 4, 4, 4, 7], [0, 0, 4, 0, 7, 7, 7, 7, 7]
        ])
        transformed_output = np.array([
            [4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 7, 7, 7, 7, 7],
            [4, 4, 4, 4, 7, 4, 4, 4, 7], [4, 4, 4, 4, 4, 4, 4, 4, 7], [4, 4, 4, 4, 4, 4, 4, 4, 7],
            [4, 4, 4, 4, 4, 4, 4, 4, 7], [4, 4, 4, 4, 7, 4, 4, 4, 7], [4, 4, 4, 4, 7, 7, 7, 7, 7]
        ])
        coords = np.where((transformed_output == 4) & (expected_output == 0))
        coord_list = sorted(list(zip(coords[0], coords[1])))
        print(f"Pixels Off: {np.sum(expected_output != transformed_output)}")
        print(f"Incorrectly Yellow Count: {len(coord_list)}")
        print(f"Incorrectly Yellow Coords: {coord_list}")