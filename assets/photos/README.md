# Title photography

Photographs for the **Photo Deck Title** layout. Applied as a slide background
by `skills/digi-pptx/scripts/set_title_photo.py`.

## Rights

**Digi purchased these outright and owns them, with no restriction on use**
— confirmed by Taylor Salentine, who owns Digi's brand and template library,
2026-08-07. They ship in this repo and need no attribution, no license file,
and no special handling.

Recorded here rather than left to memory because the question is expensive to
re-ask and the files themselves cannot answer it: all four were processed
through Photoshop and stripped of metadata, so they carry no rights, creator,
or credit fields at all. Anyone inspecting the bytes will find nothing and may
reasonably wonder — this section is the answer.

They originate from the earlier-generation Digi deck template
(`Digi template.pptx`), which embedded them in its title layouts.

## The four photographs

Listed with `python3 skills/digi-pptx/scripts/set_title_photo.py --list`.

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
(`gen_graphic.py --style photo`) when no real photograph fits the subject.

Formats: `.jpg`, `.jpeg`, `.png`.
