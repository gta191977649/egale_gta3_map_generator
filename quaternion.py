import numpy as np
import math

def quaternion_to_3x3(x, y, z, w):
    identity_matrix = np.identity(3)
    symmetrical_matrix = np.array([
        [-(y*y)-(z*z), x*y, x*z],
        [x*y, -(x*x)-(z*z), y*z],
        [x*z, y*z, -(x*x)-(y*y)]
    ])
    antisymmetrical_matrix = np.array([
        [0, -z, y],
        [z, 0, -x],
        [-y, x, 0]
    ])

    matrix_3x3 = identity_matrix + 2 * symmetrical_matrix + 2 * w * antisymmetrical_matrix
    return matrix_3x3


def get_euler_angles_from_matrix(matrix):
    x2, y2, z2 = matrix[2]  # Extracting the second row

    # Clamping z2 to the range [-1, 1]
    z2 = max(-1, min(z2, 1))

    nz3 = math.sqrt(x2 * x2 + y2 * y2)
    nz1 = -x2 * z2 / nz3 if nz3 != 0 else 0
    nz2 = -y2 * z2 / nz3 if nz3 != 0 else 0
    vx = nz1 * matrix[0][0] + nz2 * matrix[0][1] + nz3 * matrix[0][2]
    vz = nz1 * matrix[2][0] + nz2 * matrix[2][1] + nz3 * matrix[2][2]
    return math.degrees(math.asin(z2)), -math.degrees(math.atan2(vx, vz)), -math.degrees(math.atan2(x2, y2))


def quaternion_to_euler(x, y, z, w):
    matrix = quaternion_to_3x3(x, y, z, w)
    return get_euler_angles_from_matrix(matrix)
