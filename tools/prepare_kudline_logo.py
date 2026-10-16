"""Prepare web assets from the approved KUDLINE JPG without redrawing it."""
from pathlib import Path
from shutil import copy2
from PIL import Image, ImageChops

SOURCE = Path(r"C:\Users\Professional\Downloads\IMG_20261016_173640.jpg")
OUT = Path(r"C:\KUDLINE\frontend\public\brand")
OUT.mkdir(parents=True, exist_ok=True)


def alpha_from_white(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    luminance = rgb.convert("L")
    # Keep the approved geometry intact; only remove the near-white JPEG field.
    alpha = luminance.point(lambda value: 0 if value >= 250 else 255 if value <= 224 else round((250 - value) * 255 / 26))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(alpha)
    return rgba


def crop_content(image: Image.Image, padding: int = 8) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        raise RuntimeError("No logo content found")
    left, top, right, bottom = bbox
    return image.crop((max(0, left-padding), max(0, top-padding), min(image.width, right+padding), min(image.height, bottom+padding)))


def recolor(image: Image.Image, color: tuple[int, int, int]) -> Image.Image:
    result = Image.new("RGBA", image.size, (*color, 0))
    result.putalpha(image.getchannel("A"))
    return result


def save_pair(image: Image.Image, stem: str) -> None:
    image.save(OUT / f"{stem}.png", optimize=True)
    image.save(OUT / f"{stem}.webp", "WEBP", lossless=True, method=6)


source = Image.open(SOURCE).convert("RGB")
copy2(SOURCE, OUT / "kudline-logo-source.jpg")
transparent = alpha_from_white(source)

# The source is a vertical lock-up: approved mark above, approved wordmark below.
mark_area = transparent.crop((0, 0, source.width, round(source.height * 0.68)))
word_area = transparent.crop((0, round(source.height * 0.70), source.width, source.height))
mark = crop_content(mark_area, 10)
word = crop_content(word_area, 10)

dark = (43, 43, 49)
light = (242, 241, 235)
mark_dark, mark_light = recolor(mark, dark), recolor(mark, light)
word_dark, word_light = recolor(word, dark), recolor(word, light)
save_pair(mark_dark, "kudline-mark-dark")
save_pair(mark_light, "kudline-mark-light")


def horizontal(mark_image: Image.Image, word_image: Image.Image) -> Image.Image:
    mark_h = 380
    resized_mark = mark_image.resize((round(mark_image.width * mark_h / mark_image.height), mark_h), Image.Resampling.LANCZOS)
    word_h = 118
    resized_word = word_image.resize((round(word_image.width * word_h / word_image.height), word_h), Image.Resampling.LANCZOS)
    gap, padding = 58, 18
    canvas = Image.new("RGBA", (resized_mark.width + gap + resized_word.width + 2*padding, mark_h + 2*padding), (0, 0, 0, 0))
    canvas.alpha_composite(resized_mark, (padding, padding))
    canvas.alpha_composite(resized_word, (padding + resized_mark.width + gap, padding + (mark_h-word_h)//2))
    return canvas


horizontal_dark = horizontal(mark_dark, word_dark)
horizontal_light = horizontal(mark_light, word_light)
save_pair(horizontal_dark, "kudline-logo-horizontal-dark")
save_pair(horizontal_light, "kudline-logo-horizontal-light")
horizontal_dark.save(OUT / "kudline-logo-dark.png", optimize=True)
horizontal_light.save(OUT / "kudline-logo-light.png", optimize=True)

# Favicon uses the untouched mark silhouette, reduced with high-quality resampling.
favicon_master = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
fit = mark_dark.copy()
fit.thumbnail((224, 224), Image.Resampling.LANCZOS)
favicon_master.alpha_composite(fit, ((256-fit.width)//2, (256-fit.height)//2))
favicon_master.resize((32, 32), Image.Resampling.LANCZOS).save(OUT / "favicon-32.png", optimize=True)
favicon_master.resize((192, 192), Image.Resampling.LANCZOS).save(OUT / "favicon-192.png", optimize=True)
favicon_master.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

print(f"Prepared brand assets in {OUT}")
