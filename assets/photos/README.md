# Title photography

Photographs for the **Photo Deck Title** layout. Applied as a slide background
by `skills/digi-pptx/scripts/set_title_photo.py`.

## The image files are deliberately NOT in this repo

`.gitignore` excludes every image in this directory. This repo is public, and
these are **third-party licensed stock photographs**. A stock license lets Digi
use an image in Digi materials; it does not let us publish the image file where
anyone can download it, which is exactly what committing it here would do. That
restriction is the photographer's and the agency's, not Digi's — so it is not
Digi's to waive.

Everything else about the feature is in the repo. Only the pixels are missing.

## Populating the library

The four photographs come from the earlier-generation Digi deck template
(`Digi template.pptx`), which carried them embedded in its title layouts. To
recover them locally:

```bash
mkdir -p /tmp/digi-src && cd /tmp/digi-src
unzip -q "$HOME/Downloads/Digi template.pptx"
cp ppt/media/image2.jpeg  "$OLDPWD/city-skyline-network.jpeg"
cp ppt/media/image10.jpeg "$OLDPWD/offshore-platform.jpeg"
cp ppt/media/image23.jpeg "$OLDPWD/night-city-connections.jpeg"
cp ppt/media/image26.jpeg "$OLDPWD/transit-traveler.jpeg"
```

Verify with `python3 skills/digi-pptx/scripts/set_title_photo.py --list`.

| Name | Subject | Reads as |
| --- | --- | --- |
| `city-skyline-network` | Daytime skyline with network-graphic overlay | Connectivity, infrastructure, scale |
| `night-city-connections` | Night aerial, interchange, light arcs | Traffic, data movement, always-on |
| `offshore-platform` | Offshore rig, open sea | Remote/harsh-site deployment, industrial |
| `transit-traveler` | Traveler with a phone in a transit hall | End users, mobility, retail/transit verticals |

## Using a custom photograph

Nothing about the layout is tied to the library — the four are a convenience,
not a constraint:

```bash
python3 skills/digi-pptx/scripts/set_title_photo.py \
    --unpacked unpacked/ --slide 1 --image work/customer-site.jpg
```

Pick something that reads at a glance and is legible under the scrim. The
translucent dark diagonal covers the left of the slide where the title sits, so
a photo whose subject is on the **right** works best — a busy or high-contrast
left side fights the title text. Generated photography works too
(`gen_graphic.py --style photo`), and carries no licensing question at all
since we produce it.

Formats: `.jpg`, `.jpeg`, `.png`.
