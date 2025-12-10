"""Media elements examples for NitroUI.

This module demonstrates HTML media elements:
- Images
- Video and audio
- Picture element for responsive images
- Figure and figcaption
- Canvas
- SVG and embedded content
- Image maps
"""

from nitro_ui import *


def basic_image():
    """Basic image usage."""
    print("=== Basic Image ===\n")

    # Simple image
    img = Image(src="/images/photo.jpg", alt="A beautiful landscape")
    print("Simple image:")
    print(img.render())
    print()

    # Image with dimensions
    img_sized = Image(
        src="/images/photo.jpg", alt="A beautiful landscape", width="800", height="600"
    )
    print("Image with dimensions:")
    print(img_sized.render())
    print()

    # Image with loading and decoding hints
    img_optimized = Image(
        src="/images/large-photo.jpg",
        alt="Large image",
        loading="lazy",
        decoding="async",
        width="1200",
        height="800",
    )
    print("Optimized image (lazy loading):")
    print(img_optimized.render())


def responsive_images():
    """Responsive images with srcset and sizes."""
    print("\n=== Responsive Images ===\n")

    # Image with srcset
    img = Image(
        src="/images/hero.jpg",
        srcset="/images/hero-480.jpg 480w, /images/hero-800.jpg 800w, /images/hero-1200.jpg 1200w",
        sizes="(max-width: 600px) 480px, (max-width: 1000px) 800px, 1200px",
        alt="Hero image",
    )
    print("Image with srcset:")
    print(img.render())


def picture_element():
    """Picture element for art direction."""
    print("\n=== Picture Element ===\n")

    picture = Picture(
        # WebP for modern browsers
        Source(srcset="/images/hero.webp", type="image/webp"),
        # Different crops for different screen sizes
        Source(srcset="/images/hero-mobile.jpg", media="(max-width: 600px)"),
        Source(srcset="/images/hero-tablet.jpg", media="(max-width: 1000px)"),
        # Fallback image
        Image(src="/images/hero-desktop.jpg", alt="Hero image"),
    )

    print("Picture with multiple sources:")
    print(picture.render(pretty=True))


def figure_element():
    """Figure with figcaption."""
    print("\n=== Figure Element ===\n")

    figure = Figure(
        Image(src="/images/chart.png", alt="Sales chart showing Q4 growth"),
        Figcaption(
            "Figure 1: Q4 2024 Sales Growth. ", Em("Source: Internal Analytics")
        ),
    )

    print("Figure with caption:")
    print(figure.render(pretty=True))

    # Multiple images in a figure
    gallery_figure = Figure(
        Div(
            Image(src="/gallery/1.jpg", alt="Photo 1"),
            Image(src="/gallery/2.jpg", alt="Photo 2"),
            Image(src="/gallery/3.jpg", alt="Photo 3"),
            class_name="gallery-images",
        ),
        Figcaption("Gallery: Summer Vacation 2024"),
        class_name="image-gallery",
    )

    print("\nFigure with multiple images:")
    print(gallery_figure.render(pretty=True))


def video_element():
    """Video element examples."""
    print("\n=== Video Element ===\n")

    # Basic video
    video = Video(
        Source(src="/videos/intro.mp4", type="video/mp4"),
        Source(src="/videos/intro.webm", type="video/webm"),
        "Your browser does not support the video tag.",
        controls="true",
        width="640",
        height="360",
    )
    print("Basic video:")
    print(video.render(pretty=True))

    # Video with all options
    video_full = Video(
        Source(src="/videos/demo.mp4", type="video/mp4"),
        Track(
            src="/videos/demo-captions.vtt",
            kind="captions",
            srclang="en",
            label="English",
        ),
        Track(
            src="/videos/demo-captions-es.vtt",
            kind="captions",
            srclang="es",
            label="Spanish",
        ),
        controls="true",
        autoplay="false",
        muted="false",
        loop="false",
        preload="metadata",
        poster="/videos/demo-poster.jpg",
        width="800",
        height="450",
    )
    print("\nVideo with captions and poster:")
    print(video_full.render(pretty=True))

    # Autoplay muted video (for background)
    video_bg = Video(
        Source(src="/videos/background.mp4", type="video/mp4"),
        autoplay="true",
        muted="true",
        loop="true",
        playsinline="true",
        class_name="background-video",
    ).add_styles(
        {
            "position": "absolute",
            "width": "100%",
            "height": "100%",
            "object-fit": "cover",
        }
    )
    print("\nBackground video (autoplay, muted, loop):")
    print(video_bg.render())


