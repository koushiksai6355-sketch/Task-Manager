import streamlit as st
import requests

# Live Railway URL
BASE_URL = "https://task-manager-production-20a5.up.railway.app"

st.set_page_config(page_title="Team Task Manager", layout="wide")

# =========================
# SESSION STATE
# =========================
if "token" not in st.session_state:
    st.session_state.token = None

# =========================
# SIDEBAR NAV
# =========================
menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Signup", "Dashboard"]
)

# =========================
# SIGNUP
# =========================
if menu == "Signup":
    st.title("Create Account")
    name = st.text_input("Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    role = st.selectbox("Role", ["Admin", "Member"], key="signup_role")

    if st.button("Signup", key="signup_btn"):
        res = requests.post(
            f"{BASE_URL}/signup",
            json={"name": name, "email": email, "password": password, "role": role}
        )
        if res.status_code == 200:
            st.success("Signup successful! Head over to Login.")
        else:
            st.error(f"Signup Failed: {res.text}")

# =========================
# LOGIN
# =========================
elif menu == "Login":
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_btn"):
        res = requests.post(
            f"{BASE_URL}/login",
            json={"email": email, "password": password}
        )
        if res.status_code == 200:
            data = res.json()
            st.session_state.token = data.get("token")
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")

# =========================
# DASHBOARD
# =========================
elif menu == "Dashboard":
    if not st.session_state.token:
        st.warning("Please login first")
        st.stop()

    st.title("📊 Dashboard")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    tab1, tab2 = st.tabs(["📁 Projects", "📝 Tasks"])

    # =========================
    # PROJECTS TAB
    # =========================
    with tab1:
        st.subheader("Current Projects")
        
        # We fetch projects INSIDE the tab so they don't leak into the Task tab
        try:
            res = requests.get(f"{BASE_URL}/projects", headers=headers)
            if res.status_code == 200:
                projects = res.json()
                if projects:
                    for p in projects:
                        with st.expander(f"Project: {p['name']}"):
                            st.write(f"**Description:** {p.get('description', 'No description')}")
                            st.write(f"**ID:** `{p['id']}`")
                else:
                    st.info("No projects found.")
            else:
                st.error("Could not fetch projects.")
        except Exception as e:
            st.error(f"Connection Error: {e}")

        st.divider()
        st.markdown("### ➕ Create New Project")
        project_name = st.text_input("Project Name", key="new_proj_name")
        project_desc = st.text_area("Project Description", key="new_proj_desc")

        if st.button("Add Project", key="btn_add_project"):
            if project_name:
                r = requests.post(
                    f"{BASE_URL}/projects",
                    headers=headers,
                    json={"name": project_name, "description": project_desc}
                )
                if r.status_code == 200:
                    st.success("Project added successfully!")
                    st.rerun()
                else:
                    st.error(f"Error: {r.text}")
            else:
                st.warning("Project name is required.")

    # =========================
    # TASKS TAB
    # =========================
    with tab2:
        st.subheader("Your Tasks")
        
        try:
            res = requests.get(f"{BASE_URL}/tasks", headers=headers)
            if res.status_code == 200:
                tasks = res.json()
                if tasks:
                    st.table(tasks) # Tables are cleaner for lists of tasks
                else:
                    st.info("No tasks assigned yet.")
        except Exception as e:
            st.error(f"Connection Error: {e}")

        st.divider()
        st.markdown("### ➕ Create New Task")
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task Title", key="task_title")
            task_due = st.text_input("Due Date (YYYY-MM-DD)", key="task_due")
        with col2:
            task_project_id = st.number_input("Project ID", min_value=1, key="task_project_id")
            task_assigned_to = st.number_input("Assign User ID", min_value=1, key="task_assigned_to")
        
        task_desc = st.text_area("Task Description", key="task_desc")

        if st.button("Add Task", key="add_task"):
            r = requests.post(
                f"{BASE_URL}/tasks",
                headers=headers,
                json={
                    "title": task_title,
                    "description": task_desc,
                    "due_date": task_due,
                    "project_id": task_project_id,
                    "assigned_to": task_assigned_to
                }
            )
            if r.status_code == 200:
                st.success("Task added successfully")
                st.rerun()
            else:
                st.error(f"Failed to add task: {r.text}")
