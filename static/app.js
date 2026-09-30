const task = document.getElementById("task");
const levelWrap = document.getElementById("level-wrap");
const hoursWrap = document.getElementById("hours-wrap");
const input = document.getElementById("input-text");
const level = document.getElementById("level");
const hours = document.getElementById("hours");
const button = document.getElementById("submit-btn");
const status = document.getElementById("status");
const resultCard = document.getElementById("result-card");
const result = document.getElementById("result");
const copyButton = document.getElementById("copy-btn");


const placeholders = {
    qa: "Example: Which is the largest ocean?",
    explain: "Example: Explain Pythagoras theorem",
    quiz: "Paste an educational passage here.",
    summarize: "Paste a long educational passage here.",
    learn: "Example: SQL"
};


function updateForm() {

    const currentTask = task.value;

    const needsLevel =
        currentTask === "explain" ||
        currentTask === "learn";

    levelWrap.classList.toggle(
        "hidden",
        !needsLevel
    );

    hoursWrap.classList.toggle(
        "hidden",
        currentTask !== "learn"
    );

    input.placeholder =
        placeholders[currentTask];

    const buttonNames = {

        qa: "Ask EduGenie",

        explain: "Explain Concept",

        quiz: "Generate Quiz",

        summarize: "Summarize",

        learn: "Create Learning Path"
    };

    button.textContent =
        buttonNames[currentTask];
}


task.addEventListener(
    "change",
    updateForm
);

task.addEventListener(
    "change",
    () => {

        input.value = "";

        result.innerHTML = "";

        resultCard.classList.add("hidden");

        status.textContent = "";

        copyButton.textContent = "Copy";
    }
);

updateForm();


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function renderResponse(data) {

    resultCard.classList.remove("hidden");

if (data.questions) {

    result.innerHTML = `

        <div id="quiz-container">

            ${data.questions.map(
                (question, index) => `

                <div class="quiz-question">

                    <strong>
                        ${index + 1}.
                        ${escapeHtml(question.question)}
                    </strong>

                    ${question.options.map(
                        option => `

                        <label class="quiz-option">

                            <input
                                type="radio"
                                name="q${index}"
                                value="${escapeHtml(option)}"
                                data-correct="${escapeHtml(question.correct_answer)}"
                                data-explanation="${escapeHtml(question.explanation || "")}"
                            >

                            ${escapeHtml(option)}

                        </label>

                        `
                    ).join("")}

                    <div
                        class="feedback"
                        id="feedback-${index}"
                    ></div>

                </div>

                `
            ).join("")}

        </div>

        <button
            id="submit-quiz"
            type="button"
            class="secondary"
        >
            Submit Quiz
        </button>

        <div
            id="quiz-score"
            class="quiz-score"
        ></div>

    `;


    /* ============================
       SHOW ANSWER FEEDBACK
       ============================ */

    result
        .querySelectorAll(
            'input[type="radio"]'
        )
        .forEach(radio => {

            radio.addEventListener(
                "change",
                () => {

                    const index =
                        radio.name.replace("q", "");

                    const feedback =
                        document.getElementById(
                            `feedback-${index}`
                        );

                    const correct =
                        radio.dataset.correct;

                    if (
                        radio.value === correct
                    ) {

                        feedback.textContent =
                            "✓ Correct! " +
                            radio.dataset.explanation;

                    } else {

                        feedback.textContent =
                            "✗ Incorrect. Correct answer: " +
                            correct +
                            ". " +
                            radio.dataset.explanation;
                    }

                }
            );

        });


    /* ============================
       QUIZ SCORE
       ============================ */

    const submitQuiz =
        document.getElementById(
            "submit-quiz"
        );


    submitQuiz.addEventListener(
        "click",
        () => {

            let score = 0;

            let answered = 0;

            const total =
                data.questions.length;


            data.questions.forEach(
                (question, index) => {

                    const selected =
                        document.querySelector(
                            `input[name="q${index}"]:checked`
                        );


                    const feedback =
                        document.getElementById(
                            `feedback-${index}`
                        );


                    if (!selected) {

                        feedback.textContent =
                            "⚠ Please select an answer.";

                        return;
                    }


                    answered++;


                    const correct =
                        selected.dataset.correct;


                    if (
                        selected.value === correct
                    ) {

                        score++;

                        feedback.textContent =
                            "✓ Correct!";

                    } else {

                        feedback.textContent =
                            "✗ Incorrect. Correct answer: " +
                            correct;
                    }

                }
            );


            const scoreBox =
                document.getElementById(
                    "quiz-score"
                );


            if (answered < total) {

                scoreBox.textContent =
                    `Please answer all questions. You answered ${answered} of ${total}.`;

                return;
            }


            const percentage =
                Math.round(
                    (score / total) * 100
                );


            let message;


            if (percentage >= 80) {

                message =
                    "Excellent work! 🎉";

            } else if (
                percentage >= 60
            ) {

                message =
                    "Good job! Keep practicing. 👍";

            } else {

                message =
                    "Keep learning and try again! 📚";
            }


            scoreBox.innerHTML = `

                <strong>
                    Quiz Score: ${score} / ${total}
                </strong>

                <br>

                ${percentage}% — ${message}

            `;


            submitQuiz.disabled = true;

        }
    );


    return;
}

const text =
    data.answer ||
    data.explanation ||
    data.summary ||
    data.learning_path ||
    JSON.stringify(data, null, 2);

const formattedText =
    escapeHtml(text)
        .replace(/\n/g, "<br>")
        .replace(/•/g, "<br>•");

    result.innerHTML = `

        <div class="result-content">

            ${formattedText}

        </div>
    `;
}