def audio_element():
    """Audio element examples."""
    print("\n=== Audio Element ===\n")

    # Basic audio
    audio = Audio(
        Source(src="/audio/podcast.mp3", type="audio/mpeg"),
        Source(src="/audio/podcast.ogg", type="audio/ogg"),
        "Your browser does not support the audio tag.",
        controls="true",
    )
    print("Basic audio:")
    print(audio.render(pretty=True))

    # Audio with preload
    audio_preload = Audio(
        Source(src="/audio/notification.mp3", type="audio/mpeg"),
        preload="auto",
        controls="true",
    )
    print("\nAudio with preload:")
    print(audio_preload.render())


def canvas_element():
    """Canvas element for graphics."""
    print("\n=== Canvas Element ===\n")

    canvas = Canvas(
        "Your browser does not support the canvas element.",
        id="myCanvas",
        width="400",
        height="300",
    )
    print("Canvas element:")
    print(canvas.render())

    # Canvas in a styled container
    canvas_container = Div(
        Canvas(id="chartCanvas", width="600", height="400"),
        Paragraph("Chart rendered with JavaScript"),
        class_name="canvas-container",
    ).add_styles(
        {"border": "1px solid #ddd", "padding": "10px", "background": "#fafafa"}
    )
    print("\nCanvas in container:")
    print(canvas_container.render(pretty=True))


def embed_and_object():
    """Embed and object elements."""
    print("\n=== Embed and Object Elements ===\n")

    # Embed element
    embed = Embed(
        src="/files/document.pdf", type="application/pdf", width="800", height="600"
    )
    print("Embed PDF:")
    print(embed.render())

    # Object element with fallback
    obj = Object(
        Param(name="movie", value="/flash/animation.swf"),
        Param(name="quality", value="high"),
        Paragraph(
            "Flash content not supported. ",
            Link("Download instead", href="/files/animation.swf"),
        ),
        data="/flash/animation.swf",
        type="application/x-shockwave-flash",
        width="400",
        height="300",
    )
    print("\nObject with params and fallback:")
    print(obj.render(pretty=True))


def iframe_element():
    """IFrame for embedded content."""
    print("\n=== IFrame Element ===\n")

    # Basic iframe
    iframe = IFrame(
        src="https://example.com", width="800", height="600", title="Embedded website"
    )
    print("Basic iframe:")
    print(iframe.render())

    # Secure iframe (embedded video)
    iframe_video = IFrame(
        src="https://www.youtube.com/embed/dQw4w9WgXcQ",
        width="560",
        height="315",
        title="YouTube video player",
        frameborder="0",
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
        allowfullscreen="true",
    )
    print("\nYouTube embed iframe:")
    print(iframe_video.render())

    # Sandboxed iframe
    iframe_sandbox = IFrame(
        src="/embed/widget.html",
        sandbox="allow-scripts allow-same-origin",
        width="300",
        height="200",
        title="Sandboxed widget",
    )
    print("\nSandboxed iframe:")
    print(iframe_sandbox.render())


def image_map():
    """Image map with clickable areas."""
    print("\n=== Image Map ===\n")

    content = Div(
        Image(
            src="/images/workspace.jpg",
            alt="Office workspace",
            usemap="#workspace-map",
            width="800",
            height="600",
        ),
        Map(
            Area(
                shape="rect",
                coords="0,0,200,150",
                href="/products/monitor",
                alt="Monitor",
                title="Click to see monitors",
            ),
            Area(
                shape="rect",
                coords="250,200,450,400",
                href="/products/keyboard",
                alt="Keyboard",
                title="Click to see keyboards",
            ),
            Area(
                shape="circle",
                coords="600,300,50",
                href="/products/mouse",
                alt="Mouse",
                title="Click to see mice",
            ),
            Area(
                shape="poly",
                coords="500,100,550,50,600,100,550,150",
                href="/products/lamp",
                alt="Lamp",
                title="Click to see lamps",
            ),
            name="workspace-map",
        ),
    )

    print("Image with clickable map:")
    print(content.render(pretty=True))


def media_gallery():
    """Building a media gallery."""
    print("\n=== Media Gallery ===\n")

    images = [
        {
            "src": "/gallery/photo1.jpg",
            "alt": "Mountain landscape",
            "caption": "Swiss Alps",
        },
        {
            "src": "/gallery/photo2.jpg",
            "alt": "Beach sunset",
            "caption": "Malibu Beach",
        },
        {
            "src": "/gallery/photo3.jpg",
            "alt": "City skyline",
            "caption": "New York City",
        },
        {"src": "/gallery/photo4.jpg", "alt": "Forest path", "caption": "Black Forest"},
    ]

    gallery = Div(
        H2("Photo Gallery"),
        Div(
            *[
                Figure(
                    Image(src=img["src"], alt=img["alt"], loading="lazy").add_styles(
                        {"width": "100%", "height": "200px", "object-fit": "cover"}
                    ),
                    Figcaption(img["caption"]),
                    class_name="gallery-item",
                ).add_styles({"margin": "0", "break-inside": "avoid"})
                for img in images
            ],
            class_name="gallery-grid",
        ).add_styles(
            {
                "display": "grid",
                "grid-template-columns": "repeat(auto-fill, minmax(250px, 1fr))",
                "gap": "16px",
            }
        ),
        class_name="gallery-container",
    )

    print(gallery.render(pretty=True))


