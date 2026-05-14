#!/usr/bin/env python3
"""Synthesize a 20s workout EDM/trap-style beat at 128 BPM.

Layers: kick on beats 1,3; clap on 2,4; hi-hat 16ths; sub-bass drone;
build-up + drop at 15s. Output: 1080-Hz mono → stereo WAV → MP3.
"""
import math, struct, wave
from array import array

SR = 44100
BPM = 128
BEAT = 60 / BPM  # 0.469 s
BAR  = BEAT * 4  # 1.875 s
DURATION = 20.0
N = int(SR * DURATION)

def synth_kick(length_s=0.18):
    """Punchy kick: pitch sweep + amplitude env."""
    n = int(SR * length_s)
    buf = [0.0] * n
    for i in range(n):
        t = i / SR
        f = 110 * math.exp(-25 * t) + 45  # pitch from 155Hz → 45Hz
        env = math.exp(-12 * t)  # exp decay
        buf[i] = math.sin(2 * math.pi * f * t) * env
    return buf

def synth_clap(length_s=0.13):
    """Clap: 3 quick noise bursts."""
    import random
    random.seed(7)
    n = int(SR * length_s)
    buf = [0.0] * n
    bursts = [0.0, 0.012, 0.024]
    for bt in bursts:
        bi = int(bt * SR)
        for j in range(min(int(0.04 * SR), n - bi)):
            t = j / SR
            env = math.exp(-30 * t)
            buf[bi + j] += (random.random() * 2 - 1) * env * 0.55
    return buf

def synth_hat(length_s=0.04):
    """Hi-hat: short bright noise."""
    import random
    random.seed(11)
    n = int(SR * length_s)
    buf = [0.0] * n
    for i in range(n):
        t = i / SR
        env = math.exp(-60 * t)
        buf[i] = (random.random() * 2 - 1) * env
    # simple highpass via diff
    for i in range(len(buf) - 1, 0, -1):
        buf[i] = buf[i] - 0.7 * buf[i-1]
    return buf

def mix(target, sample, start_i, gain=1.0):
    end = min(start_i + len(sample), len(target))
    for i in range(end - start_i):
        target[start_i + i] += sample[i] * gain

# Build mix
mixed = [0.0] * N

# Sub bass: constant drone at 41Hz (deep), low amplitude
for i in range(N):
    t = i / SR
    mixed[i] += math.sin(2 * math.pi * 41 * t) * 0.10

# Pre-render samples
kick = synth_kick()
clap = synth_clap()
hat  = synth_hat()

# Bars 0-6: build-up phase (less kick, more hat)
# Bars 7-end: full energy
def build_intensity(t):
    """0-3.75s: intro, 3.75-15s: main, 15-18s: build-up, 18-20s: tail."""
    if t < 1.875:    return 0.4  # bar 1
    if t < 7.5:      return 0.85 # bars 2-4
    if t < 13.0:     return 0.95 # bars 5-7
    if t < 16.0:     return 1.05 # build (bar 8)
    return 1.0  # drop / tail

# Kick on every beat
t = 0.0
beat_i = 0
while t < DURATION:
    bar_pos = beat_i % 4
    intensity = build_intensity(t)
    # Kick on 1, 3 (and 4 of last bar for stutter)
    if bar_pos in (0, 2):
        mix(mixed, kick, int(t * SR), 1.05 * intensity)
    # Extra kick stutter in last 2 bars
    if t >= 16 and bar_pos == 3:
        mix(mixed, kick, int(t * SR), 1.10)
        mix(mixed, kick, int((t + BEAT/2) * SR), 1.0)
    t += BEAT
    beat_i += 1

# Clap on 2, 4
t = BEAT  # start at beat 2 (=index 1)
beat_i = 1
while t < DURATION:
    bar_pos = beat_i % 4
    if bar_pos in (1, 3):
        intensity = build_intensity(t)
        mix(mixed, clap, int(t * SR), 0.85 * intensity)
    t += BEAT
    beat_i += 1

# Hi-hat 16ths (every quarter-beat)
t = 0.0
step = BEAT / 4  # 16th
hat_idx = 0
while t < DURATION:
    intensity = build_intensity(t)
    # Open hat (louder) every 8th
    gain = 0.32 if hat_idx % 2 == 0 else 0.18
    # Roll in build-up bar (14-16s)
    if 14.0 <= t < 16.0:
        gain = 0.45
        step_now = BEAT / 8  # 32nd notes roll
    else:
        step_now = step
    mix(mixed, hat, int(t * SR), gain * intensity)
    t += step_now
    hat_idx += 1

# Riser sweep at 13-16s (filtered noise rising)
import random
random.seed(13)
riser_start = int(13.0 * SR)
riser_end   = int(16.0 * SR)
for i in range(riser_start, riser_end):
    t = (i - riser_start) / SR
    progress = t / 3.0  # 0 to 1
    env = progress ** 1.5 * 0.35
    # Filtered noise (band-pass sweep up)
    n = random.random() * 2 - 1
    mixed[i] += n * env

# Reverse cymbal (sweep down) for outro 18-20s
for i in range(int(18.0 * SR), N):
    t = (i - int(18.0 * SR)) / SR
    env = math.exp(-2 * t) * 0.30
    n = random.random() * 2 - 1
    mixed[i] += n * env

# Normalize
peak = max(abs(x) for x in mixed)
if peak > 0:
    gain = 0.95 / peak
    mixed = [x * gain for x in mixed]

# Soft tanh limiter
mixed = [math.tanh(x * 1.4) for x in mixed]

# Write 16-bit stereo WAV
print(f"writing {N} samples ({DURATION}s @ {SR}Hz)...")
data = array('h')
for s in mixed:
    v = int(max(-32767, min(32767, s * 32767)))
    data.append(v)
    data.append(v)  # stereo

with wave.open('/tmp/beat.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())

print("OK /tmp/beat.wav")
