import typing


class Instrument(typing.NamedTuple):
    id: int
    name: str
    octave: int

    range: int = 2


OCTAVE = 12
F0 = 18


INSTRUMENTS = [
    Instrument(id=0, name='block.note_block.bass', octave=2),
    Instrument(id=1, name='block.note_block.bell', octave=6),
    Instrument(id=2, name='block.note_block.flute', octave=5),
    Instrument(id=3, name='block.note_block.chime', octave=6),
    Instrument(id=4, name='block.note_block.guitar', octave=3),
    Instrument(id=5, name='block.note_block.xylophone', octave=6),
    Instrument(id=6, name='block.note_block.iron_xylophone', octave=4),
    Instrument(id=7, name='block.note_block.cow_bell', octave=5),
    Instrument(id=8, name='block.note_block.didgeridoo', octave=2),
    Instrument(id=9, name='block.note_block.bit', octave=4),
    Instrument(id=10, name='block.note_block.banjo', octave=4),
    Instrument(id=11, name='block.note_block.pling', octave=4),
    Instrument(id=12, name='block.note_block.harp', octave=4)
]

INSTRUMENTS_BY_NAME = {
    inst.name: inst
    for inst in INSTRUMENTS
}


def get_instrument_by_name(name: str) -> Instrument:
    return INSTRUMENTS_BY_NAME[name]
