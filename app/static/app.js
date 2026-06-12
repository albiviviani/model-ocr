const serviceStatus = document.getElementById("service-status");
const ocrForm = document.getElementById("ocr-form");
const fileInput = document.getElementById("file");
const textForm = document.getElementById("text-form");
const textInput = document.getElementById("text");
const resultStatus = document.getElementById("result-status");
const resultOutput = document.getElementById("result-output");
const copyOutput = document.getElementById("copy-output");
const clearOutput = document.getElementById("clear-output");

function setStatus(message, type = "info") {
  resultStatus.textContent = message;
  resultStatus.className = `result-status ${type}`;
}

function sanitizeText(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

async function fetchJson(url, formData) {
  const response = await fetch(url, {
    method: "POST",
    body: formData,
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || payload.error || response.statusText || "Request failed.");
  }
  return payload;
}

async function updateServiceStatus() {
  try {
    const health = await fetch("/api/health").then((res) => res.json());
    serviceStatus.textContent = health.status === "ok" ? "Service is online." : "Service available.";
    serviceStatus.className = "status-pill status-pill--online";
  } catch (error) {
    serviceStatus.textContent = "OCR service is unavailable.";
    serviceStatus.className = "status-pill status-pill--error";
  }
}

function showResult(text) {
  const safeText = sanitizeText(text || "(no text extracted)");
  resultOutput.textContent = safeText;
  setStatus("Extraction complete.", "success");
}

ocrForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const file = fileInput.files[0];
  if (!file) {
    setStatus("Please choose an image or PDF file.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  setStatus("Extracting text from file...", "loading");

  try {
    const payload = await fetchJson("/api/ocr", formData);
    showResult(payload.text);
    fileInput.value = "";
  } catch (error) {
    setStatus(error.message, "error");
  }
});

textForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const textValue = textInput.value.trim();
  if (!textValue) {
    setStatus("Please enter some text.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("text", textValue);

  setStatus("Submitting text...", "loading");

  try {
    const payload = await fetchJson("/api/ocr", formData);
    showResult(payload.text);
    textInput.value = "";
  } catch (error) {
    setStatus(error.message, "error");
  }
});

copyOutput.addEventListener("click", async () => {
  const text = resultOutput.textContent || "";
  if (!text) return;
  await navigator.clipboard.writeText(text);
  setStatus("Copied extracted text to clipboard.", "success");
});

clearOutput.addEventListener("click", () => {
  resultOutput.textContent = "";
  setStatus("No extraction performed yet.", "info");
});

window.addEventListener("load", () => {
  updateServiceStatus();
  setStatus("Ready to extract text.", "info");
});
