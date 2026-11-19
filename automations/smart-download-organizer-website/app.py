
from pathlib import Path

import streamlit as st


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

LOGO_PATH = ASSETS_DIR / "logo.png"
ICON_PATH = ASSETS_DIR / "app_icon.png"


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

PAGE_ICON = str(ICON_PATH) if ICON_PATH.exists() else "📁"

st.set_page_config(
    page_title="Smart Download Organizer",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

APP_NAME = "Smart Download Organizer"
VERSION = "1.0.1"

GITHUB_REPO = (
    "https://github.com/silverbullet-ai/"
    "intelligent-systems"
)

PROJECT_URL = (
    f"{GITHUB_REPO}/tree/main/automations/"
    "smart-download-organizer"
)

RELEASE_URL = f"{GITHUB_REPO}/releases/latest"

INSTALLER_URL = (
    f"{GITHUB_REPO}/releases/latest/download/"
    "SmartDownloadOrganizer-Setup.exe"
)

PORTABLE_URL = (
    f"{GITHUB_REPO}/releases/latest/download/"
    "SmartDownloadOrganizer-Portable.zip"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --background: #08111f;
        --surface: #101d30;
        --surface-light: #162740;
        --primary: #3b82f6;
        --primary-hover: #60a5fa;
        --text: #f1f5f9;
        --muted: #9aabc1;
        --border: #263a55;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .top-label {
        color: #60a5fa;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .hero-title {
        color: #f8fafc;
        font-size: clamp(2.5rem, 6vw, 4.4rem);
        font-weight: 800;
        line-height: 1.12;
        letter-spacing: -2px;
        margin-bottom: 1.2rem;
    }

    .hero-title span {
        color: #60a5fa;
    }

    .hero-description {
        color: #a9bad0;
        font-size: 1.08rem;
        line-height: 1.8;
        max-width: 680px;
        margin-bottom: 1.5rem;
    }

    .section-title {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 750;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    .section-description {
        color: var(--muted);
        font-size: 1rem;
        margin-bottom: 1.7rem;
    }

    .feature-card {
        background: linear-gradient(
            145deg,
            #13243a,
            #0e1b2d
        );
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.4rem;
        min-height: 175px;
        margin-bottom: 1rem;
    }

    .feature-icon {
        font-size: 1.8rem;
        margin-bottom: 0.7rem;
    }

    .feature-title {
        color: #f1f5f9;
        font-size: 1.08rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .feature-description {
        color: #9aabc1;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .download-card {
        background: linear-gradient(
            145deg,
            #142945,
            #0e1b2d
        );
        border: 1px solid #31527b;
        border-radius: 18px;
        padding: 1.6rem;
        height: 300px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    }

    .download-card h3 {
        color: #f8fafc;
        font-size: 1.3rem;
    }

    .download-card p {
        color: #a9bad0;
        line-height: 1.7;
    }

    .version-pill {
        display: inline-block;
        background: #173b68;
        border: 1px solid #2863a5;
        color: #93c5fd;
        border-radius: 30px;
        padding: 0.35rem 0.8rem;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .info-strip {
        background: #101d30;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
    }

    .info-value {
        color: #60a5fa;
        font-size: 1.5rem;
        font-weight: 800;
    }

    .info-label {
        color: #9aabc1;
        font-size: 0.85rem;
    }

    .footer {
        border-top: 1px solid var(--border);
        padding-top: 1.5rem;
        margin-top: 3rem;
        color: #8193aa;
        font-size: 0.85rem;
        text-align: center;
        line-height: 1.8;
    }

    div.stLinkButton > a {
        background: #2563eb;
        color: white !important;
        border: 1px solid #3b82f6;
        border-radius: 9px;
        font-weight: 650;
        transition: 0.2s ease;
    }

    div.stLinkButton > a:hover {
        background: #1d4ed8;
        border-color: #60a5fa;
        color: white !important;
    }

    div.stLinkButton > a:focus {
        color: white !important;
    }

    [data-testid="stMarkdownContainer"] a {
        color: #60a5fa;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-title {
            letter-spacing: -1px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# NAVIGATION / BRANDING
# --------------------------------------------------

nav_left, nav_right = st.columns([3, 1])

with nav_left:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=260)
    else:
        st.markdown(
            "### 📁 SMART DOWNLOAD ORGANIZER"
        )

with nav_right:
    st.markdown(
        f"""
        <div style="text-align:right; padding-top:12px;">
            <span class="version-pill">VERSION {VERSION}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

hero_left, hero_right = st.columns(
    [1.35, 1],
    gap="large",
    vertical_alignment="center",
)

with hero_left:
    st.markdown(
        '<div class="top-label">A smarter way to organize</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-title">
            Your files.<br>
            Organized <span>automatically.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-description">
            Take control of your digital workspace.
            Smart Download Organizer automatically
            categorizes your files, simplifies folder
            management, and helps keep everything organized.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "⬇  Download for Windows",
        INSTALLER_URL,
        type="primary",
        use_container_width=True,
    )

    st.link_button(
        "Explore the GitHub Project",
        PROJECT_URL,
        use_container_width=True,
    )

with hero_right:
    if LOGO_PATH.exists():
        st.image(
            str(LOGO_PATH),
            use_container_width=True,
        )
    else:
        st.markdown(
            """
            <div style="
                background:linear-gradient(145deg,#142945,#0b1728);
                border:1px solid #263a55;
                border-radius:22px;
                padding:3rem 1rem;
                text-align:center;
                font-size:6rem;
            ">
                📁
                <div style="
                    color:#60a5fa;
                    font-size:1rem;
                    font-weight:700;
                    margin-top:1rem;
                ">
                    SMART DOWNLOAD ORGANIZER
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# PRODUCT HIGHLIGHTS
# --------------------------------------------------

st.write("")
st.write("")

st.markdown(
    '<div class="section-title">Built to make file management easier.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Everything you need to organize your files with confidence.'
    '</div>',
    unsafe_allow_html=True,
)

highlights = st.columns(3)

highlight_data = [
    ("45", "Automated tests passing"),
    ("7+", "Built-in file categories"),
    (VERSION, "Latest release"),
]

for column, (value, label) in zip(highlights, highlight_data):
    with column:
        st.markdown(
            f"""
            <div class="info-strip">
                <div class="info-value">{value}</div>
                <div class="info-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

st.write("")
st.write("")

st.markdown(
    '<div class="section-title">Everything in one place.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Explore the features that make Smart Download Organizer useful.'
    '</div>',
    unsafe_allow_html=True,
)

features = [
    (
        "🔎",
        "File Scanning",
        "Scan selected directories and discover files with "
        "recursive and non-recursive scanning options.",
    ),
    (
        "🗂️",
        "Automatic Categorization",
        "Categorize files based on their extensions using "
        "configurable JSON rules.",
    ),
    (
        "👁️",
        "Organization Preview",
        "Review the proposed file organization plan before "
        "making any changes.",
    ),
    (
        "📦",
        "Safe File Movement",
        "Move files into category folders while protecting "
        "existing files and handling duplicates.",
    ),
    (
        "↩️",
        "Undo Operations",
        "Restore files to their original locations with "
        "safeguards against overwriting.",
    ),
    (
        "📜",
        "Activity History",
        "Keep track of previous file movements and access "
        "persistent organization history.",
    ),
    (
        "⚙️",
        "Configuration Management",
        "Create custom categories, manage extensions, and "
        "change your default category.",
    ),
    (
        "🛡️",
        "Safety Checks",
        "Detect files changed or deleted after scanning "
        "before attempting to move them.",
    ),
]

feature_columns = st.columns(2)

for index, (icon, title, description) in enumerate(features):
    with feature_columns[index % 2]:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-description">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# DOWNLOAD CENTER
# --------------------------------------------------

st.write("")
st.write("")

st.markdown(
    '<div class="section-title">Get Smart Download Organizer.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Choose the version that works best for you.'
    '</div>',
    unsafe_allow_html=True,
)

download_left, download_right = st.columns(2, gap="large")

with download_left:
    st.markdown(
        """
        <div class="download-card">
            <div class="version-pill">RECOMMENDED</div>
            <h3>Windows Installer</h3>
            <p>
                The easiest way to install Smart Download Organizer.
                Includes installation and uninstallation support,
                Start Menu shortcut, and optional desktop shortcut.
            </p>
            <p><b>File:</b> SmartDownloadOrganizer-Setup.exe</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "⬇  Download Installer",
        INSTALLER_URL,
        type="primary",
        use_container_width=True,
    )

with download_right:
    st.markdown(
        """
        <div class="download-card">
            <div class="version-pill">PORTABLE</div>
            <h3>Portable Version</h3>
            <p>
                Prefer not to use an installer?
                Download the portable ZIP, extract its contents,
                and launch the application directly.
            </p>
            <p><b>File:</b> SmartDownloadOrganizer-Portable.zip</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "⬇  Download Portable ZIP",
        PORTABLE_URL,
        use_container_width=True,
    )

st.caption(
    "Both distributions are intended for Windows. "
    "Check the release page for the latest files and release notes."
)

st.link_button(
    "View Release Notes and All Downloads",
    RELEASE_URL,
)


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

st.write("")
st.write("")

st.markdown(
    '<div class="section-title">Built with Python. Designed for simplicity.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    Smart Download Organizer is a Python-based desktop
    application built with CustomTkinter.

    It combines file scanning, configurable categorization,
    safe file movement, activity history, and undo functionality
    in a single desktop application.
    """
)

tech_columns = st.columns(4)

technologies = [
    ("Python", "Core application"),
    ("CustomTkinter", "Desktop interface"),
    ("JSON", "Configuration"),
    ("unittest", "Testing"),
]

for column, (technology, purpose) in zip(
    tech_columns,
    technologies,
):
    with column:
        st.markdown(
            f"""
            <div class="feature-card" style="min-height:110px;">
                <div class="feature-title">{technology}</div>
                <div class="feature-description">{purpose}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# GITHUB SECTION
# --------------------------------------------------

st.write("")
st.write("")

st.markdown(
    '<div class="section-title">Explore the project.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    Interested in how it works? Explore the source code,
    review the documentation, or contribute to the project.
    """
)

github_left, github_right = st.columns(2)

with github_left:
    st.link_button(
        "View Source Code on GitHub",
        PROJECT_URL,
        use_container_width=True,
    )

with github_right:
    st.link_button(
        "View Latest Release",
        RELEASE_URL,
        use_container_width=True,
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <b style="color:#dbeafe;">
            SMART DOWNLOAD ORGANIZER
        </b>
        <br>
        Organize. Simplify. Stay productive.
        <br><br>
        Built by <b>Aahish Aayan (Silver Bullet)</b>
        <br>
        © 2026 · Open-source project
        <br><br>
        Built with Python, curiosity, and a little automation magic.
    </div>
    """,
    unsafe_allow_html=True,
)
