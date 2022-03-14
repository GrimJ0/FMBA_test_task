import os
from pprint import pprint

labels_dir = "/tmp/labels"
os.makedirs(labels_dir, exist_ok=True)
labels = {
    "label1": ["1image.JPG", "2.jpeg", "2.json", "1image.json", "3.jpg"],
    "label2": ["1.jpg", "1.json", "2.json", "3.json"],
    "label3": ["15.png", "15.json", "16.json", "16.jpg", "1.PNG", "1.JSON"],
    "label4": ["1.png", "1.txt", "2.txt", ],
}
for label in labels:
    label_path = os.path.join(labels_dir, label)
    os.makedirs(label_path, exist_ok=True)
    for item in labels[label]:
        open(os.path.join(label_path, item), 'a').close()
    print(f"{label_path} {os.listdir(label_path)}")
open(os.path.join(labels_dir, "test.txt"), 'a').close()


def get_file(path: str) -> list:
    found_items = []
    tmp_label = []
    tmp_file = {}

    for file in os.listdir(path):
        file_path = f"{path}/{file}"
        if os.path.isdir(file_path):
            found_items += get_file(file_path)
        else:
            filepath, file_extension = os.path.splitext(file_path)
            filename = os.path.split(filepath)[-1]

            if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
                tmp_file.setdefault('img', {}).update({filename: file_path})

            elif file_extension.lower() == '.json':
                tmp_file.setdefault('json', {}).update({filename: file_path})

    json = tmp_file.get('json')
    img = tmp_file.get('img')
    label = os.path.split(path)[-1]

    if json and img:
        for key, value in json.items():
            if key in img:
                tmp_label.append([img[key], json[key]])

        found_items.append({label: tmp_label})

    return found_items


if __name__ == '__main__':
    print()
    pprint(get_file(labels_dir))

    """
    Должен получиться следующий ответ:
        [{"label1" : [
                  ['/tmp/labels/label1/2.jpeg', '/tmp/labels/label1/2.json'],
                  ['/tmp/labels/label1/1image.JPG', '/tmp/labels/label1/1image.json']
              ]
          },
        {"label2" : [
                ['/tmp/labels/label2/1.jpg', '/tmp/labels/label2/1.json']
            ]
        },
        {"label3" : [
                  ['/tmp/labels/label3/1.PNG', '/tmp/labels/label3/1.JSON'],
                  ['/tmp/labels/label3/16.jpg', '/tmp/labels/label3/16.json'],
                  ['/tmp/labels/label3/15.png', '/tmp/labels/label3/15.json']
              ]
          }
        ]
    """

