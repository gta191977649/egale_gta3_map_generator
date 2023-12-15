import math

def quaternion_to_3x3(x, y, z, w):
    identity_matrix = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

    symmetrical_matrix = [
        [-(y * y) - (z * z), x * y, x * z],
        [x * y, -(x * x) - (z * z), y * z],
        [x * z, y * z, -(x * x) - (y * y)]
    ]

    antisymmetrical_matrix = [
        [0, -z, y],
        [z, 0, -x],
        [-y, x, 0]
    ]

    matrix_3x3 = [[0 for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            matrix_3x3[i][j] = identity_matrix[i][j] + 2 * symmetrical_matrix[i][j] + 2 * w * antisymmetrical_matrix[i][j]

    return matrix_3x3

def get_euler_angles_from_matrix(matrix):
    x2, y2, z2 = matrix[1][0], matrix[1][1], matrix[1][2]
    x1, y1, z1 = matrix[0][0], matrix[0][1], matrix[0][2]
    x3, y3, z3 = matrix[2][0], matrix[2][1], matrix[2][2]

    nz3 = math.sqrt(x2 * x2 + y2 * y2)
    nz1 = -x2 * z2 / nz3 if nz3 != 0 else 0
    nz2 = -y2 * z2 / nz3 if nz3 != 0 else 0

    vx = nz1 * x1 + nz2 * y1 + nz3 * z1
    vz = nz1 * x3 + nz2 * y3 + nz3 * z3

    # Clamping z2 to be within [-1, 1] range
    z2_clamped = max(-1, min(z2, 1))

    return math.degrees(math.asin(z2_clamped)), -math.degrees(math.atan2(vx, vz)), -math.degrees(math.atan2(x2, y2))

def from_quaternion(x, y, z, w):
    matrix = quaternion_to_3x3(x, y, z, w)
    return get_euler_angles_from_matrix(matrix)
