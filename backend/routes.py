from transcriber import get_audio_url_from_youtube, transcribe_audio_from_url, summarize_text

youtube_url = "https://www.youtube.com/watch?v=abc123"
audio_url = get_audio_url_from_youtube(youtube_url)
text = transcribe_audio_from_url(audio_url)
summary = summarize_text(text)

print(summary)
