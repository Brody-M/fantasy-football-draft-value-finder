# Earlier Files

These files preserve the initial work. They are not the current dataset pipeline.

Both earlier ADP cleaning scripts mishandle player rows with a line break before the position. The saved ADP CSV has 55 shifted rows and should not be used for analysis.

Use `phases/phase_0_dataset/prepare_dataset.py` to rebuild the corrected merged dataset. The archived inspection script uses pandas and is not a Phase 1 submission.
