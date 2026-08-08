# Title photography

Photographs for the **Photo Deck Title** layout. Applied as a slide background
by `skills/digi-pptx/scripts/set_title_photo.py`.

## The image files are NOT in this repo — pending a provenance answer

`.gitignore` excludes every image here. This is a **hold, not a known
restriction**, and the distinction matters:

**What was verified.** The four files carry no rights metadata whatsoever —
EXIF-only APP1 segments (114–138 bytes), an empty 54-byte Photoshop IPTC stub,
no XMP packet, no copyright/creator/credit/licensor string. All four were
processed through Photoshop and stripped, which is routine for template
artwork. `offshore-platform.jpeg` has a Nikon ICC profile, so it is
camera-original rather than a rendered composite.

**What that proves: nothing about licensing.** A stock download and an in-house
Digi shoot are indistinguishable after Photoshop stripping. We do not know
whether Digi owns these outright or licensed them from an agency.

**Why we hold anyway.** This repo is public and git history is effectively
permanent — deleting a file later does not un-publish it. Publishing an asset
of unknown provenance is the one move that cannot be walked back, so waiting
costs nothing and guessing could cost a lot.

**How to resolve it:** ask Digi marketing (the brand/template owner) where the
2024 template's title photographs came from. If Digi owns them, commit them and
delete this section. If they are licensed, the license terms decide whether an
internal repo is in scope.

Everything else about the feature is in the repo. Only the pixels are missing,
and any image works in their place.

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
