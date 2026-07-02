import { requireAuth } from './auth.js'
import { renderSidebar } from './sidebar.js'
import { getOrg, getTeams, getProjects } from './services.js'
import API from './api.js'

requireAuth()

const params = new URLSearchParams(window.location.search)
const orgId = params.get('org_id')

let currentOrg = null
let currentTeam = null
let currentProject = null
let allTeams = []
let allProjects = []

async function init() {
    const [org, teams] = await Promise.all([getOrg(orgId), getTeams(orgId)])

    if (!org || teams.length === 0) {
        console.error('failed to load org or no teams')
        return
    }

    currentOrg = org
    allTeams = teams
    currentTeam = teams[0]

    allProjects = await getProjects(orgId, currentTeam.id)

    if (allProjects.length === 0) {
        console.error('no projects in this team')
        return
    }

    currentProject = allProjects[0]

    await loadLabels()
}

async function loadLabels() {
    // TODO: fetch labels
    // hint: GET /orgs/{orgId}/teams/{teamId}/projects/{projId}/labels
    const labelsRes = await ___
    const labels = labelsRes.ok ? await labelsRes.json() : []

    renderSidebar({
        orgId,
        orgName: currentOrg.name,
        teamId: currentTeam.id,
        projectId: currentProject.id,
        activePage: 'labels',
        counts: {
            teams: allTeams.length,
            projects: allProjects.length,
            tasks: 0,
            milestones: 0
        },
        user: { initial: 'R', name: 'Richard', role: 'Team Lead' }
    })

    document.getElementById('breadcrumb_org_link').href = `/org.html?org_id=${orgId}`
    document.getElementById('breadcrumb_org_link').textContent = currentOrg.name

    document.getElementById('breadcrumb_team_link').href = `/teams.html?org_id=${orgId}&team_id=${currentTeam.id}`
    document.getElementById('breadcrumb_team_link').textContent = currentTeam.name

    document.getElementById('breadcrumb_project_link').href = `/project.html?org_id=${orgId}&team_id=${currentTeam.id}&proj_id=${currentProject.id}`
    document.getElementById('breadcrumb_project_link').textContent = currentProject.name

    renderLabels(labels)
}

function renderLabels(labels) {
    const tbody = document.getElementById('labels_tbody')

    if (labels.length === 0) {
        tbody.innerHTML = `<tr><td colspan="3" class="empty_state">No labels yet. Create one to tag tasks.</td></tr>`
        return
    }

    // NOTE: LabelResponse schema — check if it has a `color` field.
    // If not, you'll need to either add one to the backend, or default
    // to a fixed color here for now (e.g. var(--primary)).
    tbody.innerHTML = labels.map(label => `
        <tr data-label-id="${label.id}">
            <td>
                <span class="label_chip" style="background: ${___}20; color: ${___};">
                    <span class="label_dot" style="background: ${___};"></span>
                    ${___}
                </span>
            </td>
            <td class="task_count">—</td>
            <td><button class="action_btn" data-delete-id="${label.id}">Delete</button></td>
        </tr>
    `).join('')

    tbody.querySelectorAll('[data-delete-id]').forEach(btn => {
        btn.addEventListener('click', async () => {
            const labelId = btn.dataset.deleteId
            // TODO: DELETE the label, then reload
            ___
        })
    })
}

// ── new label modal ──
const newLabelModal = document.getElementById('new_label_modal')
const newLabelForm = document.getElementById('new_label_form')

document.getElementById('new_label_btn').addEventListener('click', () => {
    newLabelModal.classList.remove('hidden')
})
document.getElementById('cancel_label_btn').addEventListener('click', () => {
    newLabelModal.classList.add('hidden')
})

newLabelForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    const formData = new FormData(newLabelForm)

    const payload = {
        name: formData.get('name'),
        // color: formData.get('color')  // only include if your LabelCreate schema supports it
    }

    // TODO: POST new label, close modal, reload
    ___
})

init()
