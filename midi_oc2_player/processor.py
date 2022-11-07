import devices
import time


def play_sound(device, *args):
    device.bus.flush()
    device.bus._write_message({'type': 'invoke', 'data': {
        'deviceId': device.device_id,
        'name': 'playMultipleSounds',
        'parameters': args
    }})


def process_tick(s, data):
    notes = data.split(',')

    sounds = []
    volumes = []
    pitches = []

    for note in notes:
        sound_id, pitch, velocity = note.split('!')
        sound = MINECRAFT_INSTRUMENTS[int(sound_id)]
        if sound is not None:
            sounds.append(sound)
            volumes.append(float(velocity))
            pitches.append(float(pitch))

    play_sound(s, sounds, volumes, pitches)


def run(f):
    bus = devices.bus()
    s = bus.find('sound')

    current_tick = 0

    start_time = time.time()
    for line in f:
        tick, data = line.strip().split('|')
        tick = int(tick)

        delay = time.time() - start_time
        to_sleep = (tick - current_tick) * FREQUENCY - delay
        if to_sleep < 0:
            print('missed tick: {}'.format(tick))
            to_sleep = 0

        time.sleep(to_sleep)
        start_time = time.time()

        current_tick = tick

        process_tick(s, data)


with open('processed.oc2mid') as fd:
    header = fd.readline().strip()
    assert header.startswith('pufit-midi')

    FREQUENCY = float(fd.readline().strip())
    instruments_count = int(fd.readline().strip())

    MINECRAFT_INSTRUMENTS = {}
    for _ in range(instruments_count):
        inst_id, name = fd.readline().split()
        MINECRAFT_INSTRUMENTS[int(inst_id)] = name

    run(fd)
