// Обработка выбора города
document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('citySelect');

    if (citySelect) {
        citySelect.addEventListener('change', function() {
            const selectedCity = this.value;

            // Сохраняем выбор города в localStorage
            localStorage.setItem('selectedCity', selectedCity);

            // Обновляем контент на странице
            updateContentByCity(selectedCity);

            // Показываем анимацию смены контента
            animateContentChange();
        });

        // Восстанавливаем выбранный город при загрузке
        const savedCity = localStorage.getItem('selectedCity');
        if (savedCity) {
            citySelect.value = savedCity;
        }
    }
});

function updateContentByCity(cityId) {
    // Здесь будет логика обновления контента в зависимости от города
    // Пока просто показываем уведомление
    showNotification(`Город изменен! Фильтрация по выбранному городу.`);
}

function animateContentChange() {
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.style.animation = 'none';
        setTimeout(() => {
            mainContent.style.animation = 'fadeIn 0.5s ease';
        }, 10);
    }
}

function showNotification(message) {
    // Создаем уведомление
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--primary-blue);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        box-shadow: var(--shadow);
        z-index: 1001;
        animation: slideUp 0.3s ease;
    `;

    document.body.appendChild(notification);

    // Удаляем уведомление через 3 секунды
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Плавная прокрутка для якорей
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});