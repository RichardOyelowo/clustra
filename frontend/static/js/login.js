const form = document.getElementById("login_form");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = form.email.value;
    const password = form.password.value;

    const body = new URLSearchParams();
    body.append("username", email);
    body.append("password", password);

    const response = await fetch("/login", {
        method: "POST",
        body: body,
    });

    const data = await response.json();
    if (!response.ok) {
        console.error("Login Failed", data)
        return
    }

    localStorage.setItem("token", data.access_token);
    window.location.href = "../orgs.html";
});
