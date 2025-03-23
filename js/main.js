document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultDiv = document.getElementById('result');
    const predictionText = document.getElementById('prediction');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('error-message');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Hide any previous results or errors
        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
        
        // Show loading spinner
        loadingDiv.classList.remove('hidden');

        // Get form values
        const age = parseInt(document.getElementById('age').value);
        const bmi = parseFloat(document.getElementById('bmi').value);
        const children = parseInt(document.getElementById('children').value);
        const smoker = parseInt(document.querySelector('input[name="smoker"]:checked').value);

        // Validate inputs
        if (age < 0 || age > 120) {
            showError('Age must be between 0 and 120');
            return;
        }
        if (bmi < 10 || bmi > 50) {
            showError('BMI must be between 10 and 50');
            return;
        }
        if (children < 0 || children > 10) {
            showError('Number of children must be between 0 and 10');
            return;
        }

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    age: age,
                    bmi: bmi,
                    children: children,
                    smoker: smoker
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Show prediction
                predictionText.textContent = `$${data.prediction.toLocaleString()}`;
                resultDiv.classList.remove('hidden');
            } else {
                // Show error message
                showError(data.error || 'An error occurred while making the prediction');
            }
        } catch (error) {
            showError('Failed to connect to the server. Please try again.');
        } finally {
            // Hide loading spinner
            loadingDiv.classList.add('hidden');
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorDiv.classList.remove('hidden');
        loadingDiv.classList.add('hidden');
    }

    // Add input validation for real-time feedback
    const inputs = form.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const min = parseFloat(this.min);
            const max = parseFloat(this.max);
            
            if (value < min || value > max) {
                this.classList.add('border-red-500');
                this.classList.remove('border-gray-300');
            } else {
                this.classList.remove('border-red-500');
                this.classList.add('border-gray-300');
            }
        });
    });
});