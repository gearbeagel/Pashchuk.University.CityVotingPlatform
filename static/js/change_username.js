document.addEventListener("DOMContentLoaded", function() {
    const changeUsernameLink = document.getElementById("change-username-link");
    const usernameFormContainer = document.getElementById("username-form-container");

    changeUsernameLink.addEventListener("click", function(event) {
        event.preventDefault();
        usernameFormContainer.style.display = "block";
    });
});