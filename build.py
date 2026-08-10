#!/usr/bin/env python3
"""Build script: generate charts -> markdown to HTML -> (optional) PDF.
Usage: python build.py
"""
import os, sys, shutil, subprocess, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

MD = os.path.join(ROOT, 'AP微观经济学讲义.md')
CSS = os.path.join(ROOT, 'style.css')
HTML = os.path.join(ROOT, 'AP微观经济学讲义.html')
PDF = os.path.join(ROOT, 'AP微观经济学讲义.pdf')
PY = os.path.join(ROOT, 'generate_charts.py')

def step(msg):
    print(f'\n{"="*50}')
    print(f'  {msg}')
    print(f'{"="*50}')

# ── Step 1: Generate charts ──
step('[1/3] Generating charts...')
subprocess.run([sys.executable, PY], check=True)
print('  Charts done (PNG).')

# ── Step 2: Markdown -> HTML via pandoc ──
step('[2/3] Markdown -> HTML (pandoc)...')

# pandoc has encoding issues with Chinese paths on Windows;
# copy to temp ASCII name, run pandoc, copy back.
temp_md = os.path.join(ROOT, '_temp_lecture.md')
temp_html = os.path.join(ROOT, '_temp_lecture.html')
shutil.copy2(MD, temp_md)

gh = 'github-style'
gh_css = ['github-markdown-light.css', 'custom.css', 'print.css']
css_args = []
for _c in gh_css:
    css_args += ['--css', f'{gh}/{_c}']

cmd = (['pandoc', temp_md, '-o', temp_html,
        '--standalone',
        f'--include-before-body={gh}/before.html',
        f'--include-after-body={gh}/after.html']
       + css_args
       + ['--katex', '--number-sections', '--number-offset=-1'])
subprocess.run(cmd, check=True)

shutil.copy2(temp_html, HTML)
os.remove(temp_md)
os.remove(temp_html)
print(f'  HTML done.')

# ── Step 3: HTML -> PDF via headless browser ──
step('[3/3] HTML -> PDF (headless browser)...')

browsers = [
    os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
    os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
    os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe'),
    os.path.expandvars(r'%ProgramFiles%\Microsoft\Edge\Application\msedge.exe'),
    os.path.expandvars(r'%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe'),
]
browser = None
for b in browsers:
    if os.path.exists(b):
        browser = b
        break

if browser:
    bname = os.path.basename(browser)
    print(f'  Browser: {bname}')
    import urllib.parse
    html_uri = 'file:///' + HTML.replace('\\', '/').replace(' ', '%20')
    # Use ASCII temp name for PDF output, then move
    temp_pdf = os.path.join(ROOT, '_temp_output.pdf')
    subprocess.run([browser, '--headless', '--disable-gpu',
                    '--no-sandbox', '--no-pdf-header-footer',
                    '--virtual-time-budget=20000',
                    f'--print-to-pdf={temp_pdf}', html_uri],
                   capture_output=True, timeout=180)
    import time; time.sleep(2)
    if os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0:
        shutil.copy2(temp_pdf, PDF)
        os.remove(temp_pdf)
        size_kb = os.path.getsize(PDF) / 1024
        print(f'  PDF done: {size_kb:.0f} KB')
    else:
        print('  Auto-PDF failed. Open HTML in browser and print to PDF manually.')
        print(f'  HTML: {HTML}')
else:
    print('  Chrome/Edge not found. Open HTML in browser and print to PDF:')
    print(f'  {HTML}')

step('Build complete!')
