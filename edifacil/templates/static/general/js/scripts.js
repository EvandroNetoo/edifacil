// Page theme based on user preferences
function setThemeBasedOnPreference() {
    const theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-bs-theme', theme);
}
setThemeBasedOnPreference()

// Change page theme on user change preferences
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', setThemeBasedOnPreference);