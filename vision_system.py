#import sys
#sys.path.append('/home/nalewak/vision_system/plan_view')
#sys.path.append('/home/nalewak/vision_system/network')
#sys.path.append('/home/nalewak/vision_system/correct')


from .plan_view.plan_view import plan_view
from .network.detect_mug import detect_objects
from .correct.crop import crop_photo
from .correct.correct import correct_photo
from .take_photo import take_photo


def vision_system():
    img = take_photo()
    img  = correct_photo(img)
    img = crop_photo(img)
    detect_objects(img)
    centers = plan_view(img)
    return centers


if __name__ == "__main__":
    main()
