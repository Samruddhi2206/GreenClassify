document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("upload-form");
    const resultDiv = document.getElementById("result");

    form.addEventListener("submit", async function(e) {
        e.preventDefault();
        const fileInput = document.getElementById("imageInput");

        if (!fileInput.files.length) {
            alert("Please select an image file.");
            return;
        }

        const formData = new FormData();
        formData.append("image", fileInput.files[0]);
        resultDiv.innerHTML = `<p>Processing...</p>`;

        try { // main.js

            // Smooth scroll for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener("click", function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute("href"));
                    if (target) {
                        target.scrollIntoView({ behavior: "smooth", block: "start" });
                    }
                });
            });

            // Display preview image on upload
            document.addEventListener("DOMContentLoaded", () => {
                const input = document.getElementById("imageInput");
                const result = document.getElementById("result");

                if (input) {
                    input.addEventListener("change", function() {
                        if (this.files && this.files[0]) {
                            const reader = new FileReader();
                            reader.onload = function(e) {
                                result.innerHTML = `<p>Image Preview:</p><img src="${e.target.result}" class="img-fluid rounded" style="max-height: 300px;" />`;
                            };
                            reader.readAsDataURL(this.files[0]);
                        }
                    });
                }
            });

            const res = await fetch("/predict", {
                method: "POST",
                body: formData,
            });
            const data = await res.json();

            if (res.ok) {
                resultDiv.innerHTML = `
                    <h3 class="result-text">${data.predicted_class}</h3>
                    <p>Confidence: ${(data.confidence * 100).toFixed(2)}%</p>
                    <img class="image-preview" src="data:image/jpeg;base64,${data.image}" />
                `;
            } else {
                resultDiv.innerHTML = `<p class="text-danger">${data.error}</p>`;
            }
        } catch (error) {
            resultDiv.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
        }
    });
});