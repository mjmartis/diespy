# For viewing and assigning labels to training data.
# Label file comprises lines of the form:
#  image_file_name,p1x,p1y,p2x,p2y,p3x,p3y,p4x,p4y
# or
#  image_file_name,p1x,p1y,p2x,p2y,die_type,die_value

import sys
import tkinter as tk
from PIL import ImageTk, Image

FILE_LABEL_LEN = 9
WIN_DIMS = '1200x800'
CANVAS_DIM = 600

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

  root = tk.Tk()
  root.geometry(WIN_DIMS)

  # Add a frame that can display our source image with scroll bars.
  frame = tk.Frame(root, width=CANVAS_DIM, height=CANVAS_DIM)
  frame.pack(anchor=tk.NW, fill=None, expand=False)
  frame.pack_propagate(0)

  # Add a canvas that actually displays our source image.
  img = ImageTk.PhotoImage(Image.open(image_fn))
  canvas = tk.Canvas(frame, scrollregion=(0, 0, img.width(), img.height()))

  # Add scroll bars.
  hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
  hbar.pack(side=tk.BOTTOM, fill=tk.X)
  hbar.config(command=canvas.xview)
  vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
  vbar.pack(side=tk.RIGHT, fill=tk.Y)
  vbar.config(command=canvas.yview)
  canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

  # Make our canvas fill the whole frame.
  canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
  canvas.create_image(0, 0, anchor=tk.NW, image=img)

  root.mainloop()

if __name__ == '__main__':
  main()
