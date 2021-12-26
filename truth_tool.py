# For viewing and assigning labels to training data.
# Label file comprises lines of the form:
#  image_file_name,p1x,p1y,p2x,p2y,p3x,p3y,p4x,p4y
# or
#  image_file_name,p1x,p1y,p2x,p2y,die_type,die_value

import sys

FILE_LABEL_LEN = 9

def parse_labels(labels_f):
  ls = []

  for l in labels_f.readlines():
    ts = l[:-1].split(',')
    ls.append([ts[0]] + [int(t) for t in ts[1:]])

  return ls

def main():
  if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} labels.csv imagefile')
    exit(1)

  labels_fn, image_fn = sys.argv[1:]
  with open(labels_fn, 'r+') as labels_f:
    labels = parse_labels(labels_f)

    # Existing labels for this image and the dice in it.
    label_idxs, file_label_idxs = [], []
    for i, l in enumerate(labels):
      (file_label_idxs if len(l) == FILE_LABEL_LEN else label_idxs).append(i)
    file_label_idx = None if not file_label_idxs else file_label_idxs[0]

    print(label_idxs, file_label_idxs)

if __name__ == '__main__':
  main()
