
const upvote = document.getElementById("upvote");
const downvote = document.getElementById("downvote");

//const resultsDiv = document.getElementById("results");

function upvoteQuiz() {
    downvote.remove();
    sendRating("upvote");

    upvote.removeEventListener("click", upvoteQuiz);
}
function downvoteQuiz() {
    upvote.remove();
    sendRating("downvote");
    downvote.removeEventListener("click", downvoteQuiz);
}


function getCSRFToken() {
    var csrfToken = document.cookie.match(/csrftoken=([\w-]+)/);
    return csrfToken ? csrfToken[1] : '';
}

function sendRating(vote) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('X-CSRFToken', getCSRFToken());
    xhttp.setRequestHeader('Content-Type', 'application/json');

    const data = JSON.stringify({vote : vote});
    xhttp.send(data);

    xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(this.responseText);
    }
    }
}

upvote.addEventListener("click", upvoteQuiz);
downvote.addEventListener("click", downvoteQuiz);