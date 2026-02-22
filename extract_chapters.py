import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_chapters(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []

    
    for item in book.get_items():
        
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content()
            soup = BeautifulSoup(content, 'html.parser')
            
            title = soup.find(['h1', 'h2', 'h3'])
            chapter_title = title.get_text().strip() if title else item.get_name()
            
            text_content = soup.get_text(separator=' ')
            
            if len(text_content.strip()) > 100: 
                chapters.append({
                    'title': chapter_title,
                    'content': text_content.strip()
                })
    
    return chapters

chapters = extract_chapters("darkage.epub")

for i, ch in enumerate(chapters):
    print(f"Kapitel {i+1}: {ch['title']} ({len(ch["content"])}) Zeichen)")

# Beispielaufruf
# chapters = extract_chapters('mein_buch.epub')
# for i, ch in enumerate(chapters):
#     print(f"Kapitel {i+1}: {ch['title']} ({len(ch['content'])} Zeichen)")