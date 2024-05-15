document.addEventListener("DOMContentLoaded", function() {
    const changeUsernameLink = document.getElementById("change-username-link");
    const usernameFormContainer = document.getElementById("username-form-container");
    const changeProfilePictureLink = document.getElementById("change-profile-picture-link");
    const profilePicture = document.getElementById("profile-picture");
    const viewNotificationSettingsLink = document.getElementById("view-notification-settings");
    const notificationSettingsFormContainer = document.getElementById("notification-settings-form");

    changeUsernameLink.addEventListener("click", function(event) {
        event.preventDefault();
        toggleDisplay(usernameFormContainer);
    });

    changeProfilePictureLink.addEventListener("click", function(event) {
        event.preventDefault();
        toggleDisplay(profilePicture);
    });

    viewNotificationSettingsLink.addEventListener("click", function(event) {
        event.preventDefault();
        toggleDisplay(notificationSettingsFormContainer);
    });

    // Function to toggle display property
    function toggleDisplay(element) {
        if (element.style.display === "block") {
            element.style.display = "none";
        } else {
            element.style.display = "block";
        }
    }
});
