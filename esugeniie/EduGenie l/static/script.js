// EduGenie frontend logic
// Handles all 5 forms via fetch() calls to the FastAPI backend and
// renders the results inline, without a page reload.

function showLoading(el, message) {
  el.innerHTML = `<div class="loading">${message}</div>`;
}

function showError(el, message) {
  el.innerHTML = `<div class="error-box">⚠️ ${escapeHtml(message)}</div>`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.innerText = str;
  return div.innerHTML;
}

// ---------------------------------------------------------------------
// Q&A
// ---------------------------------------------------------------------
document.getElementById("qaForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = document.getElementById("question").value.trim();
  const resultEl = document.getElementById("qaResult");
  if (!question) return;

  showLoading(resultEl, "Thinking...");
  try {
    const res = await fetch(`/qa?question=${encodeURIComponent(question)}`);
    const data = await res.json();
    if (!res.ok || data.error) {
      showError(resultEl, data.error || "Something went wrong.");
      return;
    }
    resultEl.innerHTML = `<div class="result-box"><strong>Answer:</strong>${escapeHtml(data.answer)}</div>`;
  } catch (err) {
    showError(resultEl, "Could not reach the server. Is it running?");
  }
});

// ---------------------------------------------------------------------
// Explanation
// ---------------------------------------------------------------------
document.getElementById("explainForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const topic = document.getElementById("topic").value.trim();
  const resultEl = document.getElementById("explanationResult");
  if (!topic) return;

  showLoading(resultEl, "Preparing a simple explanation...");
  try {
    const res = await fetch("/explain/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    const data = await res.json();
    if (!res.ok || data.error) {
      showError(resultEl, data.error || "Something went wrong.");
      return;
    }
    resultEl.innerHTML = `<div class="result-box"><strong>Explanation:</strong>${escapeHtml(data.explanation)}</div>`;
  } catch (err) {
    showError(resultEl, "Could not reach the server. Is it running?");
  }
});

// ---------------------------------------------------------------------
// Summarization
// ---------------------------------------------------------------------
document.getElementById("summaryForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("summaryText").value.trim();
  const resultEl = document.getElementById("summaryResult");
  if (!text) return;

  showLoading(resultEl, "Summarizing...");
  try {
    const res = await fetch("/summarize/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    if (!res.ok || data.error) {
      showError(resultEl, data.error || "Something went wrong.");
      return;
    }
    resultEl.innerHTML = `<div class="result-box"><strong>Summary:</strong>${escapeHtml(data.summary)}</div>`;
  } catch (err) {
    showError(resultEl, "Could not reach the server. Is it running?");
  }
});

// ---------------------------------------------------------------------
// Quiz
// ---------------------------------------------------------------------
document.getElementById("quizForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("quizText").value.trim();
  const resultEl = document.getElementById("quizResult");
  if (!text) return;

  showLoading(resultEl, "Generating quiz...");
  try {
    const res = await fetch("/quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    const quiz = data.quiz;

    if (!res.ok || !quiz || (quiz[0] && quiz[0].error)) {
      showError(resultEl, (quiz && quiz[0] && quiz[0].error) || "Could not generate quiz.");
      return;
    }

    renderQuiz(resultEl, quiz);
  } catch (err) {
    showError(resultEl, "Could not reach the server. Is it running?");
  }
});

function renderQuiz(container, quiz) {
  container.innerHTML = "";
  const wrapper = document.createElement("div");

  quiz.forEach((q, index) => {
    const qDiv = document.createElement("div");
    qDiv.className = "quiz-question";

    const title = document.createElement("p");
    title.className = "q-title";
    title.innerText = `Q${index + 1}: ${q.question}`;
    qDiv.appendChild(title);

    q.options.forEach((opt, optIndex) => {
      const label = document.createElement("label");
      label.className = "option-row";

      const input = document.createElement("input");
      input.type = "radio";
      input.name = `quiz-q${index}`;
      input.value = opt;

      label.appendChild(input);
      label.appendChild(document.createTextNode(opt));
      qDiv.appendChild(label);
    });

    const checkBtn = document.createElement("button");
    checkBtn.type = "button";
    checkBtn.className = "check-btn";
    checkBtn.innerText = "Check Answer";

    const feedback = document.createElement("div");

    checkBtn.addEventListener("click", () => {
      const selected = qDiv.querySelector(`input[name="quiz-q${index}"]:checked`);
      if (!selected) {
        feedback.className = "feedback-incorrect";
        feedback.innerText = "Please select an option first.";
        return;
      }
      if (selected.value === q.answer) {
        feedback.className = "feedback-correct";
        feedback.innerText = "✅ Correct!";
      } else {
        feedback.className = "feedback-incorrect";
        feedback.innerText = `❌ Incorrect. Correct answer: ${q.answer}`;
      }
    });

    qDiv.appendChild(checkBtn);
    qDiv.appendChild(feedback);
    wrapper.appendChild(qDiv);
  });

  container.appendChild(wrapper);
}

// ---------------------------------------------------------------------
// Learning Path
// ---------------------------------------------------------------------
document.getElementById("learnForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const topic = document.getElementById("learnTopic").value.trim();
  const resultEl = document.getElementById("learnResult");
  if (!topic) return;

  showLoading(resultEl, "Building your learning path...");
  try {
    const res = await fetch(`/learn/recommendations?topic=${encodeURIComponent(topic)}`);
    const data = await res.json();
    if (!res.ok || data.error) {
      showError(resultEl, data.error || "Something went wrong.");
      return;
    }
    resultEl.innerHTML = `<div class="result-box"><strong>Learning Recommendations for "${escapeHtml(data.topic)}":</strong>${escapeHtml(data.recommendation)}</div>`;
  } catch (err) {
    showError(resultEl, "Could not reach the server. Is it running?");
  }
});
