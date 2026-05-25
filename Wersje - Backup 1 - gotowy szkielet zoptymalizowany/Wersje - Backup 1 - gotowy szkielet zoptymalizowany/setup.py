from setuptools import setup
import os
import shutil
import base64

# Try to run the build-time patch, but fail gracefully if dependencies aren't ready
try:
    print("STARTING BUILD-TIME STREAMLIT ICON AND HTML PATCH...")
    
    # Check if streamlit is installed in the current environment
    import streamlit as st
    streamlit_dir = os.path.dirname(st.__file__)
    static_dir = os.path.join(streamlit_dir, 'static')
    index_path = os.path.join(static_dir, 'index.html')
    
    # Check for icon or try to generate it
    local_icon_path = os.path.join(os.path.dirname(__file__), "zdjecia", "icon.png")
    os.makedirs(os.path.dirname(local_icon_path), exist_ok=True)
    
    # If the icon doesn't exist, we can try to generate it using Pillow
    if not os.path.exists(local_icon_path):
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGB', (192, 192), color='#0d1117')
            draw = ImageDraw.Draw(img)
            draw.ellipse([8, 8, 184, 184], outline='#31d5f2', width=4)
            text = "MS"
            try:
                font = ImageFont.truetype("arial.ttf", 80)
            except IOError:
                font = ImageFont.load_default()
            
            try:
                left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
                w = right - left
                h = bottom - top
            except AttributeError:
                w, h = draw.textsize(text, font=font)
                
            x = (192 - w) // 2
            y = (192 - h) // 2 - 5
            draw.text((x, y), text, fill='#31d5f2', font=font)
            img.save(local_icon_path, 'PNG')
            print(f"Generated default 'MS' icon at {local_icon_path}")
        except Exception as e:
            print(f"Could not generate icon during build (Pillow probably not installed yet): {e}")

    # Copy files and patch HTML if index.html exists
    if os.path.exists(local_icon_path) and os.path.exists(index_path):
        # Read the icon file to generate base64 string
        with open(local_icon_path, "rb") as f:
            icon_b64 = base64.b64encode(f.read()).decode()
            
        print(f"Applying HTML patches to {index_path}...")
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'background-color: #0d1117' not in content:
            # Clean up old patches if they exist to avoid duplicates
            content = content.replace('<meta name="apple-mobile-web-app-capable" content="yes">\n', '')
            content = content.replace('    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n', '')
            content = content.replace('    <meta name="mobile-web-app-capable" content="yes">\n', '')
            content = content.replace('    <meta name="apple-mobile-web-app-title" content="Trainer Pro">\n', '')
            content = content.replace('    <meta name="theme-color" content="#0d1117">\n', '')
            
            meta_tags = (
                '<meta name="apple-mobile-web-app-capable" content="yes">\n'
                '    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
                '    <meta name="mobile-web-app-capable" content="yes">\n'
                '    <meta name="apple-mobile-web-app-title" content="App Skeleton">\n'
                '    <meta name="theme-color" content="#0d1117">\n'
                f'    <link rel="apple-touch-icon" href="data:image/png;base64,{icon_b64}">\n'
                f'    <link rel="apple-touch-icon-precomposed" href="data:image/png;base64,{icon_b64}">\n'
                f'    <link rel="icon" href="data:image/png;base64,{icon_b64}">\n'
                '    <style>\n'
                '      html, body, #root {\n'
                '        background-color: #0d1117 !important;\n'
                '        background: #0d1117 !important;\n'
                '      }\n'
                '    </style>\n'
            )
            content = content.replace('<head>', f'<head>\n    {meta_tags}')
            print("PWA tags injected into HTML head.")
            
        target_str = 'content="width=device-width, initial-scale=1, shrink-to-fit=no"'
        if 'viewport-fit=cover' not in content and target_str in content:
            content = content.replace(target_str, 'content="width=device-width, initial-scale=1, shrink-to-fit=no, viewport-fit=cover"')
            print("Viewport-fit=cover added.")
            
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("PATCHED STREAMLIT INDEX STATIC ASSETS SUCCESSFULLY AT BUILD TIME!")
    else:
        print("Streamlit static files or icon missing at build-time. Patcher will run at startup (runtime).")

except Exception as e:
    print(f"Build-time patch skipped (expected if streamlit not fully installed yet): {e}")

setup(
    name="app-skeleton-patch",
    version="0.1",
    py_modules=[],
)
