import streamlit as st
import database as db

# 1. Page Configuration
st.set_page_config(
    page_title="AI Store Builder",
    page_icon="🛍️",
    layout="wide"
)

# 2. Session State Initialization
# This ensures the app remembers who is logged in while navigating pages
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# 3. Custom CSS for a Professional Look
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        transition: 0.3s;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        background-color: #45a049;
    }
    .welcome-text {
        font-size: 28px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 20px;
        text-align: center;
    }
    .store-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Aida.link")

 # 4. Authentication Logic (Login / Sign Up)
if not st.session_state['user_id']:
      # Create two tabs for a clean interface
      tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

      with tab1:
          with st.form("login_form"):
              st.subheader("Welcome Back")
              u = st.text_input("Username")
              p = st.text_input("Password", type="password")
              submit_login = st.form_submit_button("Login")

              if submit_login:
                  if u and p:
                      uid = db.verify_user(u, p)
                      if uid:
                          st.session_state['user_id'] = uid
                          st.session_state['username'] = u
                          st.success("Login successful! Redirecting...")
                          st.rerun()
                      else:
                          st.error("Invalid username or password")
                  else:
                      st.warning("Please enter both username and password")

      with tab2:
          with st.form("signup_form"):
              st.subheader("Create Your Account")
              u_new = st.text_input("Choose Username")
              p_new = st.text_input("Choose Password", type="password")
              t_new = st.selectbox("Account Type", ["Business", "Personal"])
              submit_signup = st.form_submit_button("Create Account")

              if submit_signup:
                  if u_new and p_new:
                      # This is where the 'account_type' error happened before
                      if db.add_user(u_new, p_new, t_new):
                          st.success("Account created successfully! Please go to the Login tab.")
                      else:
                          st.error("Username already taken. Please choose another one.")
                  else:
                      st.warning("Please fill in all fields")

  # 5. Main Application (What the user sees after logging in)
else:
      st.markdown(f'<div class="welcome-text">Welcome back, @{st.session_state["username"]}! 👋</div>', unsafe_allow_html=True)

      # Section: Featured Premium Stores
      st.subheader(" Featured Premium Stores")
      try:
          stores = db.get_all_premium_stores()
          if not stores:
              st.info("No premium stores to display yet. Upgrade your tier to be featured!")
          else:
              # Divide the page into 3 columns
              cols = st.columns(3)
              for i, s in enumerate(stores):
                  with cols[i % 3]:
                      # s[0]=store_name, s[1]=logo_path, s[2]=username
                      with st.container():
                          if s[1]:
                              st.image(s[1], width=100)
                          else:
                              st.write("🛍️") # Placeholder icon if no logo
                          st.markdown(f"**{s[0]}**")
                          st.caption(f"Created by @{s[2]}")
                          st.markdown("---")
      except Exception as e:
          st.error(f"Error loading premium stores: {e}")

      # Section: Navigation Buttons
      st.markdown("### 🛠️ Your Control Center")
      col1, col2 = st.columns(2)

      # Navigation to other pages (Ensure pages/1_dashboard.py and pages/2_my_store.py exist)
      if col1.button("🛠️ Open Dashboard"):
          st.switch_page("pages/1_dashboard.py")
      if col2.button("👁️ Preview My Store"):
          st.switch_page("pages/2_my_store.py")

  # 6. Sidebar for Global Settings
if st.session_state['user_id']:
      with st.sidebar:
          st.markdown("## ⚙️ User Settings")
          st.write(f"Logged in as: **@{st.session_state['username']}**")
          st.markdown("---")
          if st.button("Logout"):
              st.session_state['user_id'] = None
              st.session_state['username'] = None
              st.rerun()