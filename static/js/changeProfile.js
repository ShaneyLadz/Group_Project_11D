
const profileButton = document.getElementById("profile_change");
// id=file_input is an invisible element, only serving to open file prompt
const filePrompt = document.getElementById("file_input");
var image = document.getElementById("profile");

profileButton.addEventListener("click", function() {
    filePrompt.click();
});

function getCSRFToken() {
    var csrfToken = document.cookie.match(/csrftoken=([\w-]+)/);
    return csrfToken ? csrfToken[1] : '';
}

function uploadFile() {
    const formData = new FormData();
    formData.append("profile_picture", filePrompt.files[0]);

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('X-CSRFToken', getCSRFToken());

    xhttp.send(formData);

    xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(this.responseText);
        
        if (response.url && response.error == false) {
            image.src = response.url;
        }
    }
    }   
}

filePrompt.addEventListener("input", uploadFile);