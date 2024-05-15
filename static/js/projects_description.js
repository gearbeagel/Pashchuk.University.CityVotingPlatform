document.addEventListener('DOMContentLoaded', function() {
    const showMoreBtns = document.querySelectorAll('.show-more-btn');

    showMoreBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const card = this.parentElement;
            const text = card.querySelector('.project-card-text');
            text.classList.toggle('expanded');
            this.textContent = text.classList.contains('expanded') ? 'Show less' : 'Show more';
        });
    });
});
