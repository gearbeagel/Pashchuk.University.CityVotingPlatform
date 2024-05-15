document.addEventListener('DOMContentLoaded', function() {
    const notification = document.querySelector('.notification-container');
    const duration = notification ? parseInt(notification.getAttribute('data-duration')) || 5000 : 5000;
    if (notification) {
        setTimeout(function() {
            closeNotification();
        }, duration);
    }
});

function closeNotification() {
    const notification = document.querySelector('.notification-container');
    notification.style.transition = 'opacity 1s';
    notification.style.opacity = 0;

    setTimeout(function() {
        notification.style.display = 'none';
    }, 300);
}
