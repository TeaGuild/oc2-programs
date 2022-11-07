import pretty_midi
import typing
import collections

from midi_oc2_player import consts


FREQUENCY = 0.01
PATH = 'midi/believe_me.mid'

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
    notes = instrument.notes

    for note in notes:
        pitch = note.pitch + base

        minecraft_instrument = None
        for conf in instrument_configs:
            if conf.preferred_range and conf.preferred_range.start <= pitch <= conf.preferred_range.end:
                minecraft_instrument = conf.instrument
                break

        if minecraft_instrument is None:
            raise ValueError(f'No instrument found to process pitch {pitch}')

        shift = consts.F0 + consts.OCTAVE * minecraft_instrument.octave

        tick = int(note.start // FREQUENCY)
        NOTES[tick].append((minecraft_instrument.id, pitch2mine(pitch - shift), min(round(note.velocity / 127, 2), 1)))


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
            notes = [f'{n[0]}!{n[1]}!{n[2]}' for n in notes]

            print(f'{tick}|{",".join(notes)}', file=f)


if __name__ == '__main__':
    main([
        InstrumentConfig(
            consts.get_instrument_by_name('block.note_block.bass'),
            preferred_range=PreferredRange(
                start=30,
                end=54,
            )
        ),
        InstrumentConfig(
            consts.get_instrument_by_name('block.note_block.guitar'),
            preferred_range=PreferredRange(
                start=55,
                end=consts.F0 + 4 * consts.OCTAVE,
            )
        ),
        InstrumentConfig(
            consts.get_instrument_by_name('block.note_block.flute'),
            preferred_range=PreferredRange(
                start=consts.F0 + 4 * consts.OCTAVE + 1,
                end=consts.F0 + 6 * consts.OCTAVE,
            )
        )
    ], base=-consts.OCTAVE)
