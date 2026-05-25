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
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        opacity: 0 !important;
        overflow: hidden !important;
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

if "page" not in st.session_state:
    st.session_state.page = "home"
if "mobile_menu" not in st.session_state:
    st.session_state.mobile_menu = False
if "last_js_data" not in st.session_state:
    st.session_state.last_js_data = ""
if "child_profile" not in st.session_state:
    st.session_state.child_profile = None

# ══════════════════════════════════════════════════════════════════════════════
# 5. ACTION PROCESSOR
# ══════════════════════════════════════════════════════════════════════════════
qp = st.query_params
for pg in ["home", "form", "settings", "profile"]:
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
      <div class="ios-nav-title">PureBaby</div>
      <div class="ios-nav-subtitle">{today_label} · v1</div>
    </div>
    <div class="ios-avatar">PB</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Menu mobilne (wysuwane spod iOS bar)
menu_class = "mobile-menu-dropdown show" if st.session_state.mobile_menu else "mobile-menu-dropdown"
menu_items = [
    ("home", "Strona Główna", SVG_HOME),
    ("profile", "Profil Dziecka", SVG_BABY),
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
            <div style="font-size: 13px; color: #6B7B8D; margin-top: 5px;">{today_label} · v1</div>
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
# 8. WIDOKI — integralna część menu (home, form, settings)
# ══════════════════════════════════════════════════════════════════════════════
with col_main:
    if st.session_state.page == "home":
        profile = st.session_state.child_profile
        if profile:
            st.markdown(f"""
            <div class="content-card">
                <h3>Witaj, {profile['name']}! 🎉</h3>
                <p style="color: #6B7B8D; margin-top: 8px;">Profil dziecka jest aktywny. Możesz skanować produkty i sprawdzać alergeny.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="content-card">
                <h3>Witaj w PureBaby! 👶</h3>
                <p style="color: #6B7B8D; margin-top: 8px;">
                    Aplikacja do bezpiecznego skanowania produktów spożywczych dla Twojego dziecka.
                    Zacznij od utworzenia profilu dziecka.
                </p>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.page == "profile":
        profile = st.session_state.child_profile

        if profile:
            st.markdown(f"""
            <div class="content-card">
                <h3>Profil: {profile['name']}</h3>
                <p style="color: #6B7B8D; margin-top: 4px;">Wiek: {profile['age']}</p>
            </div>
            """, unsafe_allow_html=True)

            if profile['allergens']:
                tags = "".join(f'<span style="background:rgba(0,96,137,0.1);color:#006089;border-radius:20px;padding:6px 14px;font-size:13px;font-weight:600;display:inline-block;margin:4px 6px 4px 0;">{a}</span>' for a in profile['allergens'])
                st.markdown(f'<div class="content-card"><div style="font-size:14px;font-weight:700;color:#1B2B3A;margin-bottom:10px;">Alergeny i nietolerancje</div><div>{tags}</div></div>', unsafe_allow_html=True)

            if st.button("EDYTUJ PROFIL", key="btn_edit_profile", type="primary"):
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

            st.markdown("<div style='font-weight:700;margin-top:20px;margin-bottom:8px;color:#1B2B3A;'>Alergeny i nietolerancje</div>", unsafe_allow_html=True)
            selected = []
            cols = st.columns(2)
            for i, a in enumerate(PREDEFINED_ALLERGENS):
                with cols[i % 2]:
                    if st.checkbox(a, key=f"al_{i}"):
                        selected.append(a)

            custom = st.text_input("Inny alergen (opcjonalnie)", key="inp_custom", placeholder="np. Czekolada, Truskawki")

            if st.button("ZAPISZ PROFIL", key="btn_save_profile", type="primary", use_container_width=True):
                if name.strip():
                    all_allergens = selected[:]
                    if custom.strip():
                        all_allergens.append(custom.strip())
                    st.session_state.child_profile = {
                        "name": name.strip(),
                        "age": age.strip(),
                        "allergens": all_allergens,
                    }
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
page_names = {"home": "HOME", "profile": "PROFIL", "form": "FORM", "settings": "USTAW"}
page_icons = {"home": SVG_HOME, "profile": SVG_BABY, "form": SVG_ADD_DATA, "settings": SVG_SETTINGS}
bottom_items = "".join(
    f'<div class="ios-action-btn {"active" if st.session_state.page==pg else ""}" data-action="action=nav&page={pg}">'
    f'<span class="ios-action-icon">{page_icons[pg]}</span>'
    f'<span class="ios-action-text">{page_names[pg]}</span></div>'
    for pg in ["home", "profile", "form", "settings"]
)
st.markdown(f'<div class="ios-bottom-bar-wrapper">{bottom_items}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 10. JS BRIDGE — sendActionToStreamlit + click handler
# ══════════════════════════════════════════════════════════════════════════════
st.components.v1.html("""<script>
(function() {
    var pdoc = document;
    try {
        if (window.parent && window.parent.document) {
            pdoc = window.parent.document;
        }
    } catch(e) {}
    var pwin = window.parent;

    pwin.sendActionToStreamlit = function(s) {
        var i = pdoc.querySelector('input[aria-label="js_data_exchange"]');
        if (i) {
            i.focus();
            var setter = Object.getOwnPropertyDescriptor(pwin.HTMLInputElement.prototype, 'value').set;
            setter.call(i, s + '&ts=' + Date.now());
            i.dispatchEvent(new pwin.Event('input', { bubbles: true }));
            i.dispatchEvent(new pwin.Event('change', { bubbles: true }));
            i.blur();
        }
    };

    pwin.trainerClickHandler = function(e) {
        var el = e.target;
        while (el && el !== pdoc.body) {
            if (el.hasAttribute && el.hasAttribute('data-action')) {
                e.preventDefault();
                e.stopPropagation();
                var actionStr = el.getAttribute('data-action');
                if (pwin.sendActionToStreamlit) {
                    pwin.sendActionToStreamlit(actionStr);
                }
                return;
            }
            el = el.parentElement;
        }
    };

    function attachListeners() {
        if (!pdoc.body) return;
        pdoc.body.removeEventListener('click', pwin.trainerClickHandler);
        pdoc.body.addEventListener('click', pwin.trainerClickHandler);
        pdoc.body.setAttribute('data-bridge-v4', 'true');
    }

    if (pdoc.readyState === 'complete' || pdoc.readyState === 'interactive') {
        attachListeners();
    } else {
        pdoc.addEventListener('DOMContentLoaded', attachListeners);
    }
    setTimeout(attachListeners, 500);
    setTimeout(attachListeners, 2000);
})();
</script>""", height=0)

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
