import API from "./api.js";
import { requireAuth, logout } from "./auth.js";

requireAuth();

const DOM = {
    orgsContainer: document.getElementById("orgs_card"),
    createOrgModal: document.getElementById("create_org_modal"),
    createOrgBtn: document.getElementById("create_org_btn"),
    cancelBtn: document.getElementById("cancel_btn"),
    logoutBtn: document.getElementById("logout_btn"),
};

// load all orgs
async function loadOrgs() {
    const response = await API.get("/orgs");

    if (!response.ok) {
        console.error("Failed to fetch orgs");
        return;
    }
    const orgs = await response.json();
    DOM.orgsContainer.innerHTML = "";

    if (orgs.length >= 1) {
        const orgsList = document.createElement("ul");
        DOM.orgsContainer.append(orgsList);

        for (const org of orgs) {
            const li = document.createElement("li");

            const name = document.createElement("div");
            name.className = "org_name";
            name.textContent = org.name;

            const desc = document.createElement("p");
            desc.className = "org_desc";
            desc.textContent = org.desc || "";

            li.append(name, desc);

            li.addEventListener("click", () => {
                window.location.href = `/org.html?org_id=${org.id}`;
            });

            // keyboard accessibility
            li.setAttribute("tabindex", "0");
            li.addEventListener("keydown", (e) => {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault()
                    window.location.href = `/org.html?org_id=${org.id}`;
                }
            });

            orgsList.append(li);
        }
    }
}

// open modal
DOM.createOrgBtn.addEventListener("click", () => {
    DOM.createOrgModal.classList.remove("hidden");
});

// close modal
DOM.cancelBtn.addEventListener("click", () => {
    DOM.createOrgModal.classList.add("hidden");
});

// form submission to endpoint
document.getElementById("create_org_form").addEventListener("submit", async function (e) {
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

    DOM.createOrgModal.classList.add("hidden");
    form.reset();

    // update orgs after creating a new one
    await loadOrgs();
});

// logout
DOM.logoutBtn.addEventListener("click", logout);

// initial page load
await loadOrgs();
