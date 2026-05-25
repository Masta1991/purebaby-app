import streamlit as st
import datetime
import base64
import os
import json
import urllib.parse
from PIL import Image

# ══════════════════════════════════════════════════════════════════════════════
# 1. INITIALIZATION & UTILITIES
# ══════════════════════════════════════════════════════════════════════════════
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.makedirs(os.path.join(BASE_DIR, "zdjecia"), exist_ok=True)

SVG_HOME = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>"""
SVG_SETTINGS = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>"""
SVG_ADD_DATA = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect><line x1="12" y1="11" x2="12" y2="17"></line><line x1="9" y1="14" x2="15" y2="14"></line></svg>"""
SVG_BABY = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6z"></path><path d="M12 8c-3 0-5.5 1.5-7 4l2 1c1.5-2 3-3 5-3s3.5 1 5 3l2-1c-1.5-2.5-4-4-7-4z"></path><path d="M12 12c-4 0-7 2-7 5v2h14v-2c0-3-3-5-7-5z"></path></svg>"""

# ══════════════════════════════════════════════════════════════════════════════
# 2. PWA SETUP & FAVICON (cached — runs only once per session)
# ══════════════════════════════════════════════════════════════════════════════
ICON_DIR = os.path.join(BASE_DIR, "App Icon")
if not os.path.exists(ICON_DIR):
    os.makedirs(ICON_DIR, exist_ok=True)

icon_src = os.path.join(ICON_DIR, "szkielet.png")
icon_512_path = os.path.join(ICON_DIR, "icon_512.png")
icon_fav_path = os.path.join(BASE_DIR, "zdjecia", "icon.png")
logo_pure_path = os.path.join(BASE_DIR, "zdjecia", "logo_transparent_large.png")

