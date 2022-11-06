import pretty_midi


FREQUENCY = 0.1
PATH = 'bad_apple.mid'

MINECRAFT_INSTRUMENTS = {
    0: ('block.note_block.basedrum', 0.5),
    1: (None, 1.),
    2: ('block.note_block.didgeridoo', 0.5),
    3: (None, 1.),
    4: (None, 1.),
    5: ('block.note_block.bit', 1.),
    6: (None, 0.5),
    # 7: ('block.note_block.didgeridoo', 0.5),
    8: ('block.note_block.chime', 1.),
    9: (None, 0.5),
    10: (None, 0.5),
    11: (None, 0.5),
    12: (None, 1.)
}

NOTES = {}


def get_mean_pitch(mid: pretty_midi.PrettyMIDI) -> int:
    s = 0
    count = 0

    note: pretty_midi.Note
    for i, instrument in enumerate(mid.instruments):
        s += sum(note.pitch for note in instrument.notes)
        count += len(instrument.notes)

    return round(s / count)


def get_mean_for_instrument(instrument):
    return sum(note.pitch for note in instrument.notes) / len(instrument.notes)


def process_instrument(mid: pretty_midi.PrettyMIDI, instrument_id: int, sound: str | None, velocity: float, shift: int):
    instrument = mid.instruments[instrument_id]
    notes = instrument.notes

    if sound is None:
        return

    prev = notes[0]

    tick = int(prev.start // FREQUENCY)
    for i in range(1, len(notes)):
        note = notes[i]

        tick += int((note.start - prev.end) // FREQUENCY)

        NOTES.setdefault(tick, list())
        NOTES[tick].append((instrument_id, note.pitch - shift, velocity))

        tick += int((note.end - note.start) // FREQUENCY)

        prev = note


def main():
    mid = pretty_midi.PrettyMIDI(PATH)
    shift = get_mean_pitch(mid) - 12

    for instrument_id, (sound, velocity) in MINECRAFT_INSTRUMENTS.items():
        process_instrument(mid, instrument_id, sound, velocity, shift)

    with open('processed.oc2mid', 'w') as f:
        for tick, notes in sorted(NOTES.items()):
            notes = [f'{n[0]}!{n[1]}!{n[2]}' for n in notes]

            print(f'{tick}|{",".join(notes)}', file=f)


if __name__ == '__main__':
    main()
