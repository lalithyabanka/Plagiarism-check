# Plagiarism-check
we are creating an online website.
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plagiarism Detection Platform</title>
</head>
<body>
    <h1>Plagiarism Detection Platform</h1>
    <form id="upload-form" enctype="multipart/form-data">
        <label for="file-input">Upload a file:</label>
        <input type="file" id="file-input" name="file" accept=".txt,.doc,.docx,.pdf"><br><br>
        <label for="text-input">Or paste your text here:</label><br>
        <textarea id="text-input" name="text" rows="10" cols="50"></textarea><br><br>
        <button type="submit">Check for Plagiarism</button>
    </form>
    <div id="report-section" style="display: none;">
        <h2>Similarity Report</h2>
        <div id="report-output"></div>
    </div>

    <script>
        document.getElementById('upload-form').addEventListener('submit', async function (event) {
            event.preventDefault();
            const formData = new FormData();

            const fileInput = document.getElementById('file-input').files[0];
            const textInput = document.getElementById('text-input').value;

            if (fileInput) {
                formData.append('file', fileInput);
            } else if (textInput.trim()) {
                formData.append('text', textInput);
            } else {
                alert('Please upload a file or enter text.');
                return;
            }

            try {
                const response = await fetch('/api/check-plagiarism', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();

                document.getElementById('report-section').style.display = 'block';
                document.getElementById('report-output').innerHTML = `
                    <h3>Similarity Score: ${result.similarityScore}%</h3>
                    <p>${result.details}</p>
                    <h4>Sources:</h4>
                    <ul>
                        ${result.sources.map(source => `<li>${source}</li>`).join('')}
                    </ul>
                `;
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to check for plagiarism. Please try again later.');
            }
        });
    </script>
</body>
</html>