@st.cache_data
def _process_icons():
    if not os.path.exists(icon_src):
        try:
            from PIL import ImageDraw, ImageFont
            img = Image.new('RGBA', (192, 192), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse([8, 8, 184, 184], outline='#006089', width=6)
            try:
                font = ImageFont.truetype("arial.ttf", 75)
            except IOError:
                font = ImageFont.load_default()
            try:
                left, top, right, bottom = draw.textbbox((0, 0), "MS", font=font)
                w, h = right - left, bottom - top
            except AttributeError:
                w, h = draw.textsize("MS", font=font)
            draw.text(((192 - w) // 2, (192 - h) // 2 - 5), "MS", fill='#006089', font=font)
            img.save(icon_src, 'PNG')
        except Exception:
            pass
    try:
        img_pil = Image.open(icon_src)
        if img_pil.size != (192, 192):
            img_pil = img_pil.resize((192, 192), Image.LANCZOS)
            img_pil.save(icon_src, 'PNG')
        img_512 = img_pil.resize((512, 512), Image.LANCZOS)
        img_512.save(icon_512_path, 'PNG')
        img_pil.save(icon_fav_path, 'PNG')
    except Exception:
        img = Image.new('RGBA', (192, 192), (0, 0, 0, 0))
        img.save(icon_fav_path, 'PNG')
        img.resize((512, 512), Image.LANCZOS).save(icon_512_path, 'PNG')
        img.save(icon_src, 'PNG')
    with open(icon_src, "rb") as f:
        b192 = f.read()
    with open(icon_512_path, "rb") as f:
        b512 = f.read()
    return b192, b512, base64.b64encode(b192).decode(), base64.b64encode(b512).decode()

icon_bytes_192, icon_bytes_512, ICON_B64, ICON_B64_512 = _process_icons()

@st.cache_data
def _load_pure_logo():
    try:
        if os.path.exists(logo_pure_path):
            with open(logo_pure_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception:
        pass
    return ICON_B64

LOGO_PURE_B64 = _load_pure_logo()

st.set_page_config(
    page_title="PureBaby",
    page_icon=os.path.join(BASE_DIR, "zdjecia", "icon.png"),
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(f"""
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="PureBaby">
    <meta name="theme-color" content="#006089">
    <link rel="apple-touch-icon" href="data:image/png;base64,{ICON_B64}">
    <link rel="apple-touch-icon-precomposed" href="data:image/png;base64,{ICON_B64}">
""", unsafe_allow_html=True)

PWA_MANIFEST = {
    "name": "PureBaby",
    "short_name": "PureBaby",
    "start_url": ".",
    "display": "standalone",
    "background_color": "#F2F7FA",
    "theme_color": "#006089",
    "icons": [
        {"src": f"data:image/png;base64,{ICON_B64}", "sizes": "192x192", "type": "image/png"},
        {"src": f"data:image/png;base64,{ICON_B64_512}", "sizes": "512x512", "type": "image/png"}
    ]
}
PWA_MANIFEST_JSON = json.dumps(PWA_MANIFEST)
PWA_SW_JS = """self.addEventListener('install', (e) => { e.waitUntil(self.skipWaiting()); });
self.addEventListener('activate', (e) => { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', (e) => {
  e.respondWith(fetch(e.request).catch(() => new Response('', { status: 408 })));
});"""

st.components.v1.html(f"""
<script>
(function() {{
    var pdoc = window.parent.document;
    if (!pdoc) return;
    var iconB64 = 'data:image/png;base64,{ICON_B64}';
    var metas = [
        ['apple-mobile-web-app-capable', 'yes'],
        ['apple-mobile-web-app-status-bar-style', 'default'],
        ['mobile-web-app-capable', 'yes'],
        ['apple-mobile-web-app-title', 'PureBaby'],
        ['theme-color', '#006089']
    ];
    metas.forEach(function(m) {{
        var el = pdoc.querySelector('meta[name="' + m[0] + '"]');
        if (!el) {{ el = pdoc.createElement('meta'); el.name = m[0]; pdoc.head.appendChild(el); }}
        el.content = m[1];
    }});
    var setLink = function(rel, href, extra) {{
        var el = pdoc.querySelector('link[rel="' + rel + '"]');
        if (!el) {{ el = pdoc.createElement('link'); el.rel = rel; pdoc.head.appendChild(el); }}
        el.href = href;
        if (extra) {{ for (var k in extra) el.setAttribute(k, extra[k]); }}
    }};
    setLink('apple-touch-icon', iconB64);
    setLink('apple-touch-icon-precomposed', iconB64);
    setLink('icon', iconB64, {{type:'image/png'}});
    setLink('shortcut icon', iconB64, {{type:'image/png'}});
    var manifestJson = '{PWA_MANIFEST_JSON}';
    var blob = new Blob([manifestJson], {{type: 'application/json'}});
    var manifestUrl = URL.createObjectURL(blob);
    setLink('manifest', manifestUrl);
    fetch('/sw.js').then(function(r) {{
        if (r.ok && 'serviceWorker' in navigator) {{ navigator.serviceWorker.register('/sw.js'); }}
    }}).catch(function(){{}});
}})();
</script>
""", height=0)

@st.cache_resource
def inject_pwa_routes():
    try:
        import gc
        from streamlit.web.server.server import Server
        from starlette.responses import Response
        servers = [obj for obj in gc.get_objects() if isinstance(obj, Server)]
        if not servers: return
        server = servers[0]
        starlette_server = getattr(server, "_starlette_server", None)
        if not starlette_server: return
        app = getattr(starlette_server, "app", None) or getattr(starlette_server, "_server", None)
        if not app: app = starlette_server
        if hasattr(app, "routes"):
            existing = [r.path for r in app.routes if hasattr(r, "path")]
            for route_path, content_type, content in [
                ("/sw.js", "application/javascript", PWA_SW_JS),
                ("/manifest.json", "application/json", json.dumps(PWA_MANIFEST)),
                ("/favicon.png", "image/png", icon_bytes_192),
                ("/favicon.ico", "image/x-icon", icon_bytes_192),
                ("/apple-touch-icon.png", "image/png", icon_bytes_192),
                ("/apple-touch-icon-precomposed.png", "image/png", icon_bytes_192),
            ]:
                if route_path not in existing:
                    @app.route(route_path)
                    async def route(request, ct=content_type, c=content):
                        return Response(content=c, media_type=ct)
                    existing.append(route_path)
    except Exception:
        pass

inject_pwa_routes()

# ══════════════════════════════════════════════════════════════════════════════
# 3. CSS — MOBILE / WEB SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
# ── USTAWIENIA MOBILE ──
# .ios-top-bar-wrapper, .ios-hamburger, .mobile-menu-dropdown, .ios-bottom-bar-wrapper
# .block-container padding/margin dla mobile (@media max-width: 1000px)

# ── USTAWIENIA WEB (DESKTOP) ──
# .desktop-only, .tile-link, .control-panel-card
# .block-container padding/margin dla desktop
# Sidebar ukryty (@media min-width: 1001px)

def inject_custom_css():
    st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMainViewContainer"], [data-testid="stHeader"] {
        background: #F2F7FA !important;
        background-color: #F2F7FA !important;
        color: #1B2B3A;
        font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; height: 0px !important; }
    footer { display: none !important; visibility: hidden !important; }
    #MainMenu { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    [data-testid="stFooter"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    .stDeployButton { display: none !important; }
    div:has(> a[href*="streamlit.io/cloud"]) { display: none !important; }
    a[href*="streamlit.io/cloud"] { display: none !important; }
    [data-testid="stActionButton"] { display: none !important; }

    .block-container {
        padding-top: -30px !important;
        max-width: 98% !important;
        padding-bottom: 5rem !important;
    }

    .mobile-nav-item-icon svg,
    .ios-action-icon svg {
        width: 100%;
        height: 100%;
        display: block;
    }

    div[data-testid="stTextInput"]:has(input[aria-label="js_data_exchange"]),
    div[data-testid="stTextInput"]:has(input[id*="js_data_input"]) {
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        width: 1px !important;
        min-height: auto !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .main-layout {
        display: flex;
        gap: 24px;
        overflow: visible !important;
    }

    .tile-link {
        text-decoration: none !important;
        display: block;
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.06);
        margin-bottom: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100px;
        cursor: pointer;
    }
    .tile-link:hover {
        transform: translateX(5px);
        border-color: #006089;
        background: #f8fafc;
    }
    .tile-bg-icon-container {
        position: absolute;
        top: 50%;
        right: 20px;
        transform: translateY(-50%);
        z-index: 1;
        opacity: 0.12;
        transition: all 0.3s ease;
        color: #006089;
    }
    .tile-link:hover .tile-bg-icon-container {
        opacity: 0.3;
        transform: translateY(-50%) scale(1.15);
    }
    .tile-content {
        position: relative;
        z-index: 3;
        padding: 15px 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .tile-label {
        color: #006089;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .tile-title {
        font-size: 18px;
        font-weight: 700;
        color: #1B2B3A;
        margin-bottom: 2px;
    }
    .tile-desc {
        font-size: 11px;
        color: #6B7B8D;
        line-height: 1.3;
    }

    .control-panel-card {
        background: #ffffff;
        border: 1px solid rgba(0, 96, 137, 0.15);
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 25px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .header-section {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .page-title {
        font-size: 24px;
        font-weight: 800;
        color: #1B2B3A;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .content-card {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 20px;
        padding: 24px;
        margin-top: 16px;
        margin-bottom: 20px;
    }

    /* ════ MOBILE: iOS TOP BAR ════ */
    .ios-top-bar-wrapper {
        display: none;
        flex-direction: column;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        width: 100%;
        background: #ffffff !important;
        border-bottom: 1px solid rgba(0, 96, 137, 0.2);
        padding-top: env(safe-area-inset-top, 0px);
    }
    .ios-nav-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 16px;
        height: 56px;
        gap: 10px;
    }
    .ios-hamburger {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: rgba(0, 0, 0, 0.04);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 5px;
        cursor: pointer;
        flex-shrink: 0;
        transition: background 0.2s ease;
        border: 1px solid rgba(0,0,0,0.06);
    }
    .ios-hamburger:active { background: rgba(0, 96, 137, 0.1); }
    .ios-hamburger span {
        display: block;
        width: 16px;
        height: 2px;
        background: #1B2B3A;
        border-radius: 2px;
        transition: all 0.25s ease;
    }
    .ios-hamburger.open span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
    .ios-hamburger.open span:nth-child(2) { opacity: 0; width: 0; }
    .ios-hamburger.open span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

    .ios-nav-center {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex: 1;
        text-align: center;
        min-width: 0;
    }
    .ios-top-logo {
        height: 40px;
        width: auto;
        object-fit: contain;
    }
    .ios-nav-title {
        font-size: 16px;
        font-weight: 800;
        color: #006089;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        line-height: 1.1;
        white-space: nowrap;
    }
    .ios-nav-subtitle {
        font-size: 10px;
        color: #6B7B8D;
        font-weight: 500;
        letter-spacing: 0.3px;
        margin-top: 1px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 180px;
    }
    .ios-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #006089 0%, #003D5C 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 900;
        color: #ffffff;
        flex-shrink: 0;
        cursor: pointer;
        box-shadow: 0 0 12px rgba(0, 96, 137, 0.25);
        border: 1.5px solid rgba(0, 96, 137, 0.3);
    }
    .ios-avatar:active { box-shadow: 0 0 20px rgba(0, 96, 137, 0.5); }

    /* ════ MOBILE: MENU DROPDOWN ════ */
    .mobile-menu-dropdown {
        position: fixed !important;
        top: calc(56px + env(safe-area-inset-top, 0px)) !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 9998 !important;
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(0, 96, 137, 0.15) !important;
        padding: 12px 16px 16px 16px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        max-height: 0 !important;
        overflow: hidden !important;
        opacity: 0 !important;
        transform: translateY(-10px) !important;
        transition: max-height 0.35s cubic-bezier(0.4, 0, 0.2, 1),
                    opacity 0.25s ease,
                    transform 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
    }
    .mobile-menu-dropdown.show {
        max-height: 300px !important;
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    .mobile-menu-item {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        padding: 14px 18px !important;
        background: rgba(0, 0, 0, 0.02) !important;
        border-radius: 14px !important;
        color: #1B2B3A !important;
        text-decoration: none !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        transition: background 0.15s ease, color 0.15s ease !important;
        border: 1px solid rgba(0, 0, 0, 0.04) !important;
        cursor: pointer !important;
    }
    .mobile-menu-item:hover {
        background: rgba(0, 96, 137, 0.06) !important;
        color: #006089 !important;
    }
    .mobile-menu-item:active {
        background: rgba(0, 96, 137, 0.12) !important;
    }
    .mobile-menu-item.active {
        background: rgba(0, 96, 137, 0.08) !important;
        color: #006089 !important;
        border-color: rgba(0, 96, 137, 0.2) !important;
    }
    .mobile-menu-item-icon {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 20px !important;
        height: 20px !important;
        color: #6B7B8D !important;
    }
    .mobile-menu-item.active .mobile-menu-item-icon {
        color: #006089 !important;
    }
    .mobile-menu-item-arrow {
        margin-left: auto !important;
        color: #aaa !important;
        font-size: 12px !important;
    }

    /* ════ MOBILE: BOTTOM BAR ════ */
    .ios-bottom-bar-wrapper {
        display: none;
    }
    .ios-action-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: transparent !important;
        border: none !important;
        color: #6B7B8D;
        cursor: pointer;
        transition: all 0.2s ease;
        flex: 0 1 100px;
        margin: 0 15px;
        gap: 3px;
        user-select: none;
    }
    .ios-action-btn:active { transform: scale(0.92); }
    .ios-action-btn.active {
        color: #006089 !important;
    }
    .ios-action-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
    }
    .ios-action-text {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* ════ RESPONSIVE: MOBILE / WEB ════ */
    .desktop-only { display: block; }
    .mobile-only { display: none; }

    @media (min-width: 1001px) {
        .mobile-sidebar-content { display: block !important; }
        .mobile-menu-dropdown { display: none !important; }
    }

    @media (max-width: 1000px) {
        .ios-top-bar-wrapper { display: flex; }
        .mobile-sidebar-content { display: none !important; }
        .mobile-menu-dropdown { display: flex; }

        .desktop-only { display: none !important; }
        .mobile-only { display: block !important; }

        .block-container {
            padding-top: 0px !important;
            margin-top: -80px !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }
        [data-testid="stMainViewContainer"] {
            padding-top: 0px !important;
            margin-top: -60px !important;
        }
        main {
            padding-top: 0px !important;
            margin-top: -40px !important;
        }
        header[data-testid="stHeader"] { display: none !important; }

        .ios-bottom-bar-wrapper {
            display: flex;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 9999;
            background: rgba(255, 255, 255, 0.97);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-top: 1px solid rgba(0,0,0,0.08);
            padding: 10px 0 calc(10px + env(safe-area-inset-bottom, 12px)) 0;
            justify-content: center;
            align-items: center;
            box-shadow: 0 -4px 15px rgba(0,0,0,0.08);
        }
    }

    div[data-testid="stForm"] {
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        background: #ffffff !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 12px !important;
    }

    .stDateInput div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 12px !important;
    }

    /* Clean input fields — no double-border effect */
    div[data-testid="stTextInput"] {
        background: transparent !important;
    }
    div[data-testid="stTextInput"] label {
        color: #1B2B3A !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
    }
    div[data-testid="stTextInput"] div[data-baseweb="input"] {
        background: #ffffff !important;
        border: 1px solid #d0d5dd !important;
        border-radius: 12px !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
        border-color: #006089 !important;
        box-shadow: 0 0 0 2px rgba(0,96,137,0.15) !important;
    }
    div[data-testid="stTextInput"] input {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 14px 16px !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-family: 'Nunito', sans-serif !important;
        caret-color: #006089 !important;
        min-height: auto !important;
        line-height: 1.4 !important;
    }

    /* Clean multiselect */
    .stMultiSelect *,
    div[data-testid="stMultiSelect"] * {
        color: #1B2B3A !important;
    }
    .stMultiSelect label,
    div[data-testid="stMultiSelect"] > label:first-child,
    div[data-testid="stMultiSelect"] label {
        color: #1B2B3A !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
    }
    div[data-testid="stMultiSelect"] div[data-baseweb="select"],
    .stMultiSelect [data-baseweb="select"] {
        background: #ffffff !important;
        border: 1px solid #d0d5dd !important;
        border-radius: 12px !important;
        font-family: 'Nunito', sans-serif !important;
    }
    div[data-testid="stMultiSelect"] div[data-baseweb="select"]:hover,
    .stMultiSelect [data-baseweb="select"]:hover {
        border-color: #006089 !important;
    }
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] input,
    .stMultiSelect [data-baseweb="select"] input {
        color: #1B2B3A !important;
        background: transparent !important;
        font-family: 'Nunito', sans-serif !important;
    }
    div[data-testid="stMultiSelect"] input::placeholder,
    .stMultiSelect [data-baseweb="select"] input::placeholder {
        color: #6B7B8D !important;
        font-family: 'Nunito', sans-serif !important;
    }
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"],
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(0,96,137,0.08) !important;
        color: #006089 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"] span,
    .stMultiSelect [data-baseweb="tag"] span {
        color: #006089 !important;
    }
</style>
""", unsafe_allow_html=True)

inject_custom_css()

# ══════════════════════════════════════════════════════════════════════════════
# 4. SESSION STATE & DATA
# ══════════════════════════════════════════════════════════════════════════════
PREDEFINED_ALLERGENS = [
    "Mleko krowie (laktoza, kazeina)",
    "Orzechy (ziemne, drzewne)",
    "Gluten/Pszenica",
    "Jaja",
    "Soja",
    "Skorupiaki",
    "Ryby",
    "Sezam",
    "Konserwanty",
    "Sztuczne barwniki",
]

PROFILE_FILE = os.path.join(BASE_DIR, "zdjecia", "profile.json")

def load_profile():
    try:
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return None

def save_profile(data):
    try:
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass

if "page" not in st.session_state:
    st.session_state.page = "home"
if "mobile_menu" not in st.session_state:
    st.session_state.mobile_menu = False
if "last_js_data" not in st.session_state:
    st.session_state.last_js_data = ""
if "child_profile" not in st.session_state:
    st.session_state.child_profile = load_profile()
if "old_profile" not in st.session_state:
    st.session_state.old_profile = None
if "scanned_code" not in st.session_state:
    st.session_state.scanned_code = None

# ══════════════════════════════════════════════════════════════════════════════
# 5. ACTION PROCESSOR
# ══════════════════════════════════════════════════════════════════════════════
qp = st.query_params

for pg in ["home", "form", "settings", "profile", "scanner"]:
    if qp.get("nav") == pg:
        st.session_state.page = pg
        st.session_state.mobile_menu = False
        st.query_params.clear()
        st.rerun()

js_data = st.text_input("js_data_exchange", key="js_data_input", label_visibility="collapsed")

if js_data and js_data != st.session_state.last_js_data:
    st.session_state.last_js_data = js_data
    try:
        parts = {}
        for p in js_data.split('&'):
            if '=' in p:
                k, v = p.split('=', 1)
                parts[k] = urllib.parse.unquote(v)
        action = parts.get('action')
        if action == "nav":
            st.session_state.page = parts.get('page', 'home')
            st.session_state.mobile_menu = False
            st.rerun()
        elif action == "toggle_menu":
            st.session_state.mobile_menu = not st.session_state.mobile_menu
            st.rerun()
        elif action == "v_edit":
            st.session_state.page = "settings"
            st.rerun()
        elif action == "barcode":
            code = parts.get('code', '')
            if code:
                st.session_state.scanned_code = code
                st.session_state.page = "home"
                st.rerun()
        elif action == "cam_off":
            if "scanned_code" in st.session_state:
                del st.session_state.scanned_code
            st.rerun()
    except Exception as e:
        print(f"Action error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. iOS TOP BAR — hamburger + nawigacja + menu mobilne
# ══════════════════════════════════════════════════════════════════════════════
today_label = datetime.date.today().strftime("%d.%m.%Y")
ios_hbg_open = "open" if st.session_state.mobile_menu else ""

st.markdown(f"""
<div class="ios-top-bar-wrapper">
  <div class="ios-nav-bar">
    <div class="ios-hamburger {ios_hbg_open}" data-action="action=toggle_menu">
      <span class="hbr"></span><span class="hbr"></span><span class="hbr"></span>
    </div>
    <div class="ios-nav-center">
      <img src="data:image/png;base64,{LOGO_PURE_B64}" alt="Pure" class="ios-top-logo">
    </div>
    <div class="ios-avatar" data-action="action=nav&page=scanner" style="cursor:pointer;">PB</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Menu mobilne (wysuwane spod iOS bar)
menu_class = "mobile-menu-dropdown show" if st.session_state.mobile_menu else "mobile-menu-dropdown"
menu_items = [
    ("home", "Strona Główna", SVG_HOME),
    ("profile", "Profil Dziecka", SVG_BABY),
    ("scanner", "Skaner", SVG_ADD_DATA),
    ("form", "Formularz", SVG_ADD_DATA),
    ("settings", "Ustawienia", SVG_SETTINGS),
]
menu_html = f'<div class="{menu_class}" id="mobile-menu">'
for pg, label, svg in menu_items:
    active_class = "active" if st.session_state.page == pg else ""
    menu_html += f'<div class="mobile-menu-item {active_class}" data-action="action=nav&page={pg}"><span class="mobile-menu-item-icon">{svg}</span>{label}<span class="mobile-menu-item-arrow">›</span></div>'
menu_html += '</div>'
st.markdown(menu_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 7. SEKCJA TREŚCI — główna zawartość strony
# ══════════════════════════════════════════════════════════════════════════════
col_side, col_main = st.columns([1, 4])

with col_side:
    st.markdown(f"""
    <div class="desktop-only">
    <div class="control-panel-card">
        <div>
            <div class="tile-label">PANEL DOWODZENIA</div>
            <div style="font-size: 22px; font-weight: 800; color: #1B2B3A; margin-top: 10px;">PureBaby</div>
            <div style="font-size: 13px; color: #6B7B8D; margin-top: 5px;">{today_label} · v6</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tiles = [("START","Strona Główna","Widok startowy",SVG_HOME,"home"),
             ("DZIECKO","Profil Dziecka","Dane i alergeny dziecka",SVG_BABY,"profile"),
             ("DANE","Formularz","Przykładowy formularz",SVG_ADD_DATA,"form"),
             ("KONFIGURACJA","Ustawienia","Konfiguracja szkieletu",SVG_SETTINGS,"settings")]
    tiles_html = '<div class="desktop-only">'
    for label, title, desc, svg, pg in tiles:
        active = "border-color:#006089;background:#f0f7fa;" if st.session_state.page==pg else ""
        tiles_html += f'<div class="tile-link" style="{active}"><div class="tile-bg-icon-container">{svg}</div><div class="tile-content"><div class="tile-label">{label}</div><div class="tile-title">{title}</div><div class="tile-desc">{desc}</div></div></div>'
    st.markdown(tiles_html + "</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 7B. SCANNER ENGINE — Open Food Facts API + allergen matching
# ══════════════════════════════════════════════════════════════════════════════

ALLERGEN_SYNONYMS = {
    "Mleko krowie (laktoza, kazeina)": ["mleko","laktoza","kazeina","serwatka","masło","mleczna","mleczne","mleczny","śmietana","twaróg","ser","mlekiem","serwatki","maślanka","mlecznych"],
    "Orzechy (ziemne, drzewne)": ["orzech","orzechy","orzechów","orzechami","orzeszki","migdał","migdały","neregowca","pistacje","laskowe","ziemne","arachidowe","nerkowca"],
    "Gluten/Pszenica": ["gluten","pszenica","pszenny","pszenna","jęczmień","żyto","mąka","owsiana","owsiane","semolina","mąki","pszennej","glutenowa","glutenowe"],
    "Jaja": ["jaj","jaja","jajka","jajko","jajeczny","jajeczne","żółtko","żółtka","białko","jajek","jajami"],
    "Soja": ["soja","sojowe","sojowy","sojowa","soi","tofu","edamame","lecytyna sojowa"],
    "Skorupiaki": ["krewetki","krab","homar","homara","skorupiak","skorupiaki","krewetek","kryla","langusty"],
    "Ryby": ["ryba","ryby","łosoś","tuńczyk","dorsz","śledź","sardynki","rybny","rybne","łososia","rybiego","dorsza"],
    "Sezam": ["sezam","sezamu","sezamowy","sezamowe","sezamowa","sezamem"],
    "Konserwanty": ["konserwant","benzoesan","sorbinian","azotan","siarczyn","siarczyny","glutaminian","E2",
        "E210","E211","E212","E213","E220","E221","E222","E223","E224","E225","E226","E227","E228",
        "E249","E250","E251","E252"],
    "Sztuczne barwniki": ["barwnik","barwniki","E1","tartrazyna","azorubina","koszenila","E102","E104","E110",
        "E122","E124","E129","E131","E132","E133","E142","E151","E155"],
}

# Kategorie produktów nieodpowiednich dla dzieci
UNSAFE_CATEGORIES = [
    "alkohol", "alkohole", "piwo", "wino", "wódka", "whisky", "whiskey", "rum", "gin", "likier", "szampan",
    "papierosy", "tytoń", "papieros", "cygara", "cygaro", "e-papieros",
    "napoje energetyzujące", "energetyk", "energy drink",
    "kawa", "kawy", "espresso", "cappuccino",
]

def sprawdz_sklad(kod_ean, alergie_dziecka):
    """Zwraca (bezpieczny:bool, nazwa_produktu:str, wykryte_skladniki:list)"""
    import urllib.request
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{kod_ean}.json"
        req = urllib.request.Request(url, headers={"User-Agent": "PureBaby/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        if data.get("status") != 1:
            return False, "Nieznany produkt", ["Produkt nie istnieje w bazie"]

        p = data.get("product", {})
        name = p.get("product_name") or p.get("generic_name") or "Nieznany produkt"
        ingredients = (
            p.get("ingredients_text_pl") or
            p.get("ingredients_text") or
            p.get("ingredients_text_en") or
            ""
        )

        # Sprawdź kategorie nieodpowiednie dla dzieci
        categories = p.get("categories_tags", []) or p.get("categories", "") or ""
        if isinstance(categories, str):
            categories_lower = categories.lower()
        else:
            categories_lower = " ".join(categories).lower()
        for unsafe in UNSAFE_CATEGORIES:
            if unsafe in categories_lower or unsafe in name.lower():
                return False, name, [f"Produkt nieodpowiedni dla dziecka ({unsafe})"]

        # Sprawdź alergeny
        if not ingredients:
            return None, name, []  # None = brak składu, nie wiadomo

        text = ingredients.lower()
        text = text.replace("ł", "l").replace("ą", "a").replace("ę", "e").replace("ś", "s").replace("ć", "c").replace("ń", "n").replace("ó", "o").replace("ż", "z").replace("ź", "z")

        found = []
        for allergen in alergie_dziecka:
            synonyms = ALLERGEN_SYNONYMS.get(allergen, [allergen.lower()])
            for syn in synonyms:
                if syn in text:
                    found.append(allergen)
                    break

        if found:
            return False, name, found
        return True, name, []
    except Exception:
        return False, "Błąd połączenia", ["Nie można pobrać danych produktu"]




# ══════════════════════════════════════════════════════════════════════════════
# 7C. PUREBABY PRODUCT CAROUSEL — horizontal recommendation panel
# ══════════════════════════════════════════════════════════════════════════════
PUREBABY_PRODUCTS = [
    {
        "name": "Chusteczki nawilżane 99,9% wody",
        "price": "5,99 zł",
        "old_price": "8,50 zł",
        "image": "https://purebaby.com.pl/environment/cache/images/productGfx_319_500_500/chusteczki-nawilzane-99%2C9-wody.jpg",
        "url": "https://purebaby.com.pl/chusteczki-nawilzane-wet-water-wipes",
        "badge": "-30%"
    },
    {
        "name": "Chusteczki nawilżane z pantenolem",
        "price": "6,50 zł",
        "old_price": "9,99 zł",
        "image": "https://purebaby.com.pl/environment/cache/images/productGfx_358_500_500/chusteczki-nawilzane-z-pantenolem.jpg",
        "url": "https://purebaby.com.pl/chusteczki-nawilzane-do-splukiwania",
        "badge": "-35%"
    },
    {
        "name": "Ręczniki jednorazowe bawełniane",
        "price": "18,99 zł",
        "image": "https://purebaby.com.pl/environment/cache/images/productGfx_308_500_500/bawelniane-reczniki-jednorazowe.jpg",
        "url": "https://purebaby.com.pl/reczniki-jednorazowe-bawelniane-cotton-wipes",
        "badge": "Bestseller"
    },
    {
        "name": "Podkłady higieniczne chłonne",
        "price": "49,99 zł",
        "image": "https://purebaby.com.pl/environment/cache/images/productGfx_349_500_500/podklady-higieniczne-do-przewijania.jpg",
        "url": "https://purebaby.com.pl/podklady-higieniczne-chlonne-male",
        "badge": ""
    },
    {
        "name": "Ręczniki jednorazowe Eco Wipes",
        "price": "13,99 zł",
        "image": "https://purebaby.com.pl/environment/cache/images/productGfx_356_500_500/reczniki-jednorazowe-Eco-Wipes.jpg",
        "url": "https://purebaby.com.pl/reczniki-jednorazowe-biodegradowalne-eco-wipes",
        "badge": "Nowość"
    },
    {
        "name": "Nawilżany papier toaletowy",
        "price": "8,60 zł",
        "image": "https://purebaby.com.pl/environment/cache/images/productGfx_292_500_500/nawilzany-papier-toaletowy.jpg",
        "url": "https://purebaby.com.pl/papier-nawilzany-water-toilet-paper",
        "badge": "Nowość"
    },
    {
        "name": "Chusteczki nawilżane XXL",
        "price": "13,99 zł",
        "image": "https://purebaby.com.pl/environment/cache/images/productGfx_326_500_500/chusteczki-nawilzane-XXL.jpg",
        "url": "https://purebaby.com.pl/chusteczki-nawilzane-wet-water-wipes-XXL",
        "badge": ""
    },
    {
        "name": "Podkłady higieniczne duże",
        "price": "34,99 zł",
        "image": "https://purebaby.com.pl/environment/cache/images/productGfx_343_500_500/podklady-higieniczne-chlonne.jpg",
        "url": "https://purebaby.com.pl/podklady-higieniczne-duze",
        "badge": "Nowość"
    },
]

def render_product_carousel():
    products_html = ""
    for p in PUREBABY_PRODUCTS:
        badge_html = ""
        if p["badge"]:
            badge_color = "#dc2626" if p["badge"].startswith("-") else "#006089"
            badge_html = '<div class="pb-badge" style="background:' + badge_color + ';">' + p["badge"] + '</div>'
        
        old_price_html = ""
        if p.get("old_price"):
            old_price_html = '<div class="pb-old-price">' + p["old_price"] + '</div>'
        
        products_html += (
            '<a href="' + p["url"] + '" target="_blank" rel="noopener noreferrer" class="pb-product-card">'
            + badge_html
            + '<div class="pb-image-wrapper">'
            + '<img src="' + p["image"] + '" alt="' + p["name"] + '" loading="lazy">'
            + '</div>'
            + '<div class="pb-product-info">'
            + '<div class="pb-product-name">' + p["name"] + '</div>'
            + old_price_html
            + '<div class="pb-price">' + p["price"] + '</div>'
            + '<div class="pb-buy-btn">Kup teraz</div>'
            + '</div>'
            + '</a>'
        )
    
    st.components.v1.html("""
    <div class="pb-carousel-container">
        <div class="pb-carousel-header">
            <span class="pb-carousel-title">Polecane produkty PureBaby</span>
            <span class="pb-carousel-subtitle">Bezpieczne dla dziecka od 1. dnia życia</span>
        </div>
        <div class="pb-carousel-track">
            """ + products_html + """
        </div>
    </div>
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .pb-carousel-container {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border-radius: 24px;
        padding: 24px 20px;
        margin: 20px 0;
        border: 1px solid rgba(0, 96, 137, 0.08);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .pb-carousel-header {
        margin-bottom: 20px;
        padding-left: 4px;
    }
    .pb-carousel-title {
        font-size: 20px;
        font-weight: 800;
        color: #006089;
        display: block;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }
    .pb-carousel-subtitle {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
        margin-top: 4px;
        display: block;
        letter-spacing: 0.1px;
    }
    .pb-carousel-track {
        display: flex;
        flex-wrap: nowrap;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        gap: 16px;
        padding-bottom: 12px;
        scroll-snap-type: x mandatory;
        scrollbar-width: thin;
        scrollbar-color: #cbd5e1 transparent;
    }
    .pb-carousel-track::-webkit-scrollbar {
        height: 5px;
    }
    .pb-carousel-track::-webkit-scrollbar-track {
        background: transparent;
        border-radius: 10px;
    }
    .pb-carousel-track::-webkit-scrollbar-thumb {
        background: linear-gradient(90deg, #006089, #0089b3);
        border-radius: 10px;
    }
    .pb-product-card {
        flex: 0 0 190px;
        min-width: 190px;
        max-width: 190px;
        background: #ffffff;
        border-radius: 18px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        overflow: hidden;
        text-decoration: none !important;
        color: inherit;
        position: relative;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        scroll-snap-align: start;
        display: block;
        border: 1px solid rgba(0, 0, 0, 0.04);
    }
    .pb-product-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 8px 25px rgba(0, 96, 137, 0.12);
        border-color: rgba(0, 96, 137, 0.15);
    }
    .pb-badge {
        position: absolute;
        top: 10px;
        left: 10px;
        padding: 5px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 700;
        color: #ffffff;
        z-index: 2;
        letter-spacing: 0.3px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    .pb-image-wrapper {
        width: 100%;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        padding: 16px;
        position: relative;
    }
    .pb-image-wrapper::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 96, 137, 0.1), transparent);
    }
    .pb-image-wrapper img {
        max-width: 85%;
        max-height: 85%;
        object-fit: contain;
        transition: transform 0.3s ease;
    }
    .pb-product-card:hover .pb-image-wrapper img {
        transform: scale(1.05);
    }
    .pb-product-info {
        padding: 14px 16px 16px;
    }
    .pb-product-name {
        font-size: 13px;
        font-weight: 600;
        color: #1e293b;
        line-height: 1.4;
        margin-bottom: 8px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 36px;
        letter-spacing: -0.1px;
    }
    .pb-old-price {
        font-size: 12px;
        color: #94a3b8;
        text-decoration: line-through;
        margin-bottom: 2px;
        font-weight: 500;
    }
    .pb-price {
        font-size: 18px;
        font-weight: 800;
        color: #006089;
        margin-bottom: 10px;
        letter-spacing: -0.3px;
    }
    .pb-buy-btn {
        display: block;
        width: 100%;
        padding: 10px 0;
        background: linear-gradient(135deg, #006089 0%, #0078a8 100%);
        color: #ffffff;
        text-align: center;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 700;
        transition: all 0.2s ease;
        letter-spacing: 0.2px;
        box-shadow: 0 2px 8px rgba(0, 96, 137, 0.2);
    }
    .pb-product-card:hover .pb-buy-btn {
        background: linear-gradient(135deg, #004d6e 0%, #006089 100%);
        box-shadow: 0 4px 12px rgba(0, 96, 137, 0.3);
    }
    </style>
    """, height=320)

# ══════════════════════════════════════════════════════════════════════════════
# 8. WIDOKI — integralna część menu (home, form, settings)
# ══════════════════════════════════════════════════════════════════════════════
with col_main:
    if st.session_state.page == "home":
        profile = st.session_state.child_profile
        if profile:
            photo_html = ""
            if profile.get("photo"):
                photo_html = f'<img src="data:image/png;base64,{profile["photo"]}" style="width:72px;height:72px;border-radius:50%;border:2px solid #006089;object-fit:cover;flex-shrink:0;">'
            st.markdown(f"""
            <div class="content-card" style="display:flex;align-items:center;gap:20px;padding:28px 24px;">
                {photo_html}
                <div>
                    <h3 style="margin:0;">Witaj, {profile['name']}!</h3>
                    <p style="color:#6B7B8D;margin:6px 0 0 0;">Profil dziecka jest aktywny. Możesz skanować produkty i sprawdzać alergeny.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Karuzela produktowa PureBaby — zawsze widoczna na stronie głównej ──
        render_product_carousel()

    elif st.session_state.page == "scanner":
        # ── SCANNER VIEW — osobny widok z auto-start kamery ──
        profile = st.session_state.child_profile
        allergens = profile.get("allergens", []) if profile else []
        import json as _json
        child_allergens_json = _json.dumps(allergens, ensure_ascii=False)
        allergen_synonyms_json = _json.dumps(ALLERGEN_SYNONYMS, ensure_ascii=False)
        unsafe_categories_json = _json.dumps(UNSAFE_CATEGORIES, ensure_ascii=False)

        st.markdown(f"""
        <style>
        .scanner-page * {{ box-sizing: border-box; }}
        .scanner-page {{ font-family: 'Nunito', sans-serif; padding: 16px; background: transparent; }}
        .scanner-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }}
        .scanner-back-btn {{ display: flex; align-items: center; gap: 6px; background: transparent; border: none; color: #006089; font-size: 16px; font-weight: 700; cursor: pointer; font-family: 'Nunito', sans-serif; padding: 8px 0; }}
        .scanner-back-btn svg {{ width: 20px; height: 20px; }}
        .scanner-title {{ font-size: 20px; font-weight: 800; color: #1B2B3A; margin: 0; }}
        .scanner-card {{ background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        #reader {{ width: 100%; max-width: 100%; border-radius: 16px; overflow: hidden; }}
        #scan-msg {{ text-align: center; color: #6B7B8D; margin-top: 12px; font-size: 14px; }}
        #result {{ margin-top: 16px; border-radius: 16px; padding: 20px; display: none; }}
        #result.safe {{ background: #dcfce7; border: 2px solid #86efac; display: block; }}
        #result.danger {{ background: #fecaca; border: 2px solid #f87171; display: block; }}
        #result.warning {{ background: #fef3c7; border: 2px solid #fcd34d; display: block; }}
        #result h3 {{ margin: 0 0 8px 0; font-size: 18px; }}
        #result p {{ margin: 4px 0; font-size: 14px; }}
        .manual-section {{ margin-top: 20px; }}
        .manual-label {{ font-size: 14px; font-weight: 600; color: #1B2B3A; margin-bottom: 8px; }}
        .manual-row {{ display: flex; gap: 8px; }}
        .manual-row input {{ flex: 1; padding: 12px 16px; border: 1px solid #d0d5dd; border-radius: 12px; font-size: 15px; font-family: 'Nunito', sans-serif; color: #1B2B3A; outline: none; background: #fff; }}
        .manual-scan-btn {{ display: none; align-items: center; padding: 12px 20px; background: #006089; color: #fff; border-radius: 12px; font-size: 14px; font-weight: 700; cursor: pointer; font-family: 'Nunito', sans-serif; white-space: nowrap; border: none; }}
        .manual-scan-btn.visible {{ display: flex; }}
        .hidden {{ display: none !important; }}
        </style>

        <div class="scanner-page">
            <div class="scanner-header">
                <button class="scanner-back-btn" id="btn-back-home">
                    <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                    Wróć
                </button>
                <h2 class="scanner-title">Skaner kodów</h2>
            </div>

            <div id="camera-section">
                <div id="reader"></div>
                <div id="scan-msg">Skieruj kamerę na kod kreskowy...</div>
                <div id="result"></div>
            </div>

            <div class="manual-section">
                <div class="manual-label">Lub wpisz kod ręcznie</div>
                <div class="manual-row">
                    <input type="text" id="manual-barcode" placeholder="np. 5901234567890">
                    <button class="manual-scan-btn" id="scan-manual-btn">SPRAWDŹ</button>
                </div>
            </div>
        </div>

        <script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>
        <script>
        (function() {{
            var CHILD_ALLERGENS = {child_allergens_json};
            var ALLERGEN_SYNONYMS = {allergen_synonyms_json};
            var UNSAFE_CATEGORIES = {unsafe_categories_json};

            var cameraSection = document.getElementById('camera-section');
            var btnBackHome = document.getElementById('btn-back-home');
            var manualInput = document.getElementById('manual-barcode');
            var manualBtn = document.getElementById('scan-manual-btn');
            var scanMsg = document.getElementById('scan-msg');
            var resultDiv = document.getElementById('result');

            function normalizeText(text) {{
                return text.toLowerCase()
                    .replace(/ł/g,'l').replace(/ą/g,'a').replace(/ę/g,'e')
                    .replace(/ś/g,'s').replace(/ć/g,'c').replace(/ń/g,'n')
                    .replace(/ó/g,'o').replace(/ż/g,'z').replace(/ź/g,'z');
            }}

            function checkProduct(barcode) {{
                scanMsg.textContent = 'Pobieram dane produktu...';
                resultDiv.className = '';
                resultDiv.style.display = 'none';

                fetch('https://world.openfoodfacts.org/api/v2/product/' + encodeURIComponent(barcode) + '.json', {{
                    headers: {{ 'User-Agent': 'PureBaby/1.0' }}
                }})
                .then(function(r) {{ return r.json(); }})
                .then(function(data) {{
                    if (data.status !== 1) {{
                        resultDiv.className = 'danger';
                        resultDiv.innerHTML = '<h3 style="color:#991b1b;">Nie znaleziono produktu</h3><p style="color:#991b1b;">Produkt o kodzie <strong>' + barcode + '</strong> nie istnieje w bazie.</p>';
                        scanMsg.textContent = '';
                        return;
                    }}

                    var p = data.product || {{}};
                    var name = p.product_name || p.generic_name || 'Nieznany produkt';
                    var ingredients = p.ingredients_text_pl || p.ingredients_text || p.ingredients_text_en || '';
                    var categories = p.categories_tags || [];
                    var catsStr = Array.isArray(categories) ? categories.join(' ').toLowerCase() : String(categories).toLowerCase();

                    for (var i = 0; i < UNSAFE_CATEGORIES.length; i++) {{
                        var uc = UNSAFE_CATEGORIES[i];
                        if (catsStr.indexOf(uc) !== -1 || name.toLowerCase().indexOf(uc) !== -1) {{
                            resultDiv.className = 'danger';
                            resultDiv.innerHTML = '<h3 style="color:#991b1b;">Produkt NIEBEZPIECZNY!</h3><p style="color:#991b1b;">Produkt nieodpowiedni dla dziecka: <strong>' + name + '</strong></p><p style="color:#991b1b;">Kategoria: ' + uc + '</p>';
                            scanMsg.textContent = '';
                            return;
                        }}
                    }}

                    if (!ingredients) {{
                        resultDiv.className = 'warning';
                        resultDiv.innerHTML = '<h3 style="color:#92400e;">Brak informacji</h3><p style="color:#92400e;">Produkt <strong>' + name + '</strong> nie ma listy składników w bazie.</p>';
                        scanMsg.textContent = '';
                        return;
                    }}

                    var text = normalizeText(ingredients);
                    var found = [];
                    for (var a = 0; a < CHILD_ALLERGENS.length; a++) {{
                        var allergen = CHILD_ALLERGENS[a];
                        var synonyms = ALLERGEN_SYNONYMS[allergen] || [allergen.toLowerCase()];
                        for (var s = 0; s < synonyms.length; s++) {{
                            if (text.indexOf(synonyms[s]) !== -1) {{
                                found.push(allergen);
                                break;
                            }}
                        }}
                    }}

                    if (found.length > 0) {{
                        resultDiv.className = 'danger';
                        resultDiv.innerHTML = '<h3 style="color:#991b1b;">UWAGA! Produkt NIEBEZPIECZNY!</h3><p style="color:#991b1b;">Wykryto: <strong>' + found.join(', ') + '</strong></p><p style="color:#991b1b;">Produkt: <strong>' + name + '</strong></p>';
                    }} else {{
                        resultDiv.className = 'safe';
                        resultDiv.innerHTML = '<h3 style="color:#166534;">Produkt bezpieczny!</h3><p style="color:#166534;">W produkcie <strong>' + name + '</strong> nie znaleziono składników, na które dziecko ma alergię.</p>';
                    }}
                    scanMsg.textContent = '';
                }})
                .catch(function(err) {{
                    resultDiv.className = 'danger';
                    resultDiv.innerHTML = '<h3 style="color:#991b1b;">Błąd połączenia</h3><p style="color:#991b1b;">Nie można pobrać danych produktu.</p>';
                    scanMsg.textContent = '';
                }});
            }}

            function startScanner() {{
                var lastCode = '';
                if (typeof Html5Qrcode === 'undefined') {{
                    setTimeout(startScanner, 500);
                    return;
                }}
                if (window._scanner) {{
                    try {{ window._scanner.stop(); }} catch(e) {{}}
                }}
                window._scanner = new Html5Qrcode("reader");
                window._scanner.start(
                    {{ facingMode: "environment" }},
                    {{ fps: 10, qrbox: {{ width: 300, height: 120 }}, formatsToSupport: [
                        Html5QrcodeSupportedFormats.EAN_8,
                        Html5QrcodeSupportedFormats.EAN_13,
                        Html5QrcodeSupportedFormats.UPC_A,
                        Html5QrcodeSupportedFormats.UPC_E,
                        Html5QrcodeSupportedFormats.CODE_128,
                        Html5QrcodeSupportedFormats.CODE_39,
                        Html5QrcodeSupportedFormats.ITF,
                        Html5QrcodeSupportedFormats.CODABAR
                    ]}},
                    function(decodedText) {{
                        if (decodedText !== lastCode) {{
                            lastCode = decodedText;
                            scanMsg.textContent = 'Odczytano kod, analizuję...';
                            window._scanner.stop();
                            
                            // Zapisz do localStorage dla parent listener
                            localStorage.setItem('purebaby_barcode', decodedText);
                            localStorage.setItem('purebaby_ts', Date.now().toString());
                            
                            checkProduct(decodedText);
                        }}
                    }},
                    function() {{}}
                ).catch(function(err) {{
                    scanMsg.textContent = 'Nie można uruchomić kamery.';
                }});
            }}

            // Manual input
            manualInput.addEventListener('input', function() {{
                if (manualInput.value.trim()) {{
                    manualBtn.classList.add('visible');
                }} else {{
                    manualBtn.classList.remove('visible');
                }}
            }});
            manualInput.addEventListener('keydown', function(e) {{
                if (e.key === 'Enter' && manualInput.value.trim()) {{
                    checkProduct(manualInput.value.trim());
                }}
            }});
            manualBtn.addEventListener('click', function() {{
                if (manualInput.value.trim()) {{
                    checkProduct(manualInput.value.trim());
                }}
            }});

            // Back button - wróć do home i zatrzymaj kamerę
            btnBackHome.addEventListener('click', function() {{
                if (window._scanner) {{
                    try {{ window._scanner.stop(); }} catch(e) {{}}
                }}
                localStorage.setItem('purebaby_cam_off', '1');
                localStorage.setItem('purebaby_ts', Date.now().toString());
            }});

            // Auto-start kamery przy wejściu w widok
            startScanner();
        }})();
        </script>
        """, height=600)

    elif st.session_state.page == "profile":
        profile = st.session_state.child_profile

        if profile:
            photo_html = ""
            if profile.get('photo'):
                photo_html = f'<img src="data:image/png;base64,{profile["photo"]}" style="width:72px;height:72px;border-radius:50%;border:2px solid #006089;object-fit:cover;flex-shrink:0;">'
            st.markdown(f"""
            <div class="content-card" style="display:flex;align-items:center;gap:20px;padding:28px 24px;">
                {photo_html}
                <div>
                    <h3 style="margin:0;">Profil: {profile['name']}</h3>
                    <p style="color:#6B7B8D;margin:6px 0 0 0;">Wiek: {profile['age']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if profile['allergens']:
                tags = "".join(f'<span style="background:rgba(0,96,137,0.1);color:#006089;border-radius:20px;padding:6px 14px;font-size:13px;font-weight:600;display:inline-block;margin:4px 6px 4px 0;">{a}</span>' for a in profile['allergens'])
                st.markdown(f'<div class="content-card"><div style="font-size:14px;font-weight:700;color:#1B2B3A;margin-bottom:10px;">Alergeny i nietolerancje</div><div>{tags}</div></div>', unsafe_allow_html=True)

            if st.button("EDYTUJ PROFIL", key="btn_edit_profile", type="primary"):
                st.session_state.old_profile = dict(st.session_state.child_profile)
                st.session_state.child_profile = None
                st.rerun()

        else:
            st.markdown("""
            <div class="content-card">
                <h3>Profil Dziecka</h3>
                <p style="color: #6B7B8D; margin-top: 8px;">Wprowadź dane dziecka i zaznacz alergeny, aby aktywować skaner produktów.</p>
            </div>
            """, unsafe_allow_html=True)

            name = st.text_input("Imię dziecka", key="inp_name", placeholder="np. Zosia")
            age = st.text_input("Wiek", key="inp_age", placeholder="np. 3 lata")

            photo = st.file_uploader("Zdjęcie dziecka", type=["jpg","jpeg","png"], key="inp_photo")

            selected = st.multiselect(
                "Alergeny i nietolerancje",
                options=PREDEFINED_ALLERGENS,
                key="sel_allergens",
                placeholder="Wybierz alergeny..."
            )

            custom = st.text_input("Inny alergen (opcjonalnie)", key="inp_custom", placeholder="np. Czekolada, Truskawki")

            if st.button("ZAPISZ PROFIL", key="btn_save_profile", type="primary", use_container_width=True):
                if name.strip():
                    all_allergens = selected[:]
                    if custom.strip():
                        all_allergens.append(custom.strip())
                    profile_data = {
                        "name": name.strip(),
                        "age": age.strip(),
                        "allergens": all_allergens,
                    }
                    if photo is not None:
                        profile_data["photo"] = base64.b64encode(photo.read()).decode()
                    elif st.session_state.get("old_profile", {}).get("photo"):
                        profile_data["photo"] = st.session_state.old_profile["photo"]
                    st.session_state.child_profile = profile_data
                    save_profile(profile_data)
                    st.session_state.old_profile = None
                    st.success(f"Profil {name.strip()} został pomyślnie zapisany i aktywowany w skanerze")
                    st.rerun()

    elif st.session_state.page == "form":
        st.markdown("""
        <div class="content-card">
            <h3>Formularz</h3>
            <p style="color: #6B7B8D; margin-top: 8px;">Miejsce na przyszłe funkcjonalności.</p>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.page == "settings":
        st.markdown("""
        <div class="content-card">
            <h3>Ustawienia</h3>
            <p style="color: #6B7B8D; margin-top: 8px;">Konfiguracja aplikacji PureBaby.</p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 9. iOS BOTTOM BAR — dolny pasek nawigacji
# ══════════════════════════════════════════════════════════════════════════════
page_names = {"home": "HOME", "profile": "PROFIL", "settings": "USTAW"}
page_icons = {"home": SVG_HOME, "profile": SVG_BABY, "settings": SVG_SETTINGS}
bottom_items = "".join(
    f'<div class="ios-action-btn {"active" if st.session_state.page==pg else ""}" data-action="action=nav&page={pg}">'
    f'<span class="ios-action-icon">{page_icons[pg]}</span>'
    f'<span class="ios-action-text">{page_names[pg]}</span></div>'
    for pg in ["home", "profile", "settings"]
)
st.markdown(f'<div class="ios-bottom-bar-wrapper">{bottom_items}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 10. PARENT MESSAGE LISTENER — odbiera postMessage z kamery (localStorage polling)
# ══════════════════════════════════════════════════════════════════════════════
st.components.v1.html("""
<script>
(function() {
    var pwin = window.parent;
    var pdoc = pwin.document;
    
    // Zabezpieczenie przed wielokrotnym uruchomieniem pętli
    if (pwin._pb_poll) return;
    pwin._pb_poll = true;

    var lastTs = '';
    setInterval(function() {
        var ts = localStorage.getItem('purebaby_ts');
        if (ts && ts !== lastTs) {
            lastTs = ts;
            var code = localStorage.getItem('purebaby_barcode');
            if (code) {
                // Czyścimy pamięć
                localStorage.removeItem('purebaby_barcode');
                localStorage.removeItem('purebaby_ts');
                
                // Szukamy ukrytego pola Streamlit w głównym oknie (pdoc)
                var i = pdoc.querySelector('input[aria-label="js_data_exchange"]');
                if (i) {
                    i.focus();
                    var setter = Object.getOwnPropertyDescriptor(pwin.HTMLInputElement.prototype, 'value').set;
                    setter.call(i, 'action=barcode&code=' + encodeURIComponent(code) + '&ts=' + Date.now());
                    
                    // Wymuszamy aktualizację Reacta w Streamlit
                    i.dispatchEvent(new pwin.Event('input', { bubbles: true }));
                    i.dispatchEvent(new pwin.Event('change', { bubbles: true }));
                    i.dispatchEvent(new pwin.KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
                    i.blur();
                }
            }
            
            var camOff = localStorage.getItem('purebaby_cam_off');
            if (camOff === '1') {
                localStorage.removeItem('purebaby_cam_off');
                localStorage.removeItem('purebaby_ts');
                var i = pdoc.querySelector('input[aria-label="js_data_exchange"]');
                if (i) {
                    i.focus();
                    var setter = Object.getOwnPropertyDescriptor(pwin.HTMLInputElement.prototype, 'value').set;
                    setter.call(i, 'action=cam_off&ts=' + Date.now());
                    i.dispatchEvent(new pwin.Event('input', { bubbles: true }));
                    i.dispatchEvent(new pwin.Event('change', { bubbles: true }));
                    i.dispatchEvent(new pwin.KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
                    i.blur();
                }
            }
        }
    }, 500);
})();
</script>
""", height=0)



# Agresywne ukrywanie elementów Streamlit
hide_html = ("""
<script>
(function() {
    var docs = [];
    try { docs.push(window.top.document); } catch(e) {}
    try { docs.push(window.parent.document); } catch(e) {}
    try {
        var tdoc = window.top.document;
        var hideStyle = tdoc.createElement('style');
        hideStyle.textContent = 'footer,#MainMenu,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"],[data-testid="stFooter"],[data-testid="stSidebarNav"],.stDeployButton,[data-testid="stActionButton"],a[href*="streamlit.io/cloud"],a[href*="streamlit.io"]{display:none!important}';
        tdoc.head.appendChild(hideStyle);
    } catch(e) {}
    setInterval(function() {
        docs.forEach(function(d) {
            try {
                [
                    'footer', '#MainMenu',
                    '[data-testid="stToolbar"]', '[data-testid="stDecoration"]',
                    '[data-testid="stStatusWidget"]', '[data-testid="stFooter"]',
                    '[data-testid="stSidebarNav"]', '.stDeployButton',
                    '[data-testid="stActionButton"]', 'header[data-testid="stHeader"]',
                    'a[href*="streamlit.io/cloud"]', 'a[href*="streamlit.io"]'
                ].forEach(function(sel) {
                    d.querySelectorAll(sel).forEach(function(el) {
                        el.style.setProperty('display', 'none', 'important');
                    });
                });
            } catch(e) {}
        });
    }, 5000);
})();
</script>
""")

st.components.v1.html(hide_html, height=0)
