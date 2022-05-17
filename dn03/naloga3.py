import numpy as np

def naloga3(vhod: list, n: int) -> tuple[list, str]:
    """
    Izvedemo dekodiranje binarnega niza `vhod`, zakodiranega 
    s Hammingovim kodom dolzine `n` in poslanega po zasumljenem kanalu.
    Nad `vhod` izracunamo vrednost `crc` po standardu CRC-8/CDMA2000.

    Parameters
    ----------
    vhod : list
        Sporocilo y, predstavljeno kot seznam bitov (stevil tipa int) 
    n : int
        Stevilo bitov v kodni zamenjavi
    
    Returns
    -------
    (izhod, crc) : tuple[list, str]
        izhod : list
            Odkodirano sporocilo y (seznam bitov - stevil tipa int)
        crc : str
            Vrednost CRC, izracunana nad `vhod`. Niz dveh znakov.
    """
    izhod = []

    vhod = np.array(vhod)
    vhod = vhod.reshape((-1, n))

    m = get_redundant_bits(vhod,n)
    H = get_matrix(n, m)
    H = np.array(H)
    H = H.T

    I = np.zeros((m, m), dtype=int)
    cnt = 0

    # get [B | I] matrix
    for i in range(1, n):
        if np.log2(i) % 1 == 0:
            I[:, cnt] = H[:, i-cnt-1]
            H = np.delete(H, i-cnt-1, 1)
            cnt += 1
    H = np.concatenate((H, I), axis=1)

    cnt = 0
    for row in range(vhod.shape[0]):

        # calculate syndrome
        S = np.matmul(vhod[row, :], H.T)
        S = np.mod(S, 2)

        err = 0
        for i in range(n):
            if np.array_equal(H[:, i].T, S):
                err = i+1
                break

        # Error vector
        e = np.zeros((n), dtype=int)
        e[err-1] = 1

        # calculate corrected message
        y = np.bitwise_xor(vhod[row, :], e)
       
        for element in y[:n-m]:
            izhod.append(element)
                
        cnt += 1
        izhod = list(izhod)

    # calculate crc
    vhod = vhod.flatten()

    crc = ''

    vector = np.ones((9), dtype=int)
    vector[8] = vhod[0] ^ vector[7]
    #print(vector[:8], vector[8], vhod[0])
    for i in range(1, len(vhod)):

        if vector[8] == 0:
            vector = np.roll(vector, 1)
            vector[0] = 0
        else:
            # xor 
            vector[7] = vector[6] ^ 1
            vector[6] = vector[5]
            vector[5] = vector[4]
            vector[4] = vector[3] ^ 1
            vector[3] = vector[2] ^ 1
            vector[2] = vector[1]
            vector[1] = vector[0] ^ 1
            vector[0] = 1

        vector[8] = vhod[i] ^ vector[7]
    
    if vector[8] == 0:
        vector = np.roll(vector, 1)
        vector[0] = 0
    else:
        vector[7] = vector[6] ^ 1
        vector[6] = vector[5]
        vector[5] = vector[4]
        vector[4] = vector[3] ^ 1
        vector[3] = vector[2] ^ 1
        vector[2] = vector[1]
        vector[1] = vector[0] ^ 1
        vector[0] = 1

    for i in range(7, -1, -1):
        crc += str(vector[i])

    crc = hex(int(crc, 2))
    crc = str(crc[2:]).upper()
    return (izhod, crc)

def get_redundant_bits(vhod, n):
    # n = 2^m + 1
    m = np.log2(n+1)

    return int(m)
        

def get_matrix(n, m):
    H = [[0]*m for i in range(n)]
    for i in range(0, n):
        digit = bin(i+1)[2:].zfill(m)
        for j in range(m):
            H[i][m-1-j] = int(digit[j])
    return H
