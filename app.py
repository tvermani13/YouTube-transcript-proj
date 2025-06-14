import streamlit as st
import os

st.title("🎬 YouTube Summary + Validation Viewer")

base_dir = "videos"

video_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
video_dirs.sort(reverse=True)

# Load directory and title mapping
video_infos = []
for d in video_dirs:
    title_path = os.path.join(base_dir, d, "title.txt")
    if os.path.exists(title_path):
        with open(title_path, 'r', encoding='utf-8') as f:
            title = f.read().strip()
    else:
        title = f"(Untitled) {d}"
    video_infos.append((f"{title} ({d[:6]})", d))  # Display title + partial hash

# Select based on title
dropdown_labels = [info[0] for info in video_infos]
selected_hash_label = st.selectbox("Select a video", dropdown_labels)

# Get corresponding hash
selected_hash_hash = next(d for label, d in video_infos if label == selected_hash_label)


selected_hash = st.selectbox("Select a video summary", video_dirs)

if selected_hash:
    dir_path = os.path.join(base_dir, selected_hash)
    
    def read_file(name):
        path = os.path.join(dir_path, name)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return "❌ File not found"

    st.subheader("📝 Transcript")
    st.text_area("Transcript", read_file("transcript.txt"), height=300)

    st.subheader("🧠 LLM Summary (Ollama)")
    st.text_area("Summary", read_file("summary.txt"), height=200)
    
    st.subheader("✅ Summary Validation (Gemini)")
    st.text_area("Summary Validation", read_file("summary_validation.txt"), height=200)

    st.subheader("🔍 Extracted Claims")
    st.text_area("Claims", read_file("claims.txt"), height=150)

    st.subheader("✅ Claims Validation (Gemini)")
    st.text_area("Claims Validation", read_file("claims_validation.txt"), height=200)

