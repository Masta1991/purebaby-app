# Szkielet MS — v25

Profesjonalny szkielet startowy (boilerplate) dla aplikacji Streamlit z responsywnym interfejsem mobile + desktop w stylu natywnej aplikacji iOS.

> [!NOTE]
> Pełna dokumentacja: [DOKUMENTACJA_POL.md](DOKUMENTACJA_POL.md)

---

## 🚀 Uruchomienie

```bash
pip install -r requirements.txt
streamlit run app.py
```

Otwórz `http://localhost:8501`. Test mobile: F12 → widok responsywny.

---

## 📱 Architektura

### Mobile (≤1000px)
```
┌──────────────────────────────────────────┐
│ [≡] Szkielet MS              [MS]       │ ← iOS Top Bar
├──────────────────────────────────────────┤
│                                          │
│            OBSZAR ROBOCZY                │ ← Widok strony
│                                          │
├──────────────────────────────────────────┤
│   [HOME]       [FORM]      [USTAW]       │ ← iOS Bottom Bar
└──────────────────────────────────────────┘
```

### Desktop (>1000px)
```
┌──────────────────────────────────────────────────────────┐
│  SIDEBAR              │  OBSZAR ROBOCZY                  │
│ ┌───────────────────┐ │ ┌──────────────────────────────┐ │
│ │ PANEL DOWODZENIA  │ │ │                              │ │
│ │ Witaj, MS!        │ │ │  Treść wybranej strony       │ │
│ └───────────────────┘ │ │                              │ │
│ ┌───────────────────┐ │ │                              │ │
│ │ START             │ │ │                              │ │
│ │ DANE              │ │ │                              │ │
│ │ KONFIGURACJA      │ │ │                              │ │
│ └───────────────────┘ │ └──────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

---

## 📂 Struktura Kodu (`app.py`)

| Sekcja | Opis |
|---|---|
| §1-2 | Init, PWA, ikony |
| §3 | **CSS — Mobile / Web Settings** |
| §4 | Session State & Data |
| §5 | Action Processor (JS bridge) |
| §6 | **iOS TOP BAR** — hamburger + menu |
| §7 | **SEKCJA TREŚCI** — sidebar + content |
| §8 | **WIDOKI** — home, form, settings |
| §9 | **iOS BOTTOM BAR** |
| §10 | JS Bridge + ukrywanie Streamlit |

---

## ⚡ Nawigacja (JS Bridge)

Kliknięcia w `data-action` → JS handler → ukryty input → Python → `st.rerun()`

| Akcja | Efekt |
|---|---|
| `action=nav&page=home` | Strona Główna |
| `action=nav&page=form` | Formularz |
| `action=nav&page=settings` | Ustawienia |
| `action=toggle_menu` | Otwórz/zamknij menu |

---

## 🎨 Klasy CSS

| Klasa | Opis |
|---|---|
| `.ios-top-bar-wrapper` | Górny pasek (mobile) |
| `.ios-hamburger` | Hamburger z animacją ☰ → ✕ |
| `.ios-hamburger.open` | Stan otwarty (X) |
| `.mobile-menu-dropdown` | Wysuwane menu |
| `.mobile-menu-dropdown.show` | Menu widoczne |
| `.ios-bottom-bar-wrapper` | Dolny pasek (mobile) |
| `.desktop-only` | Tylko desktop |
| `.control-panel-card` | Karta powitalna sidebar |
| `.tile-link` | Kafelek nawigacyjny |
| `.content-card` | Karta zawartości |

---

## 🔧 Jak Dodać Nowy Widok

1. Dodaj SVG ikonę w §1
2. Dodaj wpis w `menu_items` (§6) i `page_names`/`page_icons` (§9)
3. Dodaj warunek `elif st.session_state.page == "nowy"` w §8
4. Dodaj kafelek w `tiles` (§7) dla desktopu

---

## 🌐 PWA

- Ikona z `App Icon/icon_192.png`
- Manifest jako Blob URL
- Service Worker: `/sw.js`
- Meta tagi dla iOS Safari
