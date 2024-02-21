#import sys
#sys.path.append('/home/nalewak/vision_system/plan_view')
#sys.path.append('/home/nalewak/vision_system/network')
#sys.path.append('/home/nalewak/vision_system/correct')


from .plan_view.plan_view import plan_view
from .network.detect_mug import detect_objects
from .correct.crop import crop_photo  # Załóżmy, że ta funkcja przycina zdjęcie
from .correct.correct import correct_photo
from .take_photo import take_photo


def vision_system():
    take_photo()
    correct_photo()
    crop_photo()
    detect_objects()
    plan_view()


if __name__ == "__main__":
    main()
