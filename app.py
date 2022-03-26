from flask import Flask, render_template, request, redirect, url_for, send_file
from dotenv import load_dotenv
import youtube_dl
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_link = request.form['videoLink']
        conversion_type = request.form['conversionType']

        savedir = "content"
        if not os.path.exists(savedir):
            os.makedirs(savedir)

        #video 
        if conversion_type == "mp4":
            options = {
                "outtmpl": "%(title)s"
            }
            
        #audio
        elif conversion_type == "mp3":
            options = {
                "outtmpl": "%(title)s",
                "extractaudio": True, #extracts the audio
                "audioformat": "mp3",
                "format": "bestaudio/best",
                "noplaylist": True #single songs only
            }

        with youtube_dl.YoutubeDL(options) as ydl:
            content = ydl.extract_info(video_link)
            ydl.download([video_link])
            savepath =os.path.join(savedir, f"{content['title']}--{content['uploader']}.{conversion_type}")
            filename = os.rename(content['title'], savepath)

        return redirect(url_for('download', filename=str(savepath)))
    return render_template("index.html")


@app.route("/download/<filename>", methods=['GET', 'POST'])
def download(filename):
    if request.method == 'POST':
        path = filename
        return send_file(path, as_attachment=True)

    return render_template("download.html", filename=filename)



if __name__=='__main__':
    app.run(debug=True, port=5001)