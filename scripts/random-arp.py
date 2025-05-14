import mido
import random
from mido import MidiFile, MidiTrack, Message

def create_midi(filename, notes, tempo=128):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(mido.MetaMessage('set_tempo', tempo=int(60000000/tempo)))
    track.append(Message('program_change', program=1, time=0))
    ticks_per_beat = 480
    for note, duration in notes:
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=int(duration * ticks_per_beat)))
    mid.save(filename)
    print(f"MIDI file '{filename}' generated!")

a_minor = [57, 60, 64, 65, 67]
random_arp = [(random.choice(a_minor), 0.25) for _ in range(16)]
create_midi("big_in_japan_random_arp.mid", random_arp)