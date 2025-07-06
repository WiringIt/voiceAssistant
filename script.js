const startBtn = document.getElementById("start-btn");
const transcriptEl = document.getElementById("transcript");
const resultEl = document.getElementById("result");

let products = [];

// Load product data
fetch("products.json")
  .then(res => res.json())
  .then(data => products = data.products);

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
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
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
      resultEl.innerHTML = `✅ Found: ${product.name}. <br/>Redirecting...`;
      setTimeout(() => {
        window.open(product.url, "_blank");
      }, 2000);
    } else {
      resultEl.textContent = "❌ No matching product found.";
    }
  };

  recognition.onerror = () => {
    transcriptEl.textContent = "⚠️ Voice recognition error. Try again.";
  };

  recognition.start();
});
