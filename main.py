import itertools
import sys
import time
from typing import List, Union, Any

import numpy as np
import synthesizer
from synthesizer import Player, Synthesizer, Waveform, Writer

primes = {2: 1}
player = Player()
writer = Writer()
player.open_stream()
synth1 = Synthesizer(osc1_waveform=Waveform.sawtooth, osc2_waveform=Waveform.sine, osc1_volume=.5,
                     osc2_volume=.3,
                     use_osc2=True)
synth2 = Synthesizer(osc1_waveform=Waveform.sine, osc2_waveform=Waveform.triangle, osc1_volume=.5, osc2_volume=.3,
                     use_osc2=True)
silence = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=.0)

# accu = []


def play_sounds(frequencies, duration):
    if frequencies:
        chord = synth2.generate_chord(frequencies, duration)
    else:
        chord = silence.generate_constant_wave(440., duration)
    player.play_wave(chord)
    # global accu
    # accu.append(chord)


def mapping_inv_harmonic(p):
    f = 3200 * (primes[p] ** -1)
    return f


def mapping_harmonic(p):
    f = 100 * (primes[p] ** 1)
    return f


def main():
    try:
        duration = .05
        last_prime = 2
        # for i in itertools.count(start=2):
        for i in range(2, 100):
            ps = [p for p in primes if i % p == 0]
            if not ps:  # then is prime
                primes[i] = len(primes) + 1
                last_prime = i
                # play = [mapping_harmonic(i)]

            ps = [p for p in ps if .1 / duration < p < 1 / duration]
            play = [mapping_harmonic(p) for p in ps]

            sys.stdout.write(f"Prime: {last_prime}, {ps}\n")
            sys.stdout.flush()
            play_sounds(frequencies=play, duration=duration)
            # time.sleep(duration)
    except KeyboardInterrupt:
        pass
    print(f'stopped at {list(primes)[-1]}')
    print(primes)
    # writer.write_wave('ascending_primes_faster.wav', np.concatenate(accu))


if __name__ == '__main__':
    main()
