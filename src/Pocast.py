import pydub
import os

from pydub import AudioSegment


class Podcast:
    def __init__(self, name, make_edit=False, silence_thresh=-50, min_silence_len=2000):
        self.name = name
        self.make_edit = make_edit
        self.silence_thresh = silence_thresh
        self.min_silence_len = min_silence_len

    def convert_video_to_audio(self, file_name):
        print(f'>> Podcast -> convert_video_to_audio - {file_name}')
        if not os.path.isdir('temp'):
            os.mkdir('temp')

        video = AudioSegment.from_file(f'temp/{file_name}.mp4')
        video.export(f'temp/{file_name}.mp3', format='mp3')

    def load_audio(self, file_name):
        print(f'>> Podcast -> load_audio - {file_name}')
        return AudioSegment.from_mp3(f'temp/{file_name}.mp3')

    def export_audio(self, audio_segment, name):
        print(f'>> Podcast ->  export_audio - {name}')
        return audio_segment.export(f'storage/{name}.mp3', format='mp3')

    def cut_silence(self, base_audio):
        print(f'>> Podcast -> cut_silence')
        silence_moments = pydub.silence.detect_silence(
            base_audio, silence_thresh=self.silence_thresh, min_silence_len=self.min_silence_len)
        edited_audio = AudioSegment.empty()
        lastStart = 0
        for moment in silence_moments:
            edited_audio += base_audio[lastStart:moment[0]]
            lastStart = moment[1]
        edited_audio += base_audio[lastStart:]
        return edited_audio

    def process(self, original_media_name, intro_music_name, end_music_name):
        try:
            print(f'>> Podcast -> process started')
            original_media = original_media_name.split('.')[0]
            self.convert_video_to_audio(original_media)

            original_audio = self.load_audio(original_media)
            intro_music = self.load_audio(intro_music_name.split('.')[0])
            end_music = self.load_audio(end_music_name.split('.')[0])

            if (self.make_edit):
                original_audio = self.cut_silence(original_audio)

            final = intro_music.append(original_audio, crossfade=1500)
            final = final.append(end_music, crossfade=1500)

            self.export_audio(final, name=self.name)
            print(f'>> Podcast -> process done')
        except:
            print(f'>> Podcast -> process failed')
            pass


# podcast = Podcast('test')
# podcast.process('flow.mp4', 'intro.mp3', 'intro.mp3')
