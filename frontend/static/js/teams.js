import { requireAuth, logout } from "./auth.js"
import { renderSidebar } from ". /sidebar.js"
import API from "./api.js"


requireAuth()

const params = new URLSearchParams(window.location.search)
const orgId = params.get("org_id")

function init() {

}

init()
