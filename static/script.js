async function analyzeCV() {
    const cvText = document.getElementById('cvInput').value.trim();
    if (!cvText) {
        alert("CV metni girin!");
        return;
    }

    document.getElementById('results').innerHTML = "<p>Analiz ediliyor...</p>";

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: 'cv_text=' + encodeURIComponent(cvText)
        });

        const data = await response.json();

        document.getElementById('results').innerHTML = `
            <h2>Almanya Uyum Skorun: <strong style="color:#00ff88; font-size:48px;">${data.match_score}%</strong></h2>
            <p><strong>Bulunan beceriler:</strong> ${data.user_skills.join(', ')}</p>
            <p><strong>En çok arananlar:</strong> ${data.top_skills.join(', ')}</p>
            <h3 style="color:#00ff88;">
                ${data.match_score >= 80 ? 'TEBRİKLER! Almanya seni bekliyor!' : 
                  data.match_score >= 60 ? 'Çok iyisin, son dokunuş kaldı!' : 
                  'Biraz daha çalış, çok yakında hazır olacaksın!'}
            </h3>
        `;
    } catch (err) {
        document.getElementById('results').innerHTML = `<p style="color:red">Hata: ${err.message}</p>`;
    }
}