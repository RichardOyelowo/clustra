import API from "./api.js";
import { requireAuth, logout } from "./auth.js";

requireAuth();

// load all orgs
async function loadOrgs() {
    const response = await API.get("/orgs");
    if (!response.ok) {
        console.error("Failed to fetch orgs");
        return;
    }
    const orgs = await response.json();
    const container = document.getElementById("orgs_card");
    container.innerHTML = "";

    if (orgs.length >= 1) {
        const orgsList = document.createElement("ul");
        container.append(orgsList);
        for (const org of orgs) {
            const newElement = document.createElement("li");
            newElement.textContent = org.name;
            orgsList.append(newElement);
        }
    }
}

// hidden hides the tag content
const createOrg = document.getElementById("create_org_btn");
createOrg.addEventListener("click", () => {
    document.getElementById("create_org_modal").classList.remove("hidden");
});

const cancelBtn = document.getElementById("cancel_btn");
cancelBtn.addEventListener("click", () => {
    document.getElementById("create_org_modal").classList.add("hidden");
});

// form submission to endpoint
const form = document.getElementById("create_org_form");
form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const body = {
        name: form.name.value,
        slug: form.slug.value,
        desc: form.desc.value,
    };
    const response = await API.post("/orgs", body);
    if (!response.ok) {
        console.error("failed to create org", await response.json());
        return;
    }
    document.getElementById("create_org_modal").classList.add("hidden");
    form.reset();

    // updates orgs
    await loadOrgs();
});

const logoutBtn = document.getElementById("logout_btn");
logoutBtn.addEventListener("click", logout);

await loadOrgs()

