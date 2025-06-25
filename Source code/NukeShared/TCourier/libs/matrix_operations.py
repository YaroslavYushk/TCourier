import math


def vector_length(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)


def build_matrix_4x4_from_list(L):
    return [[L[0], L[1], L[2], L[3]],
            [L[4], L[5], L[6], L[7]],
            [L[8], L[9], L[10], L[11]],
            [L[12], L[13], L[14], L[15]]]


def transpose_matrix_4x4(M):
    transposed_M = [[[1], [0], [0], [0]],
                    [[0], [1], [0], [0]],
                    [[0], [0], [1], [0]],
                    [[0], [0], [0], [1]]]
    for i in range(4):
        for j in range(4):
            transposed_M[i][j] = M[j][i]
    return transposed_M


def multiply_matrices_4x4(A, B):
    ''' Multiplies matrix 4x4 to another matrix 4x4 '''
    C = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                C[i][j] += A[i][k] * B[k][j]
    return C


def get_translation_from_matrix_4x4(M):
    return [M[0][3], M[1][3], M[2][3]]


def get_scale_from_matrix_4x4(M):
    scale_x = vector_length(M[0][0], M[1][0], M[2][0])
    scale_y = vector_length(M[0][1], M[1][1], M[2][1])
    scale_z = vector_length(M[0][2], M[1][2], M[2][2])
    return [scale_x, scale_y, scale_z]


def get_rotation_matrix_from_matrix_4x4(M):
    scale_x, scale_y, scale_z = get_scale_from_matrix_4x4(M)
    rot_M = [[M[0][0] / scale_x, M[0][1] / scale_y, M[0][2] / scale_z, 0],
             [M[1][0] / scale_x, M[1][1] / scale_y, M[1][2] / scale_z, 0],
             [M[2][0] / scale_x, M[2][1] / scale_y, M[2][2] / scale_z, 0],
             [0, 0, 0, 1]]
    return rot_M


def get_quaternion_from_rotation_matrix_4x4(R):
    trace = R[0][0] + R[1][1] + R[2][2]
    if trace > 0:
        S = math.sqrt(trace + 1.0) * 2
        w = 0.25 * S
        x = (R[2][1] - R[1][2]) / S
        y = (R[0][2] - R[2][0]) / S
        z = (R[1][0] - R[0][1]) / S
    elif (R[0][0] > R[1][1]) and (R[0][0] > R[2][2]):
        S = math.sqrt(1.0 + R[0][0] - R[1][1] - R[2][2]) * 2
        w = (R[2][1] - R[1][2]) / S
        x = 0.25 * S
        y = (R[0][1] + R[1][0]) / S
        z = (R[0][2] + R[2][0]) / S
    elif R[1][1] > R[2][2]:
        S = math.sqrt(1.0 + R[1][1] - R[0][0] - R[2][2]) * 2
        w = (R[0][2] - R[2][0]) / S
        x = (R[0][1] + R[1][0]) / S
        y = 0.25 * S
        z = (R[1][2] + R[2][1]) / S
    else:
        S = math.sqrt(1.0 + R[2][2] - R[0][0] - R[1][1]) * 2
        w = (R[1][0] - R[0][1]) / S
        x = (R[0][2] + R[2][0]) / S
        y = (R[1][2] + R[2][1]) / S
        z = 0.25 * S
    length = math.sqrt(w**2 + x**2 + y**2 + z**2)
    return (w / length, x / length, y / length, z / length)