async function submitTask() {

    const value =
        input.value.trim();

    if (!value) {

        status.textContent =
            "Please enter something first.";

        return;
    }


    const endpoints = {

        qa: "/qa",

        explain: "/explain",

        quiz: "/quiz",

        summarize: "/summarize",

        learn: "/learn/recommendations"
    };


    let body;


    if (task.value === "qa") {

        body = {
            question: value
        };

    } else if (task.value === "explain") {

        body = {
            topic: value,
            level: level.value
        };

    } else if (task.value === "quiz") {

        body = {
            text: value
        };

    } else if (task.value === "summarize") {

        body = {
            text: value
        };

    } else {

        body = {

            topic: value,

            level: level.value,

            hours_per_week:
                Number(hours.value)
        };
    }


    button.disabled = true;

button.textContent =
    "⏳ Generating...";

status.textContent =
    "EduGenie is thinking...";
    try {

        const response =
            await fetch(
                endpoints[task.value],
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(body)
                }
            );


        let data;

const contentType =
    response.headers.get("content-type") || "";

if (contentType.includes("application/json")) {
    data = await response.json();
} else {
    const text = await response.text();

    data = {
        detail: text
    };
}


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed."
            );
        }


        renderResponse(data);

        status.textContent =
            "Completed successfully.";

    }

    catch (error) {

        resultCard.classList.remove(
            "hidden"
        );

        result.innerHTML = `

            <div class="result-content">

                ${escapeHtml(error.message)}

            </div>
        `;

        status.textContent =
            "Something went wrong.";

    }

finally {

    button.disabled = false;

    const buttonNames = {

        qa: "Ask EduGenie",

        explain: "Explain Concept",

        quiz: "Generate Quiz",

        summarize: "Summarize",

        learn: "Create Learning Path"
    };

    button.textContent =
        buttonNames[task.value];
}
}


button.addEventListener(
    "click",
    submitTask
);


copyButton.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                result.innerText
            );

            copyButton.textContent =
                "Copied!";

            setTimeout(() => {

                copyButton.textContent =
                    "Copy";

            }, 1200);

        } catch {

            copyButton.textContent =
                "Copy failed";
        }
    }
);