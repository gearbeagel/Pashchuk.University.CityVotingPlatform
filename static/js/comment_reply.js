function replyTo(username) {
        document.getElementById("comment_text").value = "@" + username + " ";
        document.getElementById("comment_text").focus();
    }