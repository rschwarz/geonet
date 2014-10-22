'''
Utilities for geometry
'''

import numpy as np

# from http://stackoverflow.com/questions/2827393/
def unit_vector(vector):
    '''Returns the unit vector of the vector.'''
    return vector / np.linalg.norm(vector)


# from http://stackoverflow.com/questions/2827393/
def angle_between(v1, v2):
    '''Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    '''
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle


def star_angles(center, leaves, pos):
    '''compute angles between leave arcs'''
    cpos = np.array(pos[center])
    lpos = [np.array(pos[n]) for n in leaves]
    dirs = [l - cpos for l in lpos]
    pairs = zip(dirs, dirs[1:] + dirs[:1])
    return [angle_between(x,y) for x,y in pairs]
