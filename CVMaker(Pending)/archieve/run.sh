#!/bin/bash

# Set environment variables
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib"

# Run the application
python CVMaker.py 