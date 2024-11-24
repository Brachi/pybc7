from array import array
import ctypes
import struct
from ctypes import byref

_bc7 = ctypes.cdll.LoadLibrary('./_bc7.so')
_bc7.init(0)

bc7 = _bc7


class RGBA(ctypes.Structure):

    _fields_ = (
        ("r", ctypes.c_ubyte),
        ("g", ctypes.c_ubyte),
        ("b", ctypes.c_ubyte),
        ("a", ctypes.c_ubyte),
    )


class color_rgba(ctypes.Union):
    _anonymous_ = ("rgba",)
    _fields_ = (
        ("m_comps", ctypes.c_ubyte * 4),
        ("rgba", RGBA)
    )

DDS_FORMATS_BLOCK_SIZE = {
    "DXT1": (8, bc7.unpack_bc1),
    "BC7": (16, bc7.unpack_bc7),
}


class  bc7enc_compress_block_params(ctypes.Structure):
    _fields_ = (
        ("m_mode_mask", ctypes.c_uint32 ),
        ("m_max_partitions", ctypes.c_uint32),
        ("m_weights", ctypes.c_uint32 * 4),
        ("m_uber_level", ctypes.c_uint32),
        ("m_perceptual", ctypes.c_bool),
        ("m_try_least_squares", ctypes.c_bool),
        ("m_mode17_partition_estimation_filterbank", ctypes.c_bool),
        ("m_force_alpha", ctypes.c_bool),
        ("m_force_selectors", ctypes.c_bool),
        ("m_selectors", ctypes.c_ubyte * 16),
        ("m_quant_mode6_endpoints", ctypes.c_bool),
        ("m_bias_mode1_pbits", ctypes.c_bool),
        ("m_pbit1_weight", ctypes.c_float),
        ("m_mode1_error_weight", ctypes.c_float),
        ("m_mode5_error_weight", ctypes.c_float),
        ("m_mode6_error_weight", ctypes.c_float),
        ("m_mode7_error_weight", ctypes.c_float),
        ("m_low_frequency_partition_weight", ctypes.c_float),
    )
        #uint32_t m_mode_mask;
        #uint32_t m_max_partitions;
        #uint32_t m_weights[4];
        #uint32_t m_uber_level;
        #bool m_perceptual;
        #bool m_try_least_squares;
        #bool m_mode17_partition_estimation_filterbank;
        #bool m_force_alpha;
        #bool m_force_selectors;
        #uint8_t m_selectors[16];
        #bool m_quant_mode6_endpoints;
        #bool m_bias_mode1_pbits;
        #float m_pbit1_weight;
        #float m_mode1_error_weight;
        #float m_mode5_error_weight;
        #float m_mode6_error_weight;
        #float m_mode7_error_weight;
        #float m_low_frequency_partition_weight;

def bc7enc_compress_block_params_init():
    p = bc7enc_compress_block_params(
        m_mode_mask=0xFFFFFFFF,
        m_max_partitions=64,
        m_try_least_squares=True,
        m_mode17_partition_estimation_filterbank=True,
        m_uber_level=0,
        m_force_selectors=False,
        m_force_alpha=False,
        m_quant_mode6_endpoints=False,
        m_bias_mode1_pbits=False,
        m_pbit1_weight=1.0,
        m_mode1_error_weight=1.0,
        m_mode5_error_weight=1.0,
        m_mode6_error_weight=1.0,
        m_mode7_error_weight=1.0,
        m_low_frequency_partition_weight=1.0,
        m_perceptual=True,
        m_weights=(ctypes.c_uint * 4)(128, 64, 16, 32),
    )
    return p


