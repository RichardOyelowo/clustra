const form = document.getElementById("signup_form");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = form.email.value;
    const username = form.username.value;
    const plain_password = form.password.value;

    const response = await fetch("/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: email,
            username: username,
            plain_password: plain_password,
        }),
    });

    const data = await response.json();

    if (!response.ok) {
        console.error("SignUp failed", data);
        return;
    }

    const loginBody = new URLSearchParams();
    loginBody.append("username", email);
    loginBody.append("password", plain_password);

    const loginResponse = await fetch("/login", {
        method: "POST",
        body: loginBody,
    });
    const loginData = await loginResponse.json();

    if (!loginResponse.ok) {
        console.error("Login Failed", loginData);
    }

    localStorage.setItem("token", loginData.access_token);
    window.location.href = "/orgs.html";
});
