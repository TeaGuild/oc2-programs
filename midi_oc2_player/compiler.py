import pretty_midi
import typing
import collections

from midi_oc2_player import consts


FREQUENCY = 0.01
NOTE_LENGTH = 1
PATH = 'midi/blumenkranz.mid'

NOTES = collections.defaultdict(list)


class PreferredRange(typing.NamedTuple):
    start: int
    end: int


class InstrumentConfig(typing.NamedTuple):
    instrument: consts.Instrument

    preferred_range: PreferredRange | None = None


def pitch2mine(pitch):
    x = 2 ** (1 / 12 * pitch)
    return round(x, 2) if x != -12 else -11.99


def process_instrument(
        instrument: pretty_midi.Instrument,
        instrument_configs: list[InstrumentConfig],
        base: int
):
    if instrument.is_drum:
        print('drums currently are not implemented')
        return

    notes = instrument.notes

    for note in notes:
        pitch = note.pitch + base

        minecraft_instrument = None
        for conf in instrument_configs:
            if conf.preferred_range and conf.preferred_range.start <= pitch <= conf.preferred_range.end:
                minecraft_instrument = conf.instrument
                break

            if conf.instrument.range_start <= pitch <= conf.instrument.range_end:
                minecraft_instrument = conf.instrument
                break

        if minecraft_instrument is None:
            print(f'No instrument found to process pitch {pitch}')
            continue

        shift = consts.F0 + consts.OCTAVE * minecraft_instrument.octave

        tick = int(note.start // FREQUENCY)

        while tick < int(note.end // FREQUENCY):
            NOTES[tick].append(
                (
                    minecraft_instrument.id,
                    pitch2mine(pitch - shift),
                    min(round(note.velocity / 127, 2), 1),
                    note.pitch,
                )
            )
            tick += int(NOTE_LENGTH // FREQUENCY)


def main(instrument_configs: list[InstrumentConfig], base: int):
    mid = pretty_midi.PrettyMIDI(PATH)

    for inst in mid.instruments:
        process_instrument(inst, instrument_configs, base)

    with open('processed.oc2mid', 'w') as f:
        print('pufit-midi v1.0', file=f)
        print(FREQUENCY, file=f)

        print(len(instrument_configs), file=f)
        for conf in instrument_configs:
            print(conf.instrument.id, conf.instrument.name, file=f)

        for tick, notes in sorted(NOTES.items()):
            notes = [f'{n[0]}!{n[1]}!{n[2]}!{n[3] - consts.F0 - consts.OCTAVE}' for n in notes]

            print(f'{tick}|{",".join(notes)}', file=f)


if __name__ == '__main__':
    main([
        InstrumentConfig(consts.get_instrument_by_name('block.note_block.bass')),
        InstrumentConfig(consts.get_instrument_by_name('block.note_block.guitar')),
        InstrumentConfig(consts.get_instrument_by_name('block.note_block.harp')),
        InstrumentConfig(consts.get_instrument_by_name('block.note_block.bell')),
    ], base=0)
