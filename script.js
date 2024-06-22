document.getElementById('dietForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const condition = document.getElementById('condition').value;
    const recommendationsDiv = document.getElementById('recommendations');
    const summaryDiv = document.getElementById('summary');

    // Clear previous results
    recommendationsDiv.innerHTML = '';
    summaryDiv.innerHTML = '';

    // Fetch recommendations from the backend
    try {
        const response = await fetch('http://localhost:5000/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ condition }),
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        recommendationsDiv.innerHTML = `<h2>Diet recommendations for ${condition}:</h2><p>${data.recommendations}</p>`;
        summaryDiv.innerHTML = `<h2>Summary from GPT:</h2><p>${data.gpt_response}</p>`;
    } catch (error) {
        recommendationsDiv.innerHTML = `<p>Error fetching recommendations: ${error.message}</p>`;
    }
});
