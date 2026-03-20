import os

def get_latest_image(folder):
    images = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg','.png','.jpeg'))]
    if not images:
        return None
    images.sort(key=lambda x: os.path.getmtime(os.path.join(folder,x)), reverse=True)
    return os.path.join(folder, images[0])

def get_all_annotations(annot_dir, image_path):
    base = os.path.splitext(os.path.basename(image_path))[0]
    return [os.path.join(annot_dir,f) for f in os.listdir(annot_dir) if f.startswith(base)]


def get_latest_images(folder, count=2):
    images = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not images:
        return []
    images.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    return [os.path.join(folder, f) for f in images[:count]]
