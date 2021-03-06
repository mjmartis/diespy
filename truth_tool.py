# For viewing and assigning labels to training data.
# Label file comprises lines of the form:
#  image_file_name,p1x,p1y,p2x,p2y,p3x,p3y,p4x,p4y
# or
#  image_file_name,p1x,p1y,p2x,p2y,rot,die_type,die_value

import sys
import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
from functools import partial

FILE_LABEL_LEN = 9
WIN_DIMS = '1200x800'
CANVAS_DIM = 700
SCROLL_MAG = 3
POINT_RAD = 5


def parse_labels(labels_f):
  ls = []

  for l in labels_f.readlines():
    ts = l[:-1].split(',')

    ds = [ts[0]]
    if len(l) == FILE_LABEL_LEN:
      ds += [int(t) for t in ts[1:]]
    else:
      ds += [int(t) for t in ts[1:5]]
      ds += [float(ts[5])]
      ds += [int(t) for t in ts[6:]]

    ls.append(ds)

  return ls


class TruthToolWindow:

  def __init__(self, image_fn):
    self._proj_vertices = []

    self._root = None
    self._frame = None
    self._img = None
    self._canvas = None

    self._root = tk.Tk()
    self._root.geometry(WIN_DIMS)

    # Add a frame that can display our source image with scroll bars.
    self._frame = tk.Frame(self._root, width=CANVAS_DIM, height=CANVAS_DIM)
    self._frame.pack(anchor=tk.NW, fill=None, expand=False)
    self._frame.pack_propagate(0)

    # Add a canvas that actually displays our source image.
    self._img = ImageTk.PhotoImage(Image.open(image_fn))
    self._canvas = tk.Canvas(
        self._frame, scrollregion=(0, 0, self._img.width(), self._img.height()))

    # Add scroll bars.
    hbar = tk.Scrollbar(self._frame, orient=tk.HORIZONTAL)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)
    hbar.config(command=self._canvas.xview)
    vbar = tk.Scrollbar(self._frame, orient=tk.VERTICAL)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    vbar.config(command=self._canvas.yview)
    self._canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    # Scroll image via arrow keys.
    def scroll(d, back, e):
      name = ('x' if d else 'y') + 'view_scroll'
      method = getattr(self._canvas, name)
      method((-1 if back else 1) * SCROLL_MAG, 'units')

    self._root.bind_all('<Left>', partial(scroll, True, True))
    self._root.bind_all('<Right>', partial(scroll, True, False))
    self._root.bind_all('<Up>', partial(scroll, False, True))
    self._root.bind_all('<Down>', partial(scroll, False, False))

    # Make our self._canvas fill the whole self._frame.
    self._canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    self._canvas.create_image(0, 0, anchor=tk.NW, image=self._img)

    # Allow drawing on canvas.
    self._canvas.bind("<ButtonPress-1>", lambda e: self._HandleClick(e))

  def _HandleClick(self, e):
    # Clear old rect if we are starting a new one.
    if len(self._proj_vertices) == 4:
      self._canvas.create_image(0, 0, anchor=tk.NW, image=self._img)
      self._proj_vertices = []

    x, y = self._canvas.canvasx(e.x), self._canvas.canvasy(e.y)
    self._DrawPoint(x, y, 'red')
    self._proj_vertices.append((x, y))

    # Draw quad defined by points.
    if len(self._proj_vertices) == 4:
      for i in range(4):
        ax, ay = self._proj_vertices[i]
        bx, by = self._proj_vertices[(i + 1) % 4]

        self._canvas.create_line(ax, ay, bx, by, fill='red')

  def _DrawPoint(self, x, y, col):
    self._canvas.create_oval(
        x - POINT_RAD,
        y - POINT_RAD,
        x + POINT_RAD,
        y + POINT_RAD,
        outline=col,
        fill=col)

  def RunMainLoop(self):
    self._root.mainloop()


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
    file_label_idx = None if not file_label_idxs else file_label_idxs[-1]

    win = TruthToolWindow(image_fn)
    win.RunMainLoop()


if __name__ == '__main__':
  main()
