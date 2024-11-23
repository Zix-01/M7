from rest_framework import serializers
import re


class YouTubeValidator:
    def __call__(self, value):
        youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/)?([a-zA-Z0-9_-]{11})$'
        if not re.match(youtube_regex, value):
            raise serializers.ValidationError("Ссылки разрешены только на youtube.com")
