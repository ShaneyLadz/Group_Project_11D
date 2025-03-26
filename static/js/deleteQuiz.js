
const deleteButton = document.getElementById("Delete");
const quizDiv = document.getElementById("quizzes");

function deleteQuiz() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('X-CSRFToken', getCSRFToken());
    xhttp.setRequestHeader('Content-Type', 'application/json');
    
    const radios = quizDiv.getElementsByTagName("input");
    var selected = -1;
    var parentRow = null;

    for (radio of radios) {
        if (radio.checked) {
            selected = radio.value;
            parentRow = radio.parentNode.parentNode;
        }
    }
    
    if (selected == -1) {
        alert("Please select a Quiz before deleting.")
    }
    else if (confirm("Are you sure you want to delete this Quiz?")) {
        
        const data = JSON.stringify({selected : selected});
        xhttp.send(data);

        xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);

            // Remove row in the table
            parentRow.remove();
        }
        }
    }
}

function getCSRFToken() {
    var csrfToken = document.cookie.match(/csrftoken=([\w-]+)/);
    return csrfToken ? csrfToken[1] : '';
}

deleteButton.addEventListener("click", deleteQuiz)