import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# REQUEST SESSION
# ============================================================

# This prevents Windows/system proxy settings from interfering
# with communication between Streamlit and local FastAPI.

session = requests.Session()
session.trust_env = False


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FCMB Attendance",
    page_icon="🏦",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "staff_id" not in st.session_state:
    st.session_state.staff_id = None

if "staff_name" not in st.session_state:
    st.session_state.staff_name = None

if "page" not in st.session_state:
    st.session_state.page = "login"


# ============================================================
# SAFE RESPONSE FUNCTION
# ============================================================

def get_response_data(response):

    try:

        return response.json()

    except ValueError:

        text = response.text.strip()

        return {
            "detail": text
            if text
            else "FastAPI returned an empty response."
        }


# ============================================================
# FASTAPI CONNECTION TEST
# ============================================================

def check_api():

    try:

        response = session.get(
            f"{API_URL}/",
            timeout=5
        )

        return response.status_code == 200

    except requests.exceptions.RequestException:

        return False


# ============================================================
# LOGIN PAGE
# ============================================================

def login():

    st.title("FCMB Attendance")

    st.subheader("Staff Login")

    st.write(
        "Sign in to access the FCMB attendance system."
    )

    st.divider()

    email = st.text_input(
        "Email",
        placeholder="Enter your FCMB email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    st.write("")

    if st.button(
        "LOGIN",
        use_container_width=True
    ):

        if not email:

            st.warning(
                "Please enter your email."
            )

            return

        if not password:

            st.warning(
                "Please enter your password."
            )

            return

        try:

            response = session.post(

                f"{API_URL}/auth/login",

                json={
                    "email": email,
                    "password": password
                },

                timeout=10
            )

            data = get_response_data(response)

            # =================================================
            # SUCCESS
            # =================================================

            if response.status_code == 200:

                # Our Streamlit application needs the JWT.
                if "access_token" not in data:

                    st.error(
                        "Login succeeded, but FastAPI "
                        "did not return an access token."
                    )

                    st.write(
                        "FastAPI response:"
                    )

                    st.json(data)

                    return

                # Save JWT
                st.session_state.token = (
                    data["access_token"]
                )

                # Save staff information
                st.session_state.staff_id = (
                    data.get("staff_id")
                )

                st.session_state.staff_name = (
                    data.get(
                        "name",
                        "Staff"
                    )
                )

                # Move to dashboard
                st.session_state.page = "dashboard"

                st.success(
                    "Login successful!"
                )

                st.rerun()

            # =================================================
            # LOGIN FAILED
            # =================================================

            else:

                st.error(
                    f"Login failed "
                    f"(HTTP {response.status_code})"
                )

                st.warning(
                    data.get(
                        "detail",
                        "Invalid email or password."
                    )
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI."
            )

            st.info(
                "Make sure FastAPI is running at:"
            )

            st.code(API_URL)

        except requests.exceptions.Timeout:

            st.error(
                "❌ FastAPI took too long to respond."
            )

        except Exception as e:

            st.error(
                f"❌ Unexpected error: {e}"
            )


# ============================================================
# CREATE ACCOUNT PAGE
# ============================================================

def create_account():

    st.title("FCMB Attendance")

    st.subheader("Create Staff Account")

    st.write(
        "Register a new staff account."
    )

    st.divider()

    # =========================================================
    # STAFF INFORMATION
    # =========================================================

    staff_id = st.text_input(
        "Staff ID",
        placeholder="e.g. NET001"
    )

    first_name = st.text_input(
        "First Name",
        placeholder="e.g. Abdul"
    )

    last_name = st.text_input(
        "Last Name",
        placeholder="e.g. Suleiman"
    )

    email = st.text_input(
        "Email",
        placeholder="e.g. abdul@fcmb.com"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )

    # =========================================================
    # DEPARTMENT
    # =========================================================

    department = st.text_input(
        "Department",
        placeholder="e.g. Software"
    )

    # =========================================================
    # ROLE
    # =========================================================

    role = st.text_input(
        "Role",
        placeholder="e.g. Frontend"
    )

    st.write("")

    # =========================================================
    # CREATE ACCOUNT
    # =========================================================

    if st.button(
        "CREATE ACCOUNT",
        use_container_width=True
    ):

        # -----------------------------------------------------
        # VALIDATION
        # -----------------------------------------------------

        if not staff_id.strip():

            st.warning(
                "Please enter Staff ID."
            )

            return

        if not first_name.strip():

            st.warning(
                "Please enter first name."
            )

            return

        if not last_name.strip():

            st.warning(
                "Please enter last name."
            )

            return

        if not email.strip():

            st.warning(
                "Please enter email."
            )

            return

        if not password:

            st.warning(
                "Please enter password."
            )

            return

        if not department.strip():

            st.warning(
                "Please enter department."
            )

            return

        if not role.strip():

            st.warning(
                "Please enter role."
            )

            return

        # -----------------------------------------------------
        # SEND TO FASTAPI
        # -----------------------------------------------------

        try:

            response = session.post(

                f"{API_URL}/staff/",

                json={

                    "staff_id": staff_id.strip(),

                    "first_name": first_name.strip(),

                    "last_name": last_name.strip(),

                    "email": email.strip(),

                    "password": password,

                    "department": department.strip(),

                    "role": role.strip()

                },

                timeout=10
            )

            data = get_response_data(
                response
            )

            # -------------------------------------------------
            # SUCCESS
            # -------------------------------------------------

            if response.status_code in [200, 201]:

                st.success(
                    "✅ Account created successfully!"
                )

                st.info(
                    "You can now login with your "
                    "email and password."
                )

            # -------------------------------------------------
            # ERROR
            # -------------------------------------------------

            else:

                st.error(
                    f"Account creation failed "
                    f"(HTTP {response.status_code})"
                )

                st.warning(
                    data.get(
                        "detail",
                        "Could not create account."
                    )
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI."
            )

            st.info(
                "Make sure FastAPI is running at:"
            )

            st.code(
                API_URL
            )

        except requests.exceptions.Timeout:

            st.error(
                "❌ FastAPI took too long to respond."
            )

        except Exception as e:

            st.error(
                f"❌ Unexpected error: {e}"
            )

    # =========================================================
    # BACK TO LOGIN
    # =========================================================

    st.divider()

    if st.button(
        "Already have an account? Login",
        use_container_width=True
    ):

        st.session_state.page = "login"

        st.rerun()

# ============================================================
# SIGN IN
# ============================================================

def sign_in():

    # Make sure user is actually logged in
    if not st.session_state.token:

        st.error(
            "You are not logged in."
        )

        return

    try:

        response = session.post(

            f"{API_URL}/attendance/sign-in",

            headers={
                "Authorization":
                f"Bearer {st.session_state.token}"
            },

            timeout=10
        )

        data = get_response_data(response)

        # =================================================
        # SUCCESS
        # =================================================

        if response.status_code == 200:

            st.success(
                data.get(
                    "message",
                    "Sign-in successful."
                )
            )

            if data.get("sign_in_time"):

                st.write(
                    "Sign-in time:",
                    data["sign_in_time"]
                )

        # =================================================
        # ERROR
        # =================================================

        else:

            st.error(
                f"Sign-in failed "
                f"(HTTP {response.status_code})"
            )

            st.warning(
                data.get(
                    "detail",
                    "Unable to sign in."
                )
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI."
        )

    except requests.exceptions.Timeout:

        st.error(
            "❌ FastAPI took too long to respond."
        )

    except Exception as e:

        st.error(
            f"❌ Unexpected error: {e}"
        )


# ============================================================
# SIGN OUT
# ============================================================

def sign_out():

    if not st.session_state.token:

        st.error(
            "You are not logged in."
        )

        return

    try:

        response = session.post(

            f"{API_URL}/attendance/sign-out",

            headers={
                "Authorization":
                f"Bearer {st.session_state.token}"
            },

            timeout=10
        )

        data = get_response_data(response)

        # =================================================
        # SUCCESS
        # =================================================

        if response.status_code == 200:

            st.success(
                data.get(
                    "message",
                    "Sign-out successful."
                )
            )

            if data.get("sign_out_time"):

                st.write(
                    "Sign-out time:",
                    data["sign_out_time"]
                )

        # =================================================
        # ERROR
        # =================================================

        else:

            st.error(
                f"Sign-out failed "
                f"(HTTP {response.status_code})"
            )

            st.warning(
                data.get(
                    "detail",
                    "Unable to sign out."
                )
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI."
        )

    except requests.exceptions.Timeout:

        st.error(
            "❌ FastAPI took too long to respond."
        )

    except Exception as e:

        st.error(
            f"❌ Unexpected error: {e}"
        )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    st.title("FCMB Attendance")

    st.success(
        f"Welcome, {st.session_state.staff_name}"
    )

    st.write(
        f"**Staff ID:** "
        f"{st.session_state.staff_id}"
    )

    st.divider()

    # ========================================================
    # ATTENDANCE
    # ========================================================

    st.subheader(
        "Attendance"
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # SIGN IN
    # --------------------------------------------------------

    with col1:

        if st.button(
            "🟢 SIGN IN",
            use_container_width=True
        ):

            sign_in()

    # --------------------------------------------------------
    # SIGN OUT
    # --------------------------------------------------------

    with col2:

        if st.button(
            "🔴 SIGN OUT",
            use_container_width=True
        ):

            sign_out()

    st.divider()

    # ========================================================
    # LOGOUT
    # ========================================================

    if st.button(
        "LOGOUT",
        use_container_width=True
    ):

        st.session_state.token = None

        st.session_state.staff_id = None

        st.session_state.staff_name = None

        st.session_state.page = "login"

        st.rerun()


# ============================================================
# MAIN APPLICATION
# ============================================================

if st.session_state.page == "login":

    login()

    st.divider()

    if st.button(
        "Create New Account",
        use_container_width=True
    ):

        st.session_state.page = "create_account"

        st.rerun()


elif st.session_state.page == "create_account":

    create_account()


elif st.session_state.page == "dashboard":

    dashboard()