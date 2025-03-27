const questions = document.getElementById("questions");
const addQuestion = document.getElementById("addQuestion");
const deleteQuestion = document.getElementById("deleteQuestion");
var numberOfQuestions = questions.children.length;

function updateTotalForms() {
    document.querySelector('#id_questions-TOTAL_FORMS').value = numberOfQuestions;
}

addQuestion.addEventListener("click", function () {
    if (numberOfQuestions < 10) {
        const form = questions.children[numberOfQuestions];
        if (form && form.style.display === "none") {
            numberOfQuestions++;
            form.style.display = "block";
            form.querySelectorAll('input, select, button, textarea').forEach(element => element.disabled = false);
        }
        updateTotalForms();
    }
});

deleteQuestion.addEventListener("click", function () {
    if (numberOfQuestions > 1) {
        const form = questions.children[numberOfQuestions - 1];
        if (form && form.style.display !== "none") {
            form.style.display = "none";
            form.querySelectorAll('input, select, button, textarea').forEach(element => element.disabled = true);
            numberOfQuestions--;
            updateTotalForms();
        }
    }
});

document.getElementById('quiz_form').addEventListener('submit', function (event) {
    let valid = true;
    let counter = 1;
    const questionDivs = Array.from(questions.children);

    questionDivs.forEach((questionDiv) => {
        const correctAnswer = questionDiv.querySelector('input[type="radio"]:checked');
        if (correctAnswer) {
            const correctAnswerInput = correctAnswer.closest('.input-group').querySelector('input[type="text"]');
            if (!correctAnswerInput || !correctAnswerInput.value.trim()) {
                alert(`Cannot select a blank answer as correct for question ${counter}. Please select a valid answer.`);
                valid = false;
            }
        }
        counter++;
    });

    if (!valid) {
        event.preventDefault();
    }
});