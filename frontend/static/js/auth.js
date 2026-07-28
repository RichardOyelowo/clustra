let accessToken = null; // in memory only, never localStorage

export function setAccessToken(token) {
    accessToken = token;
}

export function getAccessToken() {
    return accessToken;
}

export async function refreshAccessToken() {
    const response = await fetch("/refresh", {
        method: "POST",
        credentials: "include",
    });
    if (!response.ok) {
        accessToken = null;
        return null;
    }
    const data = await response.json();
    accessToken = data.access_token;
    return accessToken;
}

export async function requireAuth() {
    if (accessToken) return accessToken;
    const token = await refreshAccessToken();
    if (!token) {
        window.location.href = "/login.html";
        return null;
    }
    return token;
}

export async function logout() {
    accessToken = null;
    await fetch("/logout", { method: "POST", credentials: "include" });
    window.location.href = "/login.html";
}

export async function authFetch(url, options = {}) {
    if (!accessToken) {
        await refreshAccessToken();
    }
    options.headers = { ...options.headers, Authorization: `Bearer ${accessToken}` };
    options.credentials = "include";

    let response = await fetch(url, options);

    if (response.status === 401) {
        const newToken = await refreshAccessToken();
        if (!newToken) {
            window.location.href = "/login.html";
            return response;
        }
        options.headers.Authorization = `Bearer ${newToken}`;
        response = await fetch(url, options);
    }

    return response;
}
