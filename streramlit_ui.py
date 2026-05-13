import os
import streamlit as st
from pathlib import Path


# ─── Page config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="File Manager — CRUD",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace; }

/* Background */
.stApp { background: #1e1e2e; color: #cdd6f4; }

/* Sidebar */
section[data-testid="stSidebar"] { background: #2a2a3e !important; }
section[data-testid="stSidebar"] * { color: #cdd6f4 !important; }

/* Inputs */
input, textarea, .stTextInput input, .stTextArea textarea {
    background: #313244 !important;
    color: #cdd6f4 !important;
    border: 1px solid #45475a !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Buttons */
.stButton > button {
    background: #7c6af7 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    padding: 0.5rem 1.2rem !important;
    transition: opacity 0.15s;
}
.stButton > button:hover { opacity: 0.85; }

/* Radio */
.stRadio label { color: #cdd6f4 !important; }

/* Tabs */
.stTabs [role="tab"] {
    background: #2a2a3e !important;
    color: #6c7086 !important;
    border-radius: 6px 6px 0 0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
}
.stTabs [aria-selected="true"] {
    background: #7c6af7 !important;
    color: white !important;
}

/* Dataframe / table */
.stDataFrame { background: #313244 !important; }

/* Metric */
[data-testid="metric-container"] {
    background: #2a2a3e;
    border-radius: 10px;
    padding: 12px 18px;
    border-left: 4px solid #7c6af7;
}
[data-testid="metric-container"] label { color: #6c7086 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #cdd6f4 !important; }

/* Alerts */
.stSuccess { background: #1e3a2e !important; border-color: #a6e3a1 !important; color: #a6e3a1 !important; }
.stError   { background: #3a1e1e !important; border-color: #f38ba8 !important; color: #f38ba8 !important; }
.stWarning { background: #3a2e1e !important; border-color: #fab387 !important; color: #fab387 !important; }
.stInfo    { background: #1e2a3a !important; border-color: #89b4fa !important; color: #89b4fa !important; }

/* Code block */
code { background: #313244 !important; color: #a6e3a1 !important; }
pre  { background: #313244 !important; }

/* Select box */
.stSelectbox [data-baseweb="select"] > div {
    background: #313244 !important;
    border-color: #45475a !important;
    color: #cdd6f4 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Core CRUD Logic ─────────────────────────────────────────────────────────

def get_all_items():
    p = Path("")
    return list(p.rglob("*"))

def read_file(file_name):
    p = Path(file_name)
    if p.exists() and p.is_file():
        with open(file_name, "r") as f:
            return f.read()
    return None

def create_file_op(file_name, content):
    p = Path(file_name)
    if p.exists():
        return False, "File already exists."
    with open(file_name, "w") as f:
        f.write(content)
    return True, f"File **{file_name}** created successfully."

def update_file(file_name, content, mode="w"):
    p = Path(file_name)
    if not p.exists():
        return False, "File does not exist."
    with open(file_name, mode) as f:
        f.write("\n" + content)
    return True, f"File **{file_name}** updated successfully."

def delete_file(file_name):
    p = Path(file_name)
    if not p.exists():
        return False, "File does not exist."
    os.remove(p)
    return True, f"File **{file_name}** deleted successfully."

def rename_file(old_name, new_name):
    p = Path(old_name)
    if not p.exists():
        return False, "File does not exist."
    p.rename(new_name)
    return True, f"Renamed **{old_name}** → **{new_name}** successfully."

def create_folder_op(folder_name):
    p = Path(folder_name)
    if p.exists():
        return False, "Folder already exists."
    p.mkdir()
    return True, f"Folder **{folder_name}** created successfully."

def remove_folder(folder_name):
    p = Path(folder_name)
    if not p.exists():
        return False, "Folder does not exist."
    p.rmdir()
    return True, f"Folder **{folder_name}** removed successfully."


# ─── Sidebar — Explorer ──────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📁 File Explorer")
    if st.button("🔄  Refresh", use_container_width=True):
        st.rerun()

    items = get_all_items()
    files   = [i for i in items if i.is_file()]
    folders = [i for i in items if i.is_dir()]

    col1, col2 = st.columns(2)
    col1.metric("Files",   len(files))
    col2.metric("Folders", len(folders))

    st.markdown("---")

    if items:
        st.markdown("### All Items")
        for item in items:
            icon = "📄" if item.is_file() else "📂"
            st.markdown(f"`{icon}  {item}`")
    else:
        st.info("No items found in current directory.")


# ─── Header ──────────────────────────────────────────────────────────────────

st.markdown("# 📁 File Manager")
st.markdown("<span style='color:#6c7086;font-size:14px;'>CRUD Operations — Create · Read · Update · Delete</span>",
            unsafe_allow_html=True)
st.markdown("---")


# ─── Tabs ────────────────────────────────────────────────────────────────────

tab_create, tab_read, tab_update, tab_delete, tab_rename, tab_folder = st.tabs([
    "➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete", "🔤 Rename", "📂 Folder"
])


# ── Create ───────────────────────────────────────────────────────────────────

with tab_create:
    st.subheader("Create a New File")
    c1, c2 = st.columns([1, 2])
    with c1:
        create_name = st.text_input("File name", placeholder="e.g. notes.txt", key="cn")
    with c2:
        st.write("")   # spacing
    create_content = st.text_area("File content", height=180, key="cc",
                                   placeholder="Type the file content here…")
    if st.button("Create File", key="btn_create"):
        if not create_name:
            st.error("Please enter a file name.")
        else:
            ok, msg = create_file_op(create_name, create_content)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()


# ── Read ─────────────────────────────────────────────────────────────────────

with tab_read:
    st.subheader("Read a File")
    read_name = st.text_input("File name", placeholder="e.g. notes.txt", key="rn")
    if st.button("Read File", key="btn_read"):
        if not read_name:
            st.error("Please enter a file name.")
        else:
            content = read_file(read_name)
            if content is not None:
                st.success(f"Loaded **{read_name}**")
                st.code(content, language="text")
            else:
                st.error("File not found.")


# ── Update ───────────────────────────────────────────────────────────────────

with tab_update:
    st.subheader("Update a File")
    update_name = st.text_input("File name", placeholder="e.g. notes.txt", key="un")

    col_load, _ = st.columns([1, 3])
    with col_load:
        load_clicked = st.button("Load Current Content", key="btn_load")

    existing = ""
    if load_clicked:
        if not update_name:
            st.error("Please enter a file name.")
        else:
            existing = read_file(update_name)
            if existing is None:
                st.error("File not found.")
                existing = ""
            else:
                st.info("Current content loaded below.")

    update_content = st.text_area("New content", value=existing, height=180, key="uc",
                                   placeholder="Enter new content…")
    update_mode = st.radio("Write mode", ["Overwrite", "Append"],
                           horizontal=True, key="um")
    mode_char = "w" if update_mode == "Overwrite" else "a"

    if st.button("Update File", key="btn_update"):
        if not update_name:
            st.error("Please enter a file name.")
        else:
            ok, msg = update_file(update_name, update_content, mode_char)
            (st.success if ok else st.error)(msg)


# ── Delete ───────────────────────────────────────────────────────────────────

with tab_delete:
    st.subheader("Delete a File")
    delete_name = st.text_input("File name", placeholder="e.g. notes.txt", key="dn")

    st.warning("⚠️  This action is irreversible.", icon="⚠️")
    confirm = st.checkbox("I confirm I want to delete this file.", key="del_confirm")

    if st.button("Delete File", key="btn_delete"):
        if not delete_name:
            st.error("Please enter a file name.")
        elif not confirm:
            st.error("Please tick the confirmation checkbox first.")
        else:
            ok, msg = delete_file(delete_name)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()


# ── Rename ───────────────────────────────────────────────────────────────────

with tab_rename:
    st.subheader("Rename a File")
    r1, r2 = st.columns(2)
    with r1:
        rename_old = st.text_input("Current file name", placeholder="old_name.txt", key="ro")
    with r2:
        rename_new = st.text_input("New file name", placeholder="new_name.txt", key="rn2")

    if st.button("Rename File", key="btn_rename"):
        if not rename_old or not rename_new:
            st.error("Please fill in both fields.")
        else:
            ok, msg = rename_file(rename_old, rename_new)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()


# ── Folder ───────────────────────────────────────────────────────────────────

with tab_folder:
    st.subheader("Folder Operations")
    folder_name = st.text_input("Folder name", placeholder="e.g. my_folder", key="fn")

    f1, f2 = st.columns(2)
    with f1:
        if st.button("📂  Create Folder", key="btn_cf", use_container_width=True):
            if not folder_name:
                st.error("Please enter a folder name.")
            else:
                ok, msg = create_folder_op(folder_name)
                (st.success if ok else st.error)(msg)
                if ok:
                    st.rerun()
    with f2:
        if st.button("🗑️  Remove Folder", key="btn_rf", use_container_width=True):
            if not folder_name:
                st.error("Please enter a folder name.")
            else:
                ok, msg = remove_folder(folder_name)
                (st.success if ok else st.error)(msg)
                if ok:
                    st.rerun()

    st.markdown("---")
    st.caption("💡 Folders must be **empty** before they can be removed.")