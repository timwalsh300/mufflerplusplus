from libc.stdint cimport int16_t, int32_t

cdef extern from "opus/opus.h":
    ctypedef struct OpusEncoder:
        pass

    ctypedef struct OpusDecoder:
        pass

    OpusEncoder *opus_encoder_create(int32_t Fs, int channels, int application, int *error)

    int32_t opus_encode_float(OpusEncoder *st, const float *pcm, int frame_size, unsigned char *data, int32_t max_data_bytes)

    int opus_encoder_ctl (OpusEncoder *st, int request, ...)

    void opus_encoder_destroy(OpusEncoder *st)

    int opus_encoder_get_size(int channels)

    OpusDecoder * opus_decoder_create(int32_t Fs, int channels, int *error)

    int opus_decode(OpusDecoder *st, const unsigned char *data, int32_t len, int16_t *pcm, int frame_size, int decode_fec)

    void opus_decoder_destroy(OpusDecoder *st)
