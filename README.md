# waveform-discovery

Analysis of waves for ML 

### wave_window_counts_vNN.py
- [x] Understand appropriate filter/kernel count for waveform
  - [x] Import waveform
  - [x] Calculate rolling variance for 2-5 samples
  - [x] Get count of large percent (90+%?) of windows.  *python/wave_window_counts_v01.py*
    - [x] 2 samples: *2 step drops that occur 3+ times make up about 5% of all 2 steps.*
    - [x] 3 samples: not good only very small values repeated
    - [x] 4 samples: didn't even look
    - [x] 5 samples: didn't even look
  - [x] Try importing longer sample and see how grouping changes   *python/wave_window_counts_v02.py*
    - Percent missed if we use (~17000) filters that occur 2+ times ~ 3%
    - Percent missed if we use (~12000) filters that occur 3+ times ~ 5%
    
### Distortion Analysis
- [x] Research optimisers, eg not mean squared error. What is the best one? Not hinge
  - Starting point: [https://keras.io/api/losses/](https://keras.io/api/losses/)
- [ ] Short, low distortion test.  See if we can get great accuracy on short wave prediction
  - [ ] Identify script for generating small waves
  - [ ] Determine what 1k sample might look like. Maybe start with a very small number of samples
    - [ ] max width - should be very short for this, maybe 50 samples?
    - [ ] max height
  - [ ] Generate 1k di samples
  - [ ] Generate 1k dist samples using steinberg tools
  - [ ] Identify ML approach, cnn vs nn
  - [ ] Build model
  - [ ] Try different losses and maybe different optimizers from link above
    - Optimizers:
      - [ ] default/MSE
      - [ ] Mean absolute error <code>model.compile(optimizer='sgd', loss=tf.keras.losses.MeanAbsoluteError())</code> [MeanAbsoluteError](https://keras.io/api/losses/regression_losses/#meanabsoluteerror-class)
      - [ ] Mean absolute % error <code>MeanAbsolutePercentageError()</code>, same link as above
  - [ ] Try visualizing filters if it makes sense
- [ ] Evaluate results. If above works, move below. If not, do an even shorter test.
- [ ] Longer low distortion test
  - [ ] create steps

### Data Input
- [ ] Figure out how to import old wavs (vs mp3s, endianness etc) *optional*
