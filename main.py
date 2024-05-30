import tkinter as tk
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import timedelta
import webbrowser
import os


def download_transcript():
    link = link_entry.get()

    try:
        yt = YouTube(link)
        title = yt.title
        transcripts_available = YouTubeTranscriptApi.list_transcripts(yt.video_id)

        # Verifica se há transcrições disponíveis
        transcript = next((transcript.fetch() for transcript in transcripts_available if transcript.language_code == 'pt'), None)

        if transcript is None:
            raise ValueError('Transcript in Portuguese not available.')

        # Cria o arquivo de transcrição
        with open(f'{title}.html', 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n<html>\n<head><style>body {font-family: Arial, sans-serif; font-size: 16px; padding: 20px;}</style></head>\n<body>\n")

            for line in transcript:
                time = timedelta(seconds=line['start'])
                formatted_time = str(time).split('.')[0]
                text = line['text']
                time_link = f'https://www.youtube.com/watch?v={yt.video_id}&t={time.seconds}s'
                formatted_line = f'<a href="{time_link}" target="_blank">{formatted_time}</a> - {text}<br>\n'
                file.write(formatted_line)

            file.write("</body>\n</html>")

        # Abre o arquivo no navegador
        webbrowser.open(f'file://{os.path.abspath(title)}.html')

        status_label.config(text='Transcript downloaded successfully!', fg='green')
    except ValueError as ve:
        status_label.config(text=str(ve), fg='red')
    except Exception as e:
        status_label.config(text='Error downloading transcript!', fg='red')


root = tk.Tk()
root.title("Download Transcript")
tk.Label(root, text="Enter the video link:").pack()
link_entry = tk.Entry(root, width=50)
link_entry.pack()
download_button = tk.Button(root, text="Download Transcript", command=download_transcript)
download_button.pack()
status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
