document.addEventListener('DOMContentLoaded', function() {
    var showMoreBtns = document.querySelectorAll('.show-more-btn');

    showMoreBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var card = this.parentElement;
            var text = card.querySelector('.project-card-text');
            text.classList.toggle('expanded');
            this.textContent = text.classList.contains('expanded') ? 'Show less' : 'Show more';
        });
    });
});
