import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from InquirerPy import inquirer
import json
import os

BOOK_PATH="./books/darkage.epub"

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

def save_to_json(data, filename):
    if not data:
        print("Nothing selected. Aborting...")
        return

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\n--- SUCCESS ---")
    print(f"Successfully saved {len(data)} chapters to '{filename}'.")


if __name__ == "__main__":

    # Extract chapters
    print(f"Reading Book: {BOOK_PATH}...")
    all_chapters = extract_chapters(BOOK_PATH)

    # Choosing Chapters
    selected_data = console_selection(all_chapters)

    output_dir = "./output/"
    # 3. Export to JSON
    save_to_json(selected_data, f"{output_dir}export.json")