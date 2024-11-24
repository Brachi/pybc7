#!/bin/bash

c++ -O3 -Wall -shared -std=c++11 \
    bc7enc_rdo/bc7decomp.cpp \
    bc7enc_rdo/rgbcx.cpp \
    bc7enc_rdo/bc7enc.cpp \
    lib.cpp \
    -o _bc7.so
