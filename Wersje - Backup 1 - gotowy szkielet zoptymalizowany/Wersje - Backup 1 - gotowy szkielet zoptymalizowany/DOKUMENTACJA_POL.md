# 📝 Dokumentacja Szkieletu MS — v25

## 🚀 Uruchomienie

```bash
pip install -r requirements.txt
streamlit run app.py
```

Aplikacja otworzy się pod adresem `http://localhost:8501`.

---

## 📂 Struktura Pliku `app.py`

Kod jest podzielony na wyraźne sekcje:

| Sekcja | Opis |
|---|---|
| **§1** | Initialization — ścieżki, SVG ikony |
| **§2** | PWA Setup — generowanie ikon, manifest, meta tagi, service worker |
| **§3** | **CSS — Mobile / Web Settings** — style dla mobile i desktop z wyraźnym podziałem |
| **§4** | Session State & Data — dane testowe, klucze sesji |
| **§5** | Action Processor — obsługa akcji z JS bridge (`nav`, `toggle_menu`) |
| **§6** | **iOS TOP BAR** — hamburger, tytuł, avatar, menu mobilne (wysuwane) |
| **§7** | **SEKCJA TREŚCI** — sidebar desktopowy + główny kontener |
| **§8** | **WIDOKI** — Strona Główna, Formularz, Ustawienia (integralna część menu) |
| **§9** | **iOS BOTTOM BAR** — dolny pasek nawigacji (HOME, FORM, USTAW) |
| **§10** | JS Bridge — `sendActionToStreamlit` + globalny `trainerClickHandler` |

---

## 📱 Nawigacja

### Mobile (≤1000px)
- **iOS Top Bar** — hamburger (lewo), tytuł (środek), avatar (prawo)
- **Hamburger** — kliknięcie otwiera/zamyka menu (animacja ☰ → ✕)
- **Menu mobilne** — wysuwany dropdown z 3 pozycjami: Strona Główna, Formularz, Ustawienia
- **iOS Bottom Bar** — 3 przyciski: HOME, FORM, USTAW

### Desktop (>1000px)
- **Sidebar** — kafelek "PANEL DOWODZENIA" + 3 kafelki: START, DANE, KONFIGURACJA
- **Mobile elementy ukryte** — hamburger, bottom bar, menu dropdown

---

## ⚡ JS Bridge — Jak Działają Kliknięcia

```
Kliknięcie w element z data-action
  → trainerClickHandler (document.body)
  → sendActionToStreamlit("action=...&...")
  → ukryty st.text_input (js_data_exchange)
  → Python wykrywa zmianę → st.rerun()
```

### Obsługiwane Akcje

| Akcja | Efekt |
|---|---|
| `action=nav&page=home` | Przejdź na Stronę Główną |
| `action=nav&page=form` | Przejdź na Formularz |
| `action=nav&page=settings` | Przejdź na Ustawienia |
| `action=toggle_menu` | Otwórz/zamknij menu mobilne |

---

## 🎨 Klasy CSS — Słownik

| Klasa | Opis |
|---|---|
| `.ios-top-bar-wrapper` | Górny pasek iOS (mobile only) |
| `.ios-hamburger` | Przycisk hamburgera z animacją ☰ → ✕ |
| `.ios-hamburger.open` | Stan otwarty (X) |
| `.ios-nav-bar` | Pasek nawigacyjny wewnątrz top bara |
| `.ios-nav-center` | Środkowa sekcja z tytułem |
| `.ios-avatar` | Okrągły awatar z inicjałami |
| `.mobile-menu-dropdown` | Wysuwane menu mobilne |
| `.mobile-menu-dropdown.show` | Menu widoczne (animacja) |
| `.mobile-menu-item` | Pojedynczy element menu |
| `.mobile-menu-item.active` | Aktywny element menu |
| `.ios-bottom-bar-wrapper` | Dolny pasek nawigacji (mobile only) |
| `.ios-action-btn` | Przycisk w dolnym pasku |
| `.ios-action-btn.active` | Aktywny przycisk dolnego paska |
| `.desktop-only` | Ukryte na mobile |
| `.mobile-only` | Ukryte na desktopie |
| `.control-panel-card` | Karta powitalna w sidebarze |
| `.tile-link` | Kafelek nawigacyjny w sidebarze |
| `.content-card` | Karta zawartości widoku |

---

## 📱 Ustawienia Mobile vs Web

### Mobile (`@media max-width: 1000px`)
- `.ios-top-bar-wrapper` — widoczny
- `.ios-bottom-bar-wrapper` — widoczny
- `.mobile-menu-dropdown` — widoczny po otwarciu
- `.desktop-only` — ukryty
- `padding-top: 0px`, `margin-top: -80px` na `.block-container`

### Web (`@media min-width: 1001px`)
- `.ios-top-bar-wrapper` — ukryty
- `.ios-bottom-bar-wrapper` — ukryty
- `.mobile-menu-dropdown` — ukryty
- `.desktop-only` — widoczny
- Sidebar z kafelkami nawigacyjnymi

---

## 🔧 Jak Dodać Nowy Widok

1. Dodaj SVG ikonę w §1
2. Dodaj wpis w `menu_items` (§6) i `page_names`/`page_icons` (§9)
3. Dodaj warunek `elif st.session_state.page == "nowy"` w §8
4. Dodaj kafelek w `tiles` (§7) dla desktopu

---

## 🌐 PWA

- Ikona generowana z `App Icon/icon_192.png`
- Manifest wstrzykiwany przez JS jako Blob URL
- Service Worker: `/sw.js`
- Meta tagi dla iOS Safari (`apple-mobile-web-app-capable`)
