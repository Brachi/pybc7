project(bc7enc)

cmake_minimum_required(VERSION 3.5)

set (BC7ENC_SRC_LIST
	bc7enc.cpp
	bc7enc.h
	bc7decomp.cpp
	bc7decomp.h
	rgbcx.cpp
	rgbcx.h
	)

add_library(bc7enc SHARED ${BC7ENC_SRC_LIST})
