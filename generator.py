import os
import requests
import json
from gtts import gTTS

class RepoVideoAgent:
    """An autonomous agent designed to turn code logic into presentation material."""
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.script_output = "video_script.txt"
        self.audio_output = "voiceover.mp3"

    def read_codebase(self):
        """Scans the local folder for essential code files to summarize."""
        print(f"[1/4] Ingesting codebase properties inside: {self.repo_path}")
        code_summary = ""
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(('.py', '.ino', '.cpp', '.md')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', errors='ignore') as f:
                        code_summary += f"\n--- File: {file} ---\n" + f.read()[:500] # Grab first 500 chars
        return code_summary[:3000] # Limit to avoid token clutter

    def generate_ai_voice_script(self, code_text):
        """Uses a local LLM to generate a natural, engaging YouTube/social video script."""
        print("[2/4] Querying local AI agent to synthesize video narrative...")
        url = "http://localhost:11434/api/generate"
        prompt = f"Write a 30-second exciting video script explaining this code for a developer audience. Keep it concise, do not use stage directions:\n{code_text}"
        
        payload = {"model": "llama3", "prompt": prompt, "stream": False}
        try:
            response = requests.post(url, json=payload, timeout=15)
            script = response.json().get('response', 'Check out this awesome new repository codebase!')
            with open(self.script_output, 'w') as f:
                f.write(script)
            return script
        except Exception:
            fallback = "This repository features an automated backend system built cleanly in Python."
            return fallback

    def compile_audio_track(self, script_text):
        """Converts the text narrative track into physical speech audio waveforms."""
        print("[3/4] Running text-to-speech rendering engines...")
        tts = gTTS(text=script_text, lang='en')
        tts.save(self.audio_output)
        print(f"[4/4] Success! Dynamic media assets ready: {self.audio_output}")

if __name__ == "__main__":
    print("--- Autonomous Repo-To-Video Production Agent ---")
    # Point the agent to look inside its own local repository directory folder
    agent = RepoVideoAgent(repo_path=".")
    code_extracted = agent.read_codebase()
    video_script = agent.generate_ai_voice_script(code_extracted)
    agent.compile_audio_track(video_script)
