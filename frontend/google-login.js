document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  if (!token) {
    // Initialize Google Sign-in
    google.accounts.id.initialize({
      client_id: "274333479323-h9ekpt485olvrf0ranojadnonorhf7t5.apps.googleusercontent.com",
      callback: handleGoogleLogin,
    });

    // Render the button
    google.accounts.id.renderButton(
      document.getElementById("googleBtn"),
      { theme: "outline", size: "large" }
    );
  }
});

function handleGoogleLogin(response) {
  fetch("http://127.0.0.1:5000/api/auth/google-login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ credential: response.credential }),
  })
    .then(res => res.json())
    .then(data => {
      if (data.token) {
        localStorage.setItem("token", data.token);
        window.location.reload(); // Reload to show Todo UI
      } else {
        alert("Google login failed!");
      }
    })
    .catch(err => {
      console.error("Google Login Error:", err);
    });
}