def video_player():
    """Custom video player structure."""
    print("\n=== Custom Video Player Structure ===\n")

    player = Div(
        # Video element
        Video(
            Source(src="/videos/movie.mp4", type="video/mp4"),
            Source(src="/videos/movie.webm", type="video/webm"),
            Track(
                src="/videos/movie-captions.vtt",
                kind="captions",
                srclang="en",
                label="English",
                default="true",
            ),
            id="video-player",
            preload="metadata",
            poster="/videos/movie-poster.jpg",
        ).add_styles({"width": "100%", "display": "block"}),
        # Custom controls
        Div(
            Button("Play", type="button", id="play-btn", aria_label="Play video"),
            Button("Pause", type="button", id="pause-btn", aria_label="Pause video"),
            # Progress bar
            Div(
                Div(id="progress-bar", class_name="progress-bar"),
                class_name="progress-container",
            ).add_styles(
                {
                    "flex": "1",
                    "height": "8px",
                    "background": "#ddd",
                    "border-radius": "4px",
                    "margin": "0 10px",
                }
            ),
            # Time display
            Span("0:00 / 0:00", id="time-display"),
            # Volume
            Input(type="range", id="volume", min="0", max="1", step="0.1", value="1"),
            # Fullscreen
            Button("Fullscreen", type="button", id="fullscreen-btn"),
            class_name="video-controls",
        ).add_styles(
            {
                "display": "flex",
                "align-items": "center",
                "padding": "10px",
                "background": "#333",
                "color": "white",
            }
        ),
        class_name="video-player-container",
    ).add_styles({"max-width": "800px", "background": "#000"})

    print(player.render(pretty=True))


def audio_playlist():
    """Audio playlist structure."""
    print("\n=== Audio Playlist ===\n")

    tracks = [
        {
            "title": "Track 1 - Morning Jazz",
            "artist": "Jazz Trio",
            "src": "/audio/track1.mp3",
            "duration": "3:42",
        },
        {
            "title": "Track 2 - Evening Blues",
            "artist": "Blues Band",
            "src": "/audio/track2.mp3",
            "duration": "4:15",
        },
        {
            "title": "Track 3 - Night Lounge",
            "artist": "Lounge Quartet",
            "src": "/audio/track3.mp3",
            "duration": "5:01",
        },
    ]

    playlist = Div(
        H2("Playlist"),
        # Audio player
        Audio(id="audio-player", controls="true", preload="none").add_style(
            "width", "100%"
        ),
        # Track list
        UnorderedList(
            *[
                ListItem(
                    Div(
                        Strong(track["title"]),
                        Span(f" - {track['artist']}"),
                        Span(track["duration"], class_name="duration"),
                        class_name="track-info",
                    ),
                    data_src=track["src"],
                    class_name="track-item",
                ).add_styles(
                    {
                        "padding": "10px",
                        "cursor": "pointer",
                        "border-bottom": "1px solid #eee",
                    }
                )
                for track in tracks
            ],
            class_name="track-list",
        ).add_styles({"list-style": "none", "padding": "0", "margin": "0"}),
        class_name="audio-playlist",
    ).add_styles(
        {
            "max-width": "400px",
            "border": "1px solid #ddd",
            "border-radius": "8px",
            "overflow": "hidden",
        }
    )

    print(playlist.render(pretty=True))


def avatar_images():
    """Avatar and thumbnail images."""
    print("\n=== Avatar Images ===\n")

    def avatar(src, name, size=48):
        """Create an avatar image."""
        return Image(
            src=src, alt=f"{name}'s avatar", width=str(size), height=str(size)
        ).add_styles({"border-radius": "50%", "object-fit": "cover"})

    users = Div(
        H3("Team Members"),
        Div(
            *[
                Div(
                    avatar(f"/avatars/{name.lower()}.jpg", name, 64),
                    Paragraph(name),
                    class_name="user-avatar",
                ).add_styles({"text-align": "center", "padding": "10px"})
                for name in ["Alice", "Bob", "Charlie", "Diana"]
            ],
            class_name="avatar-grid",
        ).add_styles({"display": "flex", "gap": "20px"}),
    )

    print(users.render(pretty=True))


if __name__ == "__main__":
    basic_image()
    responsive_images()
    picture_element()
    figure_element()
    video_element()
    audio_element()
    canvas_element()
    embed_and_object()
    iframe_element()
    image_map()
    media_gallery()
    video_player()
    audio_playlist()
    avatar_images()
