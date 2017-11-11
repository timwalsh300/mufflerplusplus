from libc.stdint cimport int16_t, int32_t

cdef extern from "opus/opus_multistream.h":
    ctypedef struct OpusMSEncoder:
        pass

    ctypedef struct OpusMSDecoder:
        pass

    OpusMSEncoder *opus_multistream_encoder_create(int32_t Fs,
                                                 int channels,
                                                 int streams,
                                                 int coupled_streams,
                                                 const unsigned char *mapping,
                                                 int application,
                                                 int *error)

    int32_t opus_multistream_encode(OpusMSEncoder *st,
                                          const int16_t *pcm,
                                          int frame_size,
                                          unsigned char *data,
                                          int32_t max_data_bytes)

    int opus_multistream_encoder_ctl(OpusMSEncoder *st, int request, ...)

    void opus_multistream_encoder_destroy(OpusMSEncoder *st)

    int opus_multistream_encoder_get_size(int channels, int coupled_streams)

    OpusMSDecoder *opus_multistream_decoder_create(int32_t Fs,
                                                    int channels,
                                                    int streams,
                                                    int coupled_streams,
                                                    const unsigned char *mapping,
                                                    int *error)

    int opus_multistream_decode(OpusMSDecoder *st,
                                const unsigned char *data,
                                int32_t len,
                                int16_t *pcm,
                                int frame_size,
                                int decode_fec)

    void opus_multistream_decoder_destroy(OpusMSDecoder *st)
