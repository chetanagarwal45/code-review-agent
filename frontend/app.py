import streamlit as st
import httpx

API = "http://localhost:8000"

st.set_page_config(page_title="🤖 Local Code Review Agent", page_icon="🤖", layout="wide")
st.title("🤖 Local Code Review Agent")
st.caption("Powered by Qwen2.5‑Coder running 100 % locally via Ollama")

# --------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio("Review mode", ["📝 Code snippet", "🔗 GitHub PR"])
    st.divider()
    st.info("🟢 Model: Qwen2.5‑Coder:7b\n\n🔒 100 % Local\n\n📖 Open Source")

# --------------------------------------------------------------
# Code snippet mode
# --------------------------------------------------------------
if mode == "📝 Code snippet":
    st.subheader("📝 Paste Your Code")
    code = st.text_area("Code to review", height=250, placeholder="Paste your code here...")
    filename = st.text_input("Filename (optional)", placeholder="e.g. main.py")

    if st.button("🔍 Review Code", type="primary"):
        if not code.strip():
            st.warning("Please paste some code first.")
        else:
            with st.spinner("🤖 Reviewing with Qwen2.5‑Coder…"):
                try:
                    r = httpx.post(
                        f"{API}/review/code",
                        json={"code": code, "filename": filename},
                        timeout=120,
                    )
                    r.raise_for_status()
                    data = r.json()
                except Exception as e:
                    st.error(f"Error contacting backend: {e}")
                    st.stop()

            score = data.get("quality_score", 0)
            emoji = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
            st.metric("Quality Score", f"{score}/10")
            st.write(f"**Summary:** {data.get('summary')}")
            st.write(f"**Severity:** `{data.get('severity', 'low').upper()}`")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.error(f"🐛 Bugs ({len(data.get('bugs', []))})")
                for b in data.get("bugs", []):
                    st.write(f"• {b}")
            with col2:
                st.warning(f"💡 Suggestions ({len(data.get('suggestions', []))})")
                for s in data.get("suggestions", []):
                    st.write(f"• {s}")
            with col3:
                st.info(f"🔒 Security ({len(data.get('security_issues', []))})")
                for sec in data.get("security_issues", []):
                    st.write(f"• {sec}")

            st.divider()
            st.subheader("📋 GitHub Comment Preview")
            st.markdown(data.get("comment", ""))

# --------------------------------------------------------------
# PR review mode
# --------------------------------------------------------------
else:
    st.subheader("🔗 Review a GitHub Pull Request")
    pr_url = st.text_input(
        "GitHub PR URL",
        placeholder="https://github.com/owner/repo/pull/123",
    )
    col1, col2 = st.columns(2)
    with col1:
        post_comment = st.checkbox("Post comment to PR", value=True)
    with col2:
        add_labels = st.checkbox("Auto‑add labels", value=True)

    if st.button("🔍 Review PR", type="primary"):
        if not pr_url.strip():
            st.warning("Please paste a PR URL.")
        else:
            with st.spinner("Fetching PR and reviewing…"):
                try:
                    # Parse URL → owner/repo + number
                    parts = pr_url.rstrip("/").split("/")
                    repo_name = f"{parts[-4]}/{parts[-3]}"
                    pr_number = int(parts[-1])

                    r = httpx.post(
                        f"{API}/review/pr",
                        json={
                            "repo_name": repo_name,
                            "pr_number": pr_number,
                            "post_comment": post_comment,
                            "add_labels": add_labels,
                        },
                        timeout=120,
                    )
                    r.raise_for_status()
                    result = r.json()
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.stop()

            review = result.get("review", {})
            st.success("✅ PR reviewed!")
            st.metric("Quality Score", f"{review.get('quality_score', 0)}/10")

            if result.get("comment_posted"):
                st.info("💬 Comment posted to GitHub PR")
            if result.get("labels_added"):
                st.info(f"🏷️ Labels added: {result['labels_added']}")

            with st.expander("Full review JSON"):
                st.json(review)
