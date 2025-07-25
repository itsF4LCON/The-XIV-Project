from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import yt_dlp
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/links")
def links():
    return render_template("links.html")

@app.route("/youtube", methods=["GET", "POST"])
def youtube_downloader():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            flash("Please enter a valid YouTube URL")
            return redirect(url_for("youtube_downloader"))

        try:
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'format': 'best'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            flash(f"✅ Download completed: {info.get('title', 'Video')}")
            return send_file(filename, as_attachment=True)

        except Exception as e:
            flash(f"❌ Error: {e}")
            return redirect(url_for("youtube_downloader"))

    return render_template("youtube.html")

if __name__ == "__main__":
    app.run(debug=True)
