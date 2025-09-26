cmake_minimum_required(VERSION 3.5)
project(pybc7)


set (BC7ENC_SRC_LIST
	bc7enc_rdo/bc7enc.cpp
	bc7enc_rdo/bc7enc.h
	bc7enc_rdo/bc7decomp.cpp
	bc7enc_rdo/bc7decomp.h
	bc7enc_rdo/rgbcx.cpp
	bc7enc_rdo/rgbcx.h
	lib.cpp
	)

set(CMAKE_SHARED_LIBRARY_PREFIX "")
add_library(pybc7 SHARED ${BC7ENC_SRC_LIST})
