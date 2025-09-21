# Free Text from YouTube Video or Audio File

A small Python script that converts **YouTube videos** or **audio files** into full text.

You can provide:

* A YouTube link
* A remote audio file URL
* A local audio file path

The script outputs the transcription directly in your console and also saves it to a text file named `generated_output.txt`.

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/brahimrida/free_text_from_youtube_video_or_audio_file.git
```

### Or Download as ZIP

* Scroll to the top of this page.
* Click the blue **Code** button.
* Select **Download ZIP**.

---


## 🎥 Install FFMPEG

This project requires **FFMPEG** to handle video and audio processing.

### Windows (with Chocolatey)

If you have [Chocolatey](https://chocolatey.org/install) installed, simply run:

```bash
choco install ffmpeg
```

### macOS (with Homebrew)

```bash
brew install ffmpeg
```

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install ffmpeg
```

After installation, verify with:

```bash
ffmpeg -version
```

---


## 🐍 Python Virtual Environment Setup (Windows)

1. Open **PowerShell** or **CMD**.

2. Create a virtual environment:

   ```bash
   python -m venv my_project_env
   ```

   *(You can replace `my_project_env` with any name you like.)*

3. Activate the virtual environment:

   * **CMD**

     ```bash
     my_project_env\Scripts\activate.bat
     ```
   * **PowerShell**

     ```bash
     my_project_env\Scripts\Activate.ps1
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Run the script with:

```bash
python speech_demo.py <YouTube link or audio path> <flag> <chunks-output-directory>
```

### Examples

**YouTube video transcription:**

```bash
python speech_demo.py https://youtu.be/LzInU71ljJQ?si=_xxxLVIdNDvfBT8d -y C:/path-to-folder/chunks/
```

**Remote or local audio file transcription:**

```bash
python speech_demo.py C:/path-to-audio/audio-file.wav -u C:/path-to-folder/chunks/
```

or

```bash
python speech_demo.py https://www.example.com/audio.wav -u C:/path-to-folder/chunks/
```

Here’s the section you can copy directly:

---

## 🎌 Flags Explanation

* **`-y`** → Use when providing a **YouTube video link**.
* **`-u`** → Use when providing a **local audio file path** or a **remote audio file URL**.

---

## 📂 Example Files

The project includes an **`audio.wav`** file, which is an example taken from a **Chef Gordon Ramsay cooking session on YouTube**.

* This file was generated from the video.
* The **`generated_output.txt`** file contains the full transcription of Chef Ramsay’s cooking session.

---


