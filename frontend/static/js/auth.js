export function requireAuth() {
    const token = localStorage.getItem("token")
    if (!token) {
        window.location.href = "/login.html"
    }
    return token
}

export function logout() {
    localStorage.removeItem("token")
    window.location.href = "/login.html"
}
