const editButton = document.getElementById("edit_button");
// editPrompt is a hidden button that receives the quiz_id from the javascript
// when editButton is clicked, and redirects the user to the Edit Page
const editPrompt = document.getElementById("edit_prompt")

function editQuiz() {
    const radios = quizDiv.getElementsByTagName("input");
    var selected = -1;

    for (radio of radios) {
        if (radio.checked) {
            selected = radio.value;
        }
    }

    if (selected == -1) {
        alert("Please select a Quiz before editing.");
    }
    else {
        // Edit the value of editPrompt with the selected quiz's id so that when posted, 
        // the view receives it and uses it to redirect to the Edit Page
        editPrompt.value = selected;
        document.getElementById("add_edit_form").submit()
        }
    }
    
editButton.addEventListener("click", editQuiz)

const questions = document.getElementById("questions");
var numberOfQuestions = questions.children.length;

document.getElementById('quiz_form').addEventListener('submit', function(event) {
    let valid = true;
    var counter = 1;

    const questionDivs = Array.from(questions.children);
    questionDivs.forEach((questionDiv) => {
        const correctAnswer = questionDiv.querySelector('input[type="radio"]:checked');

        if (correctAnswer) {
            const correctAnswerInput = correctAnswer.closest('.answer').querySelector('input[type="text"]');
            
            if (!correctAnswerInput || !correctAnswerInput.value.trim()) {
                alert(`Cannot select a blank answer as correct for question ${counter}. Please select a non-blank answer as correct.`);
                valid = false;
            }
        } 
        counter++;
    });

    if (!valid) {
        event.preventDefault(); 
    }
});