# Aurora

A dark [Omarchy](https://omarchy.org) theme drawn from a photo of the northern lights over a pine forest: a violet night sky, green and teal aurora, and pale starlight text.

![Aurora theme on a desktop with a terminal, btop and LazyVim](auroratheme.png)

![Aurora wallpaper: northern lights over a pine forest](backgrounds/1-aurora.jpg)

![Omarchy logo in the accent green on the night background](backgrounds/omarchy.png)

![Omarchy logo in a violet-to-green palette gradient](backgrounds/omarchy-spectrum.png)

![Palette](palette.png)

## Install

```bash
omarchy theme install https://github.com/thevideinfra/omarchy-aurora-theme
```

Or open **Install > Style > Theme** in the Omarchy menu and paste the URL.

## Palette

| Role | Color |
|------|-------|
| Background | `#140F1F` |
| Foreground | `#DFEDE5` |
| Accent | `#59C98D` |
| Selection | `#2A4A3E` |

Four wallpapers ship in `backgrounds/`: the aurora photo, a slowly animated version, the Omarchy logo in the accent green, and the logo in a stepped gradient that runs through the palette from magenta to bright green. Cycle between them with `omarchy theme bg next`.

## Animated aurora

On Omarchy with video wallpaper support, select `2-aurora-animated.mp4` with
`omarchy theme bg next`, or select it directly after installing:

```bash
omarchy theme bg set ~/.config/omarchy/themes/aurora/backgrounds/2-aurora-animated.mp4
```

The silent, 40-second loop gently bends the aurora curtains while keeping the
forest and stars still. It is encoded as H.264 at 1920 × 1282 and 24 fps, keeping
the photograph's composition. Playback and looping use Omarchy's built-in video
wallpaper support; no theme hooks or background scripts are needed. The original
`1-aurora.jpg` remains available for a still wallpaper and older installations.

To regenerate the video, install FFmpeg with the libx264 encoder, then run from
the repository root:

```bash
python -m venv /tmp/aurora-render-venv
/tmp/aurora-render-venv/bin/pip install numpy opencv-python-headless
/tmp/aurora-render-venv/bin/python tools/animate-aurora.py
```

Window borders use a green-to-violet gradient (`#59C98D` to `#B06BC4`). Terminal, editor and app colors are generated from `colors.toml`, so every app Omarchy themes picks up the palette.

## Credits

Wallpaper: [Polar lights over dark trees](https://unsplash.com/photos/silhouette-of-trees-near-aurora-borealis-at-night-62V7ntlKgL8) by [Vincent Guth](https://unsplash.com/@vingtcent), used under the [Unsplash License](https://unsplash.com/license). The animated wallpaper is a derivative of the same photograph and remains under the Unsplash License.

## License

The theme files are released under the MIT License. See [LICENSE](LICENSE). The wallpaper in `backgrounds/` is not covered by that license; it stays under the Unsplash License.
