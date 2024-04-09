document.addEventListener("DOMContentLoaded", function() {
    const changeUsernameLink = document.getElementById("change-username-link");
    const usernameFormContainer = document.getElementById("username-form-container");
    const changeProfilePictureLink = document.getElementById("change-profile-picture-link");
    const profilePicture = document.getElementById("profile-picture");

    changeUsernameLink.addEventListener("click", function(event) {
        event.preventDefault();
        usernameFormContainer.style.display = "block";
    });

    changeProfilePictureLink.addEventListener("click", function(event) {
        event.preventDefault();
        profilePicture.style.display = "block";
    });
});