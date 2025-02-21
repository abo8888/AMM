document.getElementById('languageSwitcher').addEventListener('change', function() {
    window.location.href = `/set_language?lang=${this.value}`;
});
