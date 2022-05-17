from math import log2
from collections import Counter

def naloga1(besedilo: str, p: int) -> float:

    besedilo = str.upper("".join(list(filter(lambda x: str.isalpha(x), besedilo))))
    entropy = 0

    if p == 0:
        # get frequency of each letter
        freq = Counter(besedilo)
        values = []

        # get probability of each
        for key, value in freq.items():
            values.append(value / len(besedilo))

        values = map(lambda x: x * log2(x), values)
    
        entropy = sum(values)
        entropy *= -1

    elif p == 1:

        # two chars
        freq = Counter(zip(besedilo, besedilo[1:]))
        values2 = []

        #for i in range(len(besedilo) - 1):
            #pair = str(besedilo[i]) + str(besedilo[i+1])
            #freq[pair] = besedilo.count(pair) #count ne steje overlapping
        
        for key, value in freq.items():
            values2.append(value / (len(besedilo) - 1))
        
        values2 = map(lambda x: x * log2(x), values2)

        entropy2 = sum(values2)
        entropy2 *= -1

        # one character
        freq = Counter(besedilo)
        values1 = []

        for key, value in freq.items():
            values1.append(value / len(besedilo))

        values1 = map(lambda x: x * log2(x), values1)
        
        entropy1 = sum(values1)
        entropy1 *= -1

        entropy = entropy2 - entropy1

    elif p == 2:

        # three chars
        freq = Counter(zip(besedilo, besedilo[1:], besedilo[2:])) 
        values3 = []
           
        for key, value in freq.items():
            values3.append(value / (len(besedilo) - 2))
        
        values3 = map(lambda x: x * log2(x), values3)
        entropy3 = sum(values3)
        entropy3 *= -1

         # two chars
        freq = {}
        values2 = []

        freq = Counter(zip(besedilo, besedilo[1:]))

        for key, value in freq.items():
            values2.append(value / (len(besedilo) - 1))
        
        values2 = map(lambda x: x * log2(x), values2)
        entropy2 = sum(values2)
        entropy2 *= -1

        entropy = entropy3 - entropy2
    
    """ Izracun povprecne nedolocenosti na znak 

    Parameters
    ----------
    besedilo : str
        Vhodni niz
    p : int
        Stevilo poznanih predhodnih znakov: 0, 1 ali 2.
        p = 0: H(X1)
            racunamo povprecno informacijo na znak abecede 
            brez poznanih predhodnih znakov
        p = 1: H(X2|X1)
            racunamo povprecno informacijo na znak abecede 
            pri enem poznanem predhodnemu znaku. V bitih.
        p = 2: H(X3|X1,X2)

    Returns
    -------
    H : float 
        Povprecna informacija na znak abecede z upostevanjem 
        stevila poznanih predhodnih znakov 'p'. V bitih.
    """
 
   
    H = float(entropy)
    return H



#besedilo = "Danes bom naredil 1. domaco nalogo!"
#besedilo = "rozica"
#print(naloga1(besedilo, 0))
#print(naloga1(besedilo, 1))
#print(naloga1(besedilo, 2))