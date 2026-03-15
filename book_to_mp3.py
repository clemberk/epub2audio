import os
import json
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from InquirerPy import inquirer
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

BOOK_PATH="./books/darkage.epub"
OUTPUT_DIR="./output/"

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def extract_chapters(epub_path):
    if not os.path.exists(epub_path):
        print(f"Error: File {epub_path} not found. Aborting...")
        return []

    book = epub.read_epub(epub_path)
    chapters = []

    for item in book.get_items():
        
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content()
            soup = BeautifulSoup(content, 'html.parser')
            
            title = soup.find(['h1', 'h2', 'h3'])
            chapter_title = title.get_text().strip() if title else item.get_name()
            
            text_content = soup.get_text(separator=' ').strip()
            
            if len(text_content.strip()) > 50: 
                chapters.append({
                    'title': chapter_title,
                    'content': text_content.strip()
                })
    
    return chapters


def console_selection(chapter_list):
    if not chapter_list:
        print("No Chapters found to choose from. Aborting...")
        return []

    choices = [ch['title'] for ch in chapter_list]
    
    selected_titles = inquirer.checkbox(
        message="Choose chapters to export (Space to check, Enter to apply):",
        choices=choices,
        pointer="👉",
        enabled_symbol="✅",
        disabled_symbol="⬜"
    ).execute()

    final_output = []
    for title in selected_titles:
        for ch in chapter_list:
            if ch['title'] == title:
                final_output.append({
                    "chapter_title": ch['title'],
                    "chapter_text": ch['content']
                })
                break 

    return final_output

def text_to_speech_file(text: str, chapter_num: int, chapter_name: str, output_path: str) -> str:
    print(f"Generating Audio for chapter {chapter_num}: {chapter_name}...")
    
    try:
        response = client.text_to_speech.convert(
            voice_id="NBqeXKdZHweef6y0B67V", # Christian Voice
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_flash_v2_5",
        )

        save_file_path = f"./output/{chapter_num:02d}_{chapter_name[:20]}.mp3"

        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"Chapter saved successfully: {save_file_path}")
        return save_file_path
    except Exception as e:
        print(f"Error in chapter {chapter_num}: {e}")
        return ""

if __name__ == "__main__":

    # Extract Chapters
    print(f"Reading Book: {BOOK_PATH}...")
    all_chapters = extract_chapters(BOOK_PATH)

    # Choosing Chapters
    selected_chapters = console_selection(all_chapters)

    print(selected_chapters)

    # Generate Audio
    if not selected_chapters:
        print("Nothing selected. Aborting...")
    else:
        print(f"\nStarting Text-To-Speech for {len(selected_chapters)} chapter(s)...\n")

        for index, chapter in enumerate(selected_chapters, 1):
            text_to_speech_file(
                text=chapter['chapter_text'], 
                chapter_num=index, 
                chapter_name=chapter['chapter_title'],
                output_path=OUTPUT_DIR
            )

            print("\n--- Successfully completed all chapters! ---")