// JSON for the answers in this quis
let answers = {}

const setQuizName = (name) => {
    answers = {
        ...answers,
        quizname: name
    }
    // console.log(answers)
}

// Saves the answer in an array to be examined by the server afterwards
const answer = (question, answer) => {
    answers = {
        ...answers,
        [question]: answer
    }
    console.log(answers)
    // console.log(answers[question])
}

// Example POST method implementation:
async function postData(url = '', data = {}) {
    // Form-encoded Request, like from Form
    let fetchFormEncodedRequest = {
        cache: "no-cache",
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(answers),
    }
    const response = await fetch(url, fetchFormEncodedRequest);
    return response.json()

}

const submit = async () => {
    const response = await postData('http://localhost:5000/quiz/submit', answers)
    console.log('response', response)
    window.location.replace(`http://localhost:5000/quiz/results/${response.id}`);
}


