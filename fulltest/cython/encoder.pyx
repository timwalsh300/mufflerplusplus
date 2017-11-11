from libc.stdint cimport int16_t, int32_t
from libc.stdio cimport FILE, fopen, fwrite, fclose
from libc.string cimport memcpy
from libc.stdlib cimport malloc, free
cimport opus

cdef class Encoder:

    cdef opus.OpusEncoder* _c_encoder

    cdef opus.OpusDecoder* _c_decoder

    cdef int _err

    cdef float _raw_data[6*960]

    cdef unsigned char _encoded_data[3*1276]

    cdef FILE *_shared_out

    # cdef FILE *_decoded_out

    def __cinit__(self):
        # first three arguments are for sample rate, channels, and AUDIO application mode
        self._c_encoder = opus.opus_encoder_create(48000, 1, 2049, &self._err)
        if self._err < 0:
            print("error creating encoder")
        # 4002 is a set bit rate request and 64000 is the rate to set
        self._err = opus.opus_encoder_ctl(self._c_encoder, 4002, 64000)
        if self._err < 0:
            print("error setting bitrate")
        # 4010 is a set complexity request and 10 is the level to set
        self._err = opus.opus_encoder_ctl(self._c_encoder, 4010, 10)
        if self._err < 0:
            print("error setting complexity")
        # self._c_decoder = opus.opus_decoder_create(48000, 1, &self._err)
        self._shared_out = fopen("shared_sample.pcm", "w")
        # self._decoded_out = fopen("decoded_sample.pcm", "w")

    def __dealloc__(self):
        if self._c_encoder is not NULL:
            opus.opus_encoder_destroy(self._c_encoder)
            # opus.opus_decoder_destroy(self._c_decoder)
            fclose(self._shared_out)
            # fclose(self._decoded_out)

    cpdef opus_encode_float(self, input, low_target, high_target, max_value):
        i = 0
        #trying max_value instead of 32768.0 in order to normalize things
        for x in input:
            self._raw_data[i] = x / max_value
            i += 1
        # Write this out to a file as a sanity check to make sure we didn't mess up audio during transfer
        fwrite(self._raw_data, 4, len(input), self._shared_out)
        cdef int32_t resulting_size
        # Make a copy of the encoder state so that we don't ruin it in case we miss our target
        cdef opus.OpusEncoder* encoder_copy = <opus.OpusEncoder *> malloc(opus.opus_encoder_get_size(1))
        memcpy(encoder_copy, self._c_encoder, opus.opus_encoder_get_size(1))
        # 960 is frame size in samples over 20 ms, and 3828 is max packet size taken from trivial example
        resulting_size = opus.opus_encode_float(encoder_copy, self._raw_data, 960, self._encoded_data, 3*1276)
        # If we are on target, update the good copy of the encoder state
        if low_target < resulting_size < high_target:
            memcpy(self._c_encoder, encoder_copy, opus.opus_encoder_get_size(1))
            # The following two lines are another sanity check - listen to the file written out
            # opus.opus_decode(self._c_decoder, self._encoded_data, resulting_size, self._raw_data, 6*960, 0)
            # fwrite(self._raw_data, 2, len(input), self._decoded_out)
        free(encoder_copy)
        return resulting_size
                
    cdef opus_encoder_get_size(self):
        # hardcoding 1 channel as input
        return opus.opus_encoder_get_size(1)
