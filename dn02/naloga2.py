
def naloga2(vhod: list, nacin: int) -> tuple[list, float]:
    """
    Izvedemo kodiranje ali dekodiranje z algoritmom LZW.
    Zacetni slovar vsebuje vse 8-bitne vrednosti (0-255). 
    Najvecja dolzina slovarja je 4096.

    Parameters
    ----------
    vhod : list
        Seznam vhodnih znakov: bodisi znaki abecede
        (ko kodiramo) bodisi kodne zamenjave 
        (ko dekodiramo).
    nacin : int 
        Stevilo, ki doloca nacin delovanja: 
            0: kodiramo ali
            1: dekodiramo.

    Returns
    -------
    (izhod, R) : tuple[list, float]
        izhod : list
            Ce je nacin = 0: "izhod" je kodiran "vhod"
            Ce je nacin = 1: "izhod" je dekodiran "vhod"
        R : float
            Kompresijsko razmerje
    """
    
    izhod = []

    if nacin == 0:
        # Encode

        grammar = {}
        for i in range(256):
            grammar[chr(i)] = i

        N = ""
        for z in vhod:
            new = str(N) + str(z)
            if new in grammar:
                N = new
            else:
                izhod.append(grammar[N])
                if len(grammar) < 4096:
                    grammar[new] = len(grammar)
                N = z

        if N:
            izhod.append(grammar[N])
        
        R = float((len(izhod) * 12) / (len(vhod) * 8))

    if nacin == 1:
        # Decode
        '''
        grammar_len = 256
        next_code = 256
        decompressed_data = []
        grammar = dict([(x, chr(x)) for x in range(grammar_len)])

        for code in vhod:
            if not (code in grammar):
                grammar[code] = string + (string[0])
            decompressed_data  grammar[code]
            if not (len(string) == 0):
                grammar[next_code] = string + (grammar[code][0])
                next_code += 1
            string = grammar[code]
        izhod = list(decompressed_data)
        '''

        vhod_len = len(vhod)
        grammar = {}
        for i in range(256):
            grammar[i] = chr(i)
        
        N = grammar[vhod[0]]
        K = N 
        izhod = []

        izhod.append(N)

        for k in vhod[1:]:
            if k in grammar:
                N = grammar[k]
            else:
                N = K + K[0]
            [izhod.append(x) for x in N]
            if len(grammar) < 4096:
                grammar[len(grammar)] = K + N[0]
            K = N

        R = float((len(vhod) * 12) / (len(izhod) * 8))

    return (izhod, R)

