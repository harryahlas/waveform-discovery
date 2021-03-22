# waveform-discovery

Analysis of waves for ML

### wave_window_counts_vNN.py

-   [x] Understand appropriate filter/kernel count for waveform

    -   [x] Import waveform

    -   [x] Calculate rolling variance for 2-5 samples

    -   [x] Get count of large percent (90+%?) of windows. *python/wave_window_counts_v01.py*

        -   [x] 2 samples: *2 step drops that occur 3+ times make up about 5% of all 2 steps.*
        -   [x] 3 samples: not good only very small values repeated
        -   [x] 4 samples: didn't even look
        -   [x] 5 samples: didn't even look

    -   [x] Try importing longer sample and see how grouping changes *python/wave_window_counts_v02.py*

        -   Percent missed if we use (\~17000) filters that occur 2+ times \~ 3%
        -   Percent missed if we use (\~12000) filters that occur 3+ times \~ 5%

### Distortion Analysis

-   [x] Research optimisers, eg not mean squared error. What is the best one? Not hinge

    -   Starting point: <https://keras.io/api/losses/>

-   [ ] Short, low distortion test. See if we can get great accuracy on short wave prediction

    -   [x] Identify script for generating artificial waves: [00_create_artificial_waves.py](https://github.com/harryahlas/flayer/blob/master/00_create_artificial_waves.py)

    -   [x] Test/debug artificial waves script

    -   [ ] Determine what samples might look like.

        -   [ ] Conduct brief steinberg tests on both amp and IR
        -   [ ] How many? Maybe start with a very small number of samples \<1k
        -   [ ] max width - should be very short for this, maybe 50 samples?
        -   [ ] max height
        -   [ ] how much space/padding/start point etc

    -   [ ] Generate initial samples

    -   [ ] Generate 1k dist samples using steinberg tools

    -   [ ] Identify ML approach, cnn vs nn

    -   [ ] Build model

    -   [ ] Try different losses and maybe different optimizers from link above

        -   Optimizers:

            -   [ ] default/MSE
            -   [ ] Mean absolute error <code>model.compile(optimizer='sgd', loss=tf.keras.losses.MeanAbsoluteError())</code> [MeanAbsoluteError](https://keras.io/api/losses/regression_losses/#meanabsoluteerror-class)
            -   [ ] Mean absolute % error <code>MeanAbsolutePercentageError()</code>, same link as above
            -   [ ] Cosine similarity <code>model.compile(optimizer='sgd', loss=tf.keras.losses.CosineSimilarity(axis=1))</code>, same link as above

    -   [ ] Try visualizing filters if it makes sense

-   [ ] Evaluate results. If above works, move below. If not, do an even shorter test.

-   [ ] Longer low distortion test

    -   [ ] create steps

### Data Input

-   [ ] Figure out how to import old wavs (vs mp3s, endianness etc) *optional*

### Alternate

-   [ ] **Try this:** <https://github.com/GuitarML/GuitarLSTM>

    -   [x] Create DI file 3-4 minutes, lots of playing styles

    -   [x] Create Dist file. Import back into DAW and then align it.

    -   [x] Export them both

    -   [x] Create colab file

    -   [ ] Try these parameters: --training_mode=0 \# enter 0, 1, or 2 for speed tranining, accuracy training, or extended training, respectively --input_size=150 \# sets the number of previous samples to consider for each output sample of audio --split_data=3 \# splits the input data by X amount to reduce RAM usage; trains the model on each split separately --max_epochs=1 \# sets the number of epochs to train for; intended to be increased dramatically for extended training --batch_size=4096 \# sets the batch size of data for training

    -   [x] Rerun with more time/epochs. Note that splitting the data by 15 allowed it to run.

        -   [x] <code>!python train.py --training_mode=2 --split_data=15 --max_epochs=30 /content/gdrive/MyDrive/Development/audio/train_x.wav /content/gdrive/MyDrive/Development/audio/train_y.wav harry_model</code> meh
        -   [x] <code>!python train.py --training_mode=1 --split_data=3 --max_epochs=150 /content/gdrive/MyDrive/Development/audio/train_x.wav /content/gdrive/MyDrive/Development/audio/train_y.wav harry_model2</code>
        -   2nd run is definitely better but still long way from accurate.
        -   [x] If improvement is minimal then try one of above without IR. If it comes close to matching amp alone, then that is a learning.

    -   [x] Try higher input size argument without IR: <code>!python train.py --training_mode=1 --split_data=30 --input_size=500 --max_epochs=3 /content/gdrive/MyDrive/Development/audio/train_x.wav /content/gdrive/MyDrive/Development/audio/train_y\_amp_only.wav harry_model</code>
        - [x] this is breaking now, not sure why. Can research, maybe look at an older version. Try this: <code>!python train.py --training_mode=2 --split_data=15 --input_size=50 --max_epochs=3 /content/gdrive/MyDrive/Development/audio/train_x.wav /content/gdrive/MyDrive/Development/audio/train_y_amp_only.wav harry_model</code> 
            - this woks, not sure whyother dores not...**research?**
        -   changed split_data to 30 because it crashed at 15
        -   changed to 3 epochs because ran out of time
        -   [x] If this works noticeably better then try with more epochs and consider adding IR back.
    -   Test plugin - cd C:\Users\USERNAME\AppData\Roaming\GuitarML\SmartAmpPro\training
        -   [x] <code>python train.py ../captures/firstmodel2.wav firstmodel2b</code>
            - garbage
        -   [ ] <code>python train.py ../captures/firstmodel2.wav firstmodel2c --max_epochs=15</code>
            - *pending - see if improvement is significant - if so, extend training epochs*   
