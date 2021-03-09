# waveform-discovery

Analysis of waves for ML 

### wave_window_counts.py
- [ ] Understand appropriate filter/kernel count for waveform
  - [x] Import waveform
  - [x] Calculate rolling variance for 2-5 samples
  - [x] Get count of large percent (90+%?) of windows.  *python/wave_window_counts_v01.py*
    - [x] 2 samples: *2 step drops that occur 3+ times make up about 5% of all 2 steps.*
    - [x] 3 samples: not good only very small values repeated
    - [x] 4 samples: didn't even look
    - [x] 5 samples: didn't even look
  - [ ] **Next** Try importing longer sample and see how grouping changes   *python/wave_window_counts_v02.py (tbd)*
- [_] Figure out how to import old wavs (vs mp3s)