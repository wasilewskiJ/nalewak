import sys
sys.path.append('correct')  # Dodaje katalog 'correct' do ścieżki, aby móc zaimportować moduły

from take_photo import take_photo  # Załóżmy, że ta funkcja robi zdjęcie i zwraca ścieżkę do tego zdjęcia
from correct.correct import correct_photo  # Załóżmy, że ta funkcja prostuje zdjęcie i zwraca ścieżkę do wyprostowanego zdjęcia
from correct.crop  import crop_photo  # Załóżmy, że ta funkcja przycina zdjęcie

def main():
    take_photo()
    correct_photo()
    crop_photo()
if __name__ == "__main__":
    main()