import os
import pathlib
import librosa
import whisper
from modelscope.tools import run_auto_label

from modelscope.models.audio.tts import SambertHifigan
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

from modelscope.metainfo import Trainers
from modelscope.trainers import build_trainer
from modelscope.utils.audio.audio_utils import TtsTrainType

pretrained_model_id = 'damo/speech_personal_sambert-hifigan_nsf_tts_zh-cn_pretrain_16k'

dataset_id = "output_training_data/"
pretrain_work_dir = "pretrain_work_dir/"

whisper_size = "base"
whisper_model = whisper.load_model(whisper_size)

def auto_label(audio):
    try:
        split_long_audio(whisper_model, audio, "test_wavs")
        input_wav = "test_wavs/"
        output_data = "output_training_data/"
        ret, report = run_auto_label(input_wav=input_wav, work_dir=output_data, resource_revision="v1.0.7")
        print(ret,report)
    except Exception:
        pass
    return "标注成功"


def train(a):
    try:
        train_info = {
            TtsTrainType.TRAIN_TYPE_SAMBERT: {  # 配置训练AM（sambert）模型
                'train_steps': 52,               # 训练多少个step
                'save_interval_steps': 50,       # 每训练多少个step保存一次checkpoint
                'log_interval': 10               # 每训练多少个step打印一次训练日志
            }
        }

        # 配置训练参数，指定数据集，临时工作目录和train_info
        kwargs = dict(
            model=pretrained_model_id,                  # 指定要finetune的模型
            model_revision = "v1.0.6",
            work_dir=pretrain_work_dir,                 # 指定临时工作目录
            train_dataset=dataset_id,                   # 指定数据集id
            train_type=train_info                       # 指定要训练类型及参数
        )

        trainer = build_trainer(Trainers.speech_kantts_trainer,
                            default_args=kwargs)

        trainer.train()

    except Exception:
        pass

    return "训练完成"


import random

def infer(text):

  model_dir = "/pretrain_work_dir"

  custom_infer_abs = {
      'voice_name':
      'F7',
      'am_ckpt':
      os.path.join(model_dir, 'tmp_am', 'ckpt'),
      'am_config':
      os.path.join(model_dir, 'tmp_am', 'config.yaml'),
      'voc_ckpt':
      os.path.join(model_dir, 'orig_model', 'basemodel_16k', 'hifigan', 'ckpt'),
      'voc_config':
      os.path.join(model_dir, 'orig_model', 'basemodel_16k', 'hifigan',
              'config.yaml'),
      'audio_config':
      os.path.join(model_dir, 'data', 'audio_config.yaml'),
      'se_file':
      os.path.join(model_dir, 'data', 'se', 'se.npy')
  }
  kwargs = {'custom_ckpt': custom_infer_abs}

  model_id = SambertHifigan(os.path.join(model_dir, "orig_model"), **kwargs)

  inference = pipeline(task=Tasks.text_to_speech, model=model_id)
  output = inference(input=text)

  filename = str(random.randint(1, 1000000000000))

  with open(filename + "myfile.wav", mode='bx') as f:
      f.write(output["output_wav"])
  return filename + "myfile.wav"

def split_long_audio(model, filepaths, save_dir="data_dir", out_sr=44100):
    if isinstance(filepaths, str):
        filepaths = [filepaths]

    for file_idx, filepath in enumerate(filepaths):

        save_path = pathlib.Path(save_dir)
        save_path.mkdir(exist_ok=True, parents=True)

        print(f"Transcribing file {file_idx}: '{filepath}' to segments...")
        result = model.transcribe(filepath, word_timestamps=True, task="transcribe", beam_size=5, best_of=5)
        segments = result['segments']

        wav, sr = librosa.load(filepath, sr=None, offset=0, duration=None, mono=True)
        wav, _ = librosa.effects.trim(wav, top_db=20)
        peak = np.abs(wav).max()
        if peak > 1.0:
            wav = 0.98 * wav / peak
        wav2 = librosa.resample(wav, orig_sr=sr, target_sr=out_sr)
        wav2 /= max(wav2.max(), -wav2.min())

        for i, seg in enumerate(segments):
            start_time = seg['start']
            end_time = seg['end']
            wav_seg = wav2[int(start_time * out_sr):int(end_time * out_sr)]
            wav_seg_name = f"{file_idx}_{i}.wav"
            out_fpath = save_path / wav_seg_name
            wavfile.write(out_fpath, rate=out_sr, data=(wav_seg * np.iinfo(np.int16).max).astype(np.int16))