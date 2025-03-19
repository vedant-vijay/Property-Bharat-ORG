document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value.trim();

    // Basic Validation
    if (username === "" || password === "") {
        alert("Please enter your username and password.");
        return;
    }

    // Send login data to Flask backend
    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json()) // Parse the response as JSON
    .then(data => {
        if (data.success) {
            alert("✅ Login Successful!");
            window.location.href = "/dashboard"; // Redirect to dashboard via Flask
        } else {
            alert("❌ Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("❌ Something went wrong. Please try again.");
    });
});
