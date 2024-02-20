import sys
sys.path.append('./plan_view')
sys.path.append('./network')
sys.path.append('./correct')


from plan_view.plan_view import plan_view
from network.detect_mug import detect_objects
from correct.crop import crop_photo  # Załóżmy, że ta funkcja przycina zdjęcie
# Załóżmy, że ta funkcja prostuje zdjęcie i zwraca ścieżkę do wyprostowanego zdjęcia
from correct.correct import correct_photo
# Załóżmy, że ta funkcja robi zdjęcie i zwraca ścieżkę do tego zdjęcia
from take_photo import take_photo


def main():
    take_photo()
    correct_photo()
    crop_photo()
    detect_objects()
    plan_view()


if __name__ == "__main__":
    main()
