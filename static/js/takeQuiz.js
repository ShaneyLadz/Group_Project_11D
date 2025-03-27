
const questions = document.getElementById("questions mt-4");
var numberOfQuestions = questions.children.length;

document.getElementById("answer_form").addEventListener("submit", function(event) {
    let valid = true;
    var counter = 0

    const questionDivs = Array.from(questions.children)
    questionDivs.forEach((questionDiv) => {
        const answer = questionDiv.querySelector('input[type="radio"]:checked');
        if (!answer) {
            counter++;
        }

    if (counter > 0) {
        valid = false;
    }
    });

    if (!valid) {
        alert("Please ensure all Questions have been answered.")
        event.preventDefault(); 
    }
});