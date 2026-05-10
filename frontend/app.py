import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

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
    password = st.text_input(
        "Password",
        type="password",
        key="signup_password"
    )

    role = st.selectbox(
        "Role",
        ["Admin", "Member"],
        key="signup_role"
    )

    if st.button("Signup", key="signup_btn"):

        res = requests.post(
            f"{BASE_URL}/signup",
            json={
                "name": name,
                "email": email,
                "password": password,
                "role": role
            }
        )

        if res.status_code == 200:
            st.success("Signup successful")
        else:
            st.error(res.text)

# =========================
# LOGIN
# =========================
elif menu == "Login":

    st.title("Login")

    email = st.text_input("Email", key="login_email")

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login", key="login_btn"):

        res = requests.post(
            f"{BASE_URL}/login",
            json={
                "email": email,
                "password": password
            }
        )

        if res.status_code == 200:

            data = res.json()

            st.session_state.token = data["token"]

            st.success("Login successful")

        else:
            st.error(res.text)

# =========================
# DASHBOARD
# =========================
elif menu == "Dashboard":

    if not st.session_state.token:
        st.warning("Please login first")
        st.stop()

    st.title("📊 Dashboard")

    # TOKEN HEADER
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    tab1, tab2 = st.tabs(["Projects", "Tasks"])

    # =========================
    # PROJECTS TAB
    # =========================
    with tab1:
        st.subheader("Projects")

    res = requests.get(
        f"{BASE_URL}/projects",
        headers=headers
    )

    projects = res.json()

    # DISPLAY PROJECTS
    if projects:
        for p in projects:
            st.markdown(f"""
            ### 📁 {p['name']}
            📝 {p['description']}
            🆔 Project ID: {p['id']}
            ---
            """)
    else:
        st.info("No projects found")

    st.markdown("## Create Project")

    # Use unique keys for inputs to avoid conflicts
    project_name = st.text_input("Project Name", key="new_proj_name")
    project_desc = st.text_input("Project Description", key="new_proj_desc")

    # This is the ONLY 'Add Project' button allowed in this section
    if st.button("Add Project", key="btn_add_project_unique"):
        if not project_name:
            st.warning("Please provide a project name.")
        else:
            r = requests.post(
                f"{BASE_URL}/projects",
                headers=headers,
                json={
                    "name": project_name,
                    "description": project_desc
                }
            )

            # Check status code BEFORE accessing json to avoid KeyError
            if r.status_code == 200:
                # .get() is a safety net; if "message" is missing, it won't crash
                msg = r.json().get("message", "Project added successfully!")
                st.success(msg)
                st.rerun()
            else:
                # If backend fails, show the actual error message or status
                st.error(f"Backend Error ({r.status_code}): {r.text}")

    # =========================
    # TASKS TAB
    # =========================
    with tab2:

        st.subheader("Tasks")

        # GET TASKS
        res = requests.get(
            f"{BASE_URL}/tasks",
            headers=headers
        )

        tasks = res.json()

        st.write(tasks)

        st.markdown("### Create Task")

        task_title = st.text_input(
            "Task Title",
            key="task_title"
        )

        task_desc = st.text_input(
            "Task Description",
            key="task_desc"
        )

        task_due = st.text_input(
            "Due Date (YYYY-MM-DD)",
            key="task_due"
        )

        task_project_id = st.number_input(
            "Project ID",
            min_value=1,
            key="task_project_id"
        )

        task_assigned_to = st.number_input(
            "Assign User ID",
            min_value=1,
            key="task_assigned_to"
        )

        # ADD TASK
        if st.button("Add Task", key="add_task"):

            r = requests.post(
                f"{BASE_URL}/tasks",
                json={
                    "title": task_title,
                    "description": task_desc,
                    "due_date": task_due,
                    "project_id": task_project_id,
                    "assigned_to": task_assigned_to
                },
                headers=headers
            )

            if r.status_code == 200:
                st.success("Task added successfully")
                st.rerun()
            else:
                st.error(r.text)