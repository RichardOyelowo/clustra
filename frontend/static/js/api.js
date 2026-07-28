import { getAccessToken, refreshAccessToken } from "./auth.js";

const API = {
    authHeaders() {
        return {
            Authorization: `Bearer ${getAccessToken()}`,
            "Content-Type": "application/json",
        };
    },
    async request(url, options = {}) {
        options.headers = { ...this.authHeaders(), ...options.headers };
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
    },
    async get(url) {
        return this.request(url);
    },
    async post(url, data) {
        return this.request(url, { method: "POST", body: JSON.stringify(data) });
    },
    async patch(url, data) {
        return this.request(url, { method: "PATCH", body: JSON.stringify(data) });
    },
    async delete(url) {
        if (!confirm("Are you sure? This action cannot be undone.")) {
            return new Response(null, { status: 499, statusText: "User Cancelled" });
        }
        return this.request(url, { method: "DELETE" });
    },
};

export default API;
