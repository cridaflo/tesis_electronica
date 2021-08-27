import mido
import string
import numpy as np

def midi2array(track):
    rta =[[0]*128]
    t = 0
    for message in track:
        dt = message.time
        if dt > 0:
            rta += [rta[-1]]*dt
            rta[-1] = rta[-1]*1
        t += dt
        if message.type == 'note_on':
            rta[-1][message.note] = message.velocity
        elif message.type == 'note_off':
            rta[-1][message.note] = 0
    return np.array(rta)

def arry2midi(arr, tempo = 500000, ticks_per_beat = 384, save = False, filename = 'my_midi.midi'):
    midi_new = mido.MidiFile(ticks_per_beat = ticks_per_beat)
    track = mido.MidiTrack()
    midi_new.tracks.append(track)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
    t = 0
    last = np.zeros(128)
    tam = arr.shape[0]
    for i in range(tam):
        act = arr[i]
        for j in range(128):
            if last[j] != act[j]:
                if act[j] > 0:
                    track.append(mido.Message('note_on', note= j, velocity=int(act[j]), time=i-t))
                else:
                    track.append(mido.Message('note_off', note= j, velocity= 0, time=i -t))
                t = i
        last = act
    track.append(mido.Message('note_on', note = 21, velocity = 0, time=tam-2-t))
    track.append(mido.MetaMessage('end_of_track', time=1))
    if save: 
        midi_new.save(filename)
    return midi_new

def count_ticks(track):
    rta = 0
    for x in track:
        rta+=x.time
    return rta