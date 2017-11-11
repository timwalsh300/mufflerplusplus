import encoder
from pydub import AudioSegment

input_audio = AudioSegment.from_file("sci0222.pcm", format="raw", frame_rate=48000, channels=1, sample_width=2)
maxValue = max(input_audio.get_array_of_samples())
print('max value is ' + str(maxValue))
tester = encoder.Encoder()

for i in range(len(input_audio) // 20):
    frame = input_audio[i*20:i*20+20].get_array_of_samples()
    print('frame length is {}'.format(len(frame)))
    result = tester.opus_encode_float(frame, 10, 450, maxValue)
    print('packet size is {}'.format(result))
