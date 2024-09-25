import streamlit as st
from PIL import Image

# Initialize posts and comments in session state if not already done
if 'posts' not in st.session_state:
    st.session_state.posts = []
if 'comments' not in st.session_state:
    st.session_state.comments = {}

# Function to add new post
def add_post(category, title, image, tags):
    st.session_state.posts.append({"category": category, "title": title, "image": image, "tags": tags, "likes": 0})

# Function to add comment to a post
def add_comment(post_title, comment):
    if post_title not in st.session_state.comments:
        st.session_state.comments[post_title] = []
    st.session_state.comments[post_title].append(comment)

# Function to like a post
def like_post(post_title):
    for post in st.session_state.posts:
        if post["title"] == post_title:
            post["likes"] += 1
            break

# App title
st.title("OJUS Community")

# Sidebar for category selection
st.sidebar.header("Categories")
categories = ["Sports", "Cultural", "Technical"]
selected_category = st.sidebar.selectbox("Select a Category", categories)

# Display subcategories based on selected category
if selected_category == "Sports":
    subcategories = ["Cricket", "Football", "Carrom"]
elif selected_category == "Cultural":
    subcategories = ["Singing", "Dancing", "Drama", "Fashion Show"]
else:  # Technical
    subcategories = ["Games", "Hackathon"]

selected_subcategory = st.sidebar.selectbox("Select a Subcategory", subcategories)

# New Post Form
st.header(f"Post in {selected_subcategory}")
title = st.text_input("Post Title")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
tags_input = st.text_input("Add tags (comma-separated)")

if st.button("Add Post"):
    if title and uploaded_file:
        image = Image.open(uploaded_file)
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]  # Process tags
        add_post(selected_subcategory, title, image, tags)
        st.success("Post added successfully!")

# Display posts with filtering by tags
st.header("Recent Posts")
filter_tags = st.sidebar.text_input("Filter by tags (comma-separated)")

for post in st.session_state.posts:
    if filter_tags:
        filter_list = [tag.strip() for tag in filter_tags.split(",")]
        if not any(tag in post["tags"] for tag in filter_list):
            continue  # Skip posts that don't match the filter

    st.subheader(post["title"])
    st.image(post["image"], use_column_width=True)

    # Like feature
    if st.button(f"Like {post['title']}"):
        like_post(post["title"])
        st.success(f"You liked '{post['title']}'!")

    # Display likes
    st.write(f"Likes: {post['likes']}")

    # Comment section
    comment = st.text_input("Leave a comment:", key=post["title"])
    if st.button("Submit Comment", key=f"comment_{post['title']}"):
        if comment:
            add_comment(post["title"], comment)
            st.success("OJUs  Community")

    # Display comments
    if post["title"] in st.session_state.comments:
        st.write("Comments:")
        for c in st.session_state.comments[post["title"]]:
            st.write(f"- {c}")

# Clear posts and comments functionality (for demonstration purposes)
if st.sidebar.button("Clear All Posts"):
    st.session_state.posts.clear()
    st.session_state.comments.clear()
    st.success("All posts and comments have been cleared.")
