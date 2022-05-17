import numpy as np
#import matplotlib.pyplot as plt

def naloga4(vhod: list, fs: int) -> str:
    """
    Poisce akord v zvocnem zapisu.

    Parameters
    ----------
    vhod : list
        vhodni zvocni zapis 
    fs : int
        frekvenca vzorcenja
    
    Returns
    -------
    izhod : str
        ime akorda, ki se skriva v zvocnem zapisu;
        ce frekvence v zvocnem zapisu ne ustrezajo nobenemu od navedenih akordov, 
        vrnemo prazen niz ''
    """
    

    N = len(vhod)
    izhod = ''
    #print("duration: ", N / fs, "s")
    d_freq = fs / N
    #print("Intervals of ", d_freq, " till ", N)

    notes = {   "C1" : 261.63, 
                "CIS1" : 277.18,
                "D1" : 293.66,
                "DIS1" : 311.13,
                "E1" : 329.63,
                "F1" : 349.23,
                "FIS1" : 369.99,
                "G1" : 392,
                "GIS1" : 415.30,
                "A1" : 440,
                "B1" : 466.16,
                "H1" : 493.88,
                
                "C2" : 523.25,
                "CIS2" : 554.37,
                "D2" : 587.33,
                "DIS2" : 622.25,
                "E2" : 659.25,
                "F2" : 698.46,
                "FIS2" : 739.99,
                "G2" : 783.99,
                "GIS2" : 830.61,
                "A2" : 880,
                "B2" : 932.33,
                "H2" :987.77,
            }

    harmonic_notes = [notes[note] * i for i in range(1,3) for note in notes]
    
    chords = {  "Cdur": ["C1", "E1", "G1"],
                "Cmol": ["C1", "DIS1", "G1"], 
                "Ddur": ["D1", "FIS1", "A1"],
                "Dmol": ["D1", "F1", "A1"],
                "Edur": ["E1", "GIS1", "H1"],
                "Emol": ["E1", "G1", "H1"],
                "Fdur": ["F1", "A1", "C2"],
                "Fmol": ["F1", "GIS1", "C2"],
                "Gdur": ["G1", "H1", "D2"],
                "Gmol": ["G1", "B1", "D2"],
                "Adur": ["A1", "CIS2", "E2"],
                "Amol": ["A1", "C2", "E2"],
                "Hdur": ["H1", "DIS2", "FIS2"],
                "Hmol": ["H1", "D2", "FIS2"]
            }

    vhod = abs(np.fft.fft(vhod))
    vhod_norm = (vhod / max(vhod))

    freqs = np.arange(0, fs, d_freq)

    #plt.plot(freqs, vhod_norm)
    #plt.show()
    
    threshold_norm = 0.7

    # get frequencies
    detected_freqs = []
    limit = int(len(vhod)/2)
    for i in range(len(vhod_norm[:limit])):
        if vhod_norm[i] > threshold_norm:
            detected_freqs.append(freqs[i])  # find freq in freqs -> calculate 

    #print(detected_freqs)

    # get notes
    detected_notes = []
    for freq in detected_freqs:
        for note in notes:
            if abs(freq - notes[note]) < 2: #or freq in harmonic_notes:     # note offset
                detected_notes.append(note)
                continue 
                
    #print(detected_notes)
    possible_chords = []

    # get chords
    for chord in chords:
        count = 0
        solved = False
        # each note in each chord
        for note in detected_notes:
            if solved:
                break
            if note in chords[chord]:
                count += 1
                #print(f"Note in {chords[chord]}: {note}, {count} {solved}")
            if count == 3:
                solved = True
                break
        
        if solved:
            #print(chord)
            possible_chords.append(chord)
            izhod = chord
            break

    #print(possible_chords)

    return izhod

