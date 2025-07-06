const startBtn = document.getElementById("start-btn");
const micStatus = document.getElementById("mic-status");
const transcriptEl = document.getElementById("transcript");
const resultEl = document.getElementById("result");

let products = [];

// Load product data
fetch("products.json")
  .then(res => res.json())
  .then(data => products = data.products);

// Check for mic access first
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(() => {
    micStatus.textContent = "✅ Microphone access granted!";
    startBtn.disabled = false;
  })
  .catch((err) => {
    micStatus.innerHTML = `❌ Microphone not available.<br>
      Please allow mic access in your browser settings. <br>
      Use <strong>Chrome</strong> on desktop or Android.`;
    startBtn.disabled = true;
    console.error("Mic access error:", err);
  });

// Match input text to product keywords
function findProduct(query) {
  query = query.toLowerCase();
  for (const product of products) {
    for (const keyword of product.keywords) {
      if (query.includes(keyword.toLowerCase())) {
        return product;
      }
    }
  }
  return null;
}

// Handle voice input
startBtn.addEventListener("click", () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    resultEl.textContent = "❌ Your browser doesn't support voice input.";
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  transcriptEl.textContent = "🎤 Listening...";
  resultEl.textContent = "";

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    transcriptEl.textContent = `You said: "${transcript}"`;

    const product = findProduct(transcript);
    if (product) {
      resultEl.innerHTML = `✅ Found: ${product.name}.<br/>Redirecting...`;
      setTimeout(() => {
        window.open(product.url, "_blank");
      }, 2000);
    } else {
      resultEl.textContent = "❌ No matching product found.";
    }
  };

  recognition.onerror = (e) => {
    resultEl.textContent = `⚠️ Voice recognition error: ${e.error}. Try again.`;
  };

  recognition.start();
});
