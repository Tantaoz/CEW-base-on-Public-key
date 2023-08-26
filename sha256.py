import hashlib
import operator


def sha256(data):
    # Calculate SHA256 hash value
    hash_object = hashlib.sha256(data.encode())
    hex_digest = hash_object.hexdigest()

    # Convert a hexadecimal string to a binary array
    binary_array, K, key = [], [], []
    for c in hex_digest:
        bits = bin(int(c, 16))[2:].zfill(4)
        binary_array.extend([int(b) for b in bits])
    S = [binary_array[i:i + 8] for i in range(0, len(binary_array), 8)]  # 256 bits divided into 32 groups
    for i in range(len(S)):
        ki = ''.join(list(map(str, S[i])))
        K.append(int(ki, 2))  # binary to decimal
    key = [K[j:j + 8] for j in range(0, len(K), 8)]  # 32 decimal integers are equally divided into 4 groups
    return binary_array, K, key


def parameter(Sum, K, key):
    d = (Sum * 256) % 31  # Compute the comparison bit index
    for i in range(0, len(key)):
        for j in range(0, len(key[i])):
            if key[i][j] >= K[d]:
                key[i][j] = 0
            else:
                key[i][j] = 1
    return key


def group(Key):
    K1, K2, K3, K4 = Key[0], Key[1], Key[2], Key[3]
    A, B, C, D, E = [], [], [], [], []
    X0, Y0, x0, a, b = 0, 0, 0, 0, 0
    for i in range(0, 8):
        A.append(operator.xor(K1[i], K2[i]))
        B.append(operator.xor(K1[i], K3[i]))
        C.append(operator.xor(K1[i], K4[i]))
        D.append(operator.xor(K2[i], K3[i]))
        E.append(operator.xor(K3[i], K4[i]))
    for j in range(8):
        X0 += int(A[7 - j]) * pow(2, j)
        Y0 += int(B[7 - j]) * pow(2, j)
        x0 += int(C[7 - j]) * pow(2, j)
        a += int(D[8 - 1 - j]) * pow(2, j)
        b += int(E[8 - 1 - j]) * pow(2, j)
    X0 = X0 / 256
    Y0 = Y0 / 256
    x0 = x0 / 256
    a = a / 256 + 1
    b = b / 512
    return X0, Y0, x0, a, b


if __name__ == "__main__":
    data = "helloworld"
    binary_array, K, key = sha256(data)
    Sum = 10000
    key1 = parameter(Sum, K, key)
    X0, Y0, x0, a, b = group(key1)
    print(X0, Y0, x0, a, b)
