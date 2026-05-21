async function runAnalysis(isUrl) {
    const text = document.getElementById('inputText').value;
    const resultsCard = document.getElementById('resultsCard');
    
    if (!text) return alert("Please enter some content");

    resultsCard.classList.remove('d-none');
    resultsCard.innerHTML = "Processing...";

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text: text, is_url: isUrl })
        });
        
        const data = await response.json();
        if (data.error) throw new Error(data.error);

        renderResults(data.results);
    } catch (err) {
        alert(err.message);
    }
}

function renderResults(res) {
    const card = document.getElementById('resultsCard');
    const aiPct = (res.ai_score * 100).toFixed(1);
    const slopPct = (res.slop_prob * 100).toFixed(1);

    card.innerHTML = `
        <h4>Verdict: ${res.ai_score > 0.5 ? '🤖 AI Generated' : '✍️ Human Written'}</h4>
        <div class="mt-3">
            <p>AI Probability: <b>${aiPct}%</b></p>
            <p>Slop Severity: <b>${slopPct}%</b></p>
            <p>Perplexity: ${res.perplexity.toFixed(2)}</p>
        </div>
        <hr>
        <h6>Insights:</h6>
        <p class="small">${res.explanation}</p>
        <button onclick="window.print()" class="btn btn-sm btn-secondary mt-2">Export PDF</button>
    `;
}