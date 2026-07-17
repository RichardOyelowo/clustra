const API = {
    getToken() {
        return localStorage.getItem("token");
    },

    authHeaders() {
        return {
            Authorization: `Bearer ${this.getToken()}`,
            "Content-Type": "application/json",
        };
    },

    async get(url) {
        const response = await fetch(url, {
            headers: this.authHeaders(),
        });
        return response;
    },

    async post(url, data) {
        const response = await fetch(url, {
            method: "POST",
            headers: this.authHeaders(),
            body: JSON.stringify(data),
        });
        return response;
    },

    async patch(url, data) {
        const response = await fetch(url, {
            method: "PATCH",
            headers: this.authHeaders(),
            body: JSON.stringify(data),
        });
        return response;
    },

    async delete(url) {
        if (!confirm("Are you sure? This action cannot be undone.")) {
            return new Response(null, {
                status: 499,
                statusText: "User Cancelled",
            });
        }

        const response = await fetch(url, {
            method: "DELETE",
            headers: this.authHeaders(),
        });
        return response;
    },
};

export default API