"""

inline void bc7enc_compress_block_params_init_perceptual_weights(bc7enc_compress_block_params *p)
{
	p->m_perceptual = true;
	p->m_weights[0] = 128;
	p->m_weights[1] = 64;
	p->m_weights[2] = 16;
	p->m_weights[3] = 32;
}


inline void bc7enc_compress_block_params_init(bc7enc_compress_block_params *p)
{
	p->m_mode_mask = UINT32_MAX;
	p->m_max_partitions = BC7ENC_MAX_PARTITIONS;
	p->m_try_least_squares = true;
	p->m_mode17_partition_estimation_filterbank = true;
	p->m_uber_level = 0;
	p->m_force_selectors = false;
	p->m_force_alpha = false;
	p->m_quant_mode6_endpoints = false;
	p->m_bias_mode1_pbits = false;
	p->m_pbit1_weight = 1.0f;
	p->m_mode1_error_weight = 1.0f;
	p->m_mode5_error_weight = 1.0f;
	p->m_mode6_error_weight = 1.0f;
	p->m_mode7_error_weight = 1.0f;
	p->m_low_frequency_partition_weight = 1.0f;
	bc7enc_compress_block_params_init_perceptual_weights(p);
}
"""



"""
struct bc7enc_compress_block_params
{
	uint32_t m_mode_mask;
	uint32_t m_max_partitions;
	uint32_t m_weights[4];
	uint32_t m_uber_level;
	bool m_perceptual;
	bool m_try_least_squares;
	bool m_mode17_partition_estimation_filterbank;
	bool m_force_alpha;
	bool m_force_selectors;
    uint8_t m_selectors[16];
	bool m_quant_mode6_endpoints;
    bool m_bias_mode1_pbits;
	float m_pbit1_weight;
	float m_mode1_error_weight;
	float m_mode5_error_weight;
	float m_mode6_error_weight;
	float m_mode7_error_weight;
	float m_low_frequency_partition_weight;
"""

COLORS_PER_BLOCK = 16


def pack_bc7(rgba_bytes, params):
    # TODO: do more than one block of 16x16 rgba pixels
    bc7.bc7_init()  # FIXME: global init
    dst_block = ctypes.create_string_buffer(16)
    rgba_ctypes = ctypes.create_string_buffer(rgba_bytes)

    bc7.pack_bc7_block(ctypes.byref(dst_block), ctypes.byref(rgba_ctypes), ctypes.byref(params))

    return bytes(dst_block)


def compress_bc7_image(rgba, width, height):
    bc7.bc7_init()  # FIXME: global init
    bc7_params = bc7enc_compress_block_params_init()

    # TODO: assert power of 2
    num_pixels = width * height
    num_bytes = num_pixels * 4
    num_blocks = num_bytes // 64
    size_bc7_block = 16

    rgba = array("B", rgba)
    rgba_addr, _  = rgba.buffer_info()
    rgba_ptr = ctypes.c_void_p(rgba_addr)

    blocks = ctypes.create_string_buffer(num_blocks * size_bc7_block)
    blocks_ptr = ctypes.byref(blocks)

    params_ptr = ctypes.byref(bc7_params)

    w = ctypes.c_int(width)
    h = ctypes.c_int(height)

    bc7.compress_image(rgba_ptr, w, h, blocks_ptr, params_ptr)
    return bytes(blocks)


def unpack_dds(file_handle, width, height, dds_format, data_offset):

    if dds_format not in DDS_FORMATS_BLOCK_SIZE:
        raise TypeError(f"Invalid DDS format: {dds_format}")

    SIZE_BLOCK, unpack_func = DDS_FORMATS_BLOCK_SIZE[dds_format]

    num_pixels = height * width
    num_colors = num_pixels * 4
    num_blocks = num_colors // COLORS_PER_BLOCK // 4
    size_blocks = num_blocks * SIZE_BLOCK


    file_handle.seek(data_offset)
    rgba = ctypes.create_string_buffer(width * height * 4)
    blocks_processed = 0

    for h in range(0, height, 4):
        for w in range(0, width, 4):
            block_bytes = ctypes.create_string_buffer(file_handle.read(SIZE_BLOCK))
            result_pixels = (color_rgba * 16)()
            if dds_format == "DXT1":
                unpack_func(ctypes.byref(block_bytes), ctypes.byref(result_pixels), True, 0)  # TODO: create actual enum
            else:
                unpack_func(ctypes.byref(block_bytes), ctypes.byref(result_pixels))

            bc7.rearrange_pixels(byref(result_pixels), byref(rgba), w, h, width, height)
            blocks_processed += 1

    assert blocks_processed == num_blocks, f"blocks processed: {blocks_processed}, {num_blocks}"

    return rgba
