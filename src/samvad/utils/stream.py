import os

# import moviepy
from faster_whisper import WhisperModel

# cuda_bin_path = r"C:\Program Files\NVIDIA\CUDNN\v9.17\bin\13.1"
# os.environ["PATH"] = cuda_bin_path + os.pathsep + os.environ["PATH"]

model = WhisperModel("small", device="cuda", compute_type="float16")
segments, info = model.transcribe(
    os.path.join(".", "oyama.mov"), beam_size=1, log_progress=False
)

print(
    "Detected language '%s' with probability %f"
    % (info.language, info.language_probability)
)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
