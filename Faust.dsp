import("stdfaust.lib");

gain = nentry("gain", 0.5, 0, 1, 0.01) : si.smoo;

original_signal = 0;
white_noise = (no.noise : si.smoo) * 0.4;

scratch_trigger = hslider("Scratch Trigger", 0.4, 0, 1, 0.01) : si.smoo;
scratch_sound = os.osc.phasor(0.1) : *(0.4) * scratch_trigger;

dust_trigger = hslider("Pop Trigger", 0.004, 0, 1, 0.001) : si.smoo;
dust_sound = os.pulsetrain(50, 100000) * (0.3) * dust_trigger;

mixed_signal = original_signal + white_noise + scratch_sound + dust_sound;
bandpass_signal = mixed_signal : fi.bandpass(3, 85, 6000);
process = bandpass_signal <: _,_;
