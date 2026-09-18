#!/usr/bin/env python3
"""Regenerate the tracked SVG and PNG listing icon (developer-only Pillow dependency)."""

from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "plugins/author-voice/assets"
SIZE, SCALE = 512, 4
image = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE))
draw = ImageDraw.Draw(image)
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" role="img" aria-label="Author Voice: an open book with manuscript lines">']


def rect(box, radius, color):
    draw.rounded_rectangle(tuple(n * SCALE for n in box), radius=radius * SCALE, fill=color)
    x, y, right, bottom = box
    svg.append(f'<rect x="{x}" y="{y}" width="{right-x}" height="{bottom-y}" rx="{radius}" fill="{color}"/>')


rect((0, 0, 512, 512), 112, "#173D38")
rect((92, 106, 244, 394), 24, "#F6F0E2")
rect((268, 106, 420, 394), 24, "#F6F0E2")
for y, right in ((168, 207), (212, 197), (256, 212), (300, 190)):
    rect((127, y, right, y + 13), 6, "#173D38")
for y, right in ((168, 371), (212, 385), (256, 366)):
    rect((303, y, right, y + 13), 6, "#173D38")
rect((303, 309, 369, 327), 9, "#BA673B")
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "logo.svg").write_text("\n".join(svg + ["</svg>"]) + "\n", encoding="utf-8")
image.resize((SIZE, SIZE), Image.Resampling.LANCZOS).save(OUT / "logo.png", optimize=True)
print("Updated plugin assets/logo.svg and assets/logo.png.")
