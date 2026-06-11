import API from "./api.js";
import { requireAuth, logout } from "./auth.js";

async function init() {
    requireAuth();

    // fetch orgs and render
    const response = await API.get("/orgs");
    if (!response.ok) {
        console.error("Failed to fetch orgs")
        return
    }
    const orgs = await response.json();

    if (orgs.length >= 1) {
        const container = document.getElementById("orgs_card");
        const orgsList = document.createElement("ul");
        container.append(orgsList);

        for (const org of orgs) {
            const newElement = document.createElement("li");
            newElement.textContent = org.name;
            orgsList.append(newElement);
        }
    }

    const createOrg = document.getElementById("create_org_btn");
    createOrg.addEventListener("click", () => {
        console.log("create org clicked")
    })

    const logoutBtn = document.getElementById("logout_btn");
    logoutBtn.addEventListener("click", logout);
}

init();
