from typing import Dict, List
import moviepy.editor
import json
from dataclasses import dataclass

video = moviepy.editor.VideoFileClip("sample.mp4")

@dataclass
class Word:
    word: str
    confidence: float
    start_sec: float
    end_sec: float

words = [
    Word(**word)
    for word in json.load(open("recognized_words.json"))
]

words_dict: Dict[str, List[Word]] = {}

for word in words:
    words_dict.setdefault(word.word.casefold(), []).append(word)

for word_list in words_dict.values():
    word_list.sort(key=lambda word: word.confidence, reverse=True)

script = open("script.txt").read()

result_parts = []

for word in script.split():
    word = words_dict[word.casefold()][0]
    result_parts.append(video.subclip(max(0, word.start_sec - 0.1), min(video.end, word.end_sec + 0.1)))

moviepy.editor.concatenate_videoclips(result_parts).write_videofile("result.mp4")
