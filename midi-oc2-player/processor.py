import devices
import time
import _thread


FREQUENCY = 0.1
CHANNELS_COUNT = 13


MINECRAFT_INSTRUMENTS = {
    0: ('block.note_block.basedrum', 0.5),
    1: (None, 1.),
    2: ('block.note_block.didgeridoo', 0.5),
    3: (None, 1.),
    4: (None, 1.),
    5: ('block.note_block.bit', 1.),
    6: (None, 0.5),
    7: ('block.note_block.didgeridoo', 0.5),
    8: ('block.note_block.chime', 1.),
    9: (None, 0.5),
    10: (None, 0.5),
    11: (None, 0.5),
    12: (None, 1.)
}


def pitch2mine(pitch):
    x = 2 ** (1 / 12 * (pitch - 12))
    return x if x != -12 else -11.99


def run():
    bus = devices.bus()
    s = bus.find('sound')

    with open('processed.oc2mid') as f:

        current_tick = 0
        for line in f:
            tick, data = line.strip().split('|')
            tick = int(tick)

            time.sleep((tick - current_tick) * FREQUENCY)
            current_tick = tick

            notes = data.split(',')
            for note in notes:
                sound_id, pitch, velocity = note.split('!')
                sound = MINECRAFT_INSTRUMENTS[int(sound_id)][0]
                if sound is not None:
                    _thread.start_new_thread(s.playSound, (sound, float(velocity), pitch2mine(float(pitch))))


run()
