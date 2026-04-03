(() => {
  const storageKey = 'cici-theme';
  const root = document.documentElement;
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

  const getTheme = () => {
    const stored = window.localStorage.getItem(storageKey);
    if (stored === 'light' || stored === 'dark') {
      return stored;
    }

    return mediaQuery.matches ? 'dark' : 'light';
  };

  const setTheme = (theme) => {
    root.setAttribute('data-bs-theme', theme);
    window.localStorage.setItem(storageKey, theme);
    updateButton(theme);
  };

  let themeButton = null;

  const updateButton = (theme) => {
    if (!themeButton) {
      return;
    }

    const isDark = theme === 'dark';
    themeButton.setAttribute('aria-label', isDark ? 'Switch to light theme' : 'Switch to dark theme');
    themeButton.title = isDark ? 'Switch to light theme' : 'Switch to dark theme';
    themeButton.innerHTML = isDark
      ? '<span class="bi bi-sun-fill" aria-hidden="true"></span><span class="theme-toggle-label">Light</span>'
      : '<span class="bi bi-moon-stars-fill" aria-hidden="true"></span><span class="theme-toggle-label">Dark</span>';
  };

  const createButton = () => {
    if (themeButton) {
      return;
    }

    themeButton = document.createElement('button');
    themeButton.type = 'button';
    themeButton.className = 'btn btn-outline-secondary theme-toggle';
    themeButton.addEventListener('click', () => {
      const currentTheme = root.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light';
      setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });

    document.body.appendChild(themeButton);
    updateButton(root.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light');
  };

  const initialize = () => {
    setTheme(getTheme());
    createButton();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }

  mediaQuery.addEventListener('change', () => {
    if (!window.localStorage.getItem(storageKey)) {
      setTheme(getTheme());
    }
  });
})();
