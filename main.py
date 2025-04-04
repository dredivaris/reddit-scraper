import praw
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables only in development
if os.path.exists('.env'):
    load_dotenv()

# Initialize Reddit API
def init_reddit():
    # Try getting from environment first (for production)
    client_id = os.environ.get("REDDIT_CLIENT_ID") or st.secrets["REDDIT_CLIENT_ID"]
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET") or st.secrets["REDDIT_CLIENT_SECRET"]
    user_agent = os.environ.get("REDDIT_USER_AGENT") or st.secrets["REDDIT_USER_AGENT"]

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_subreddit_posts(_reddit, subreddit_name, post_limit, time_filter="month"):
    try:
        subreddit = _reddit.subreddit(subreddit_name)
        posts_dict = {
            "Title": [],
            "Post Text": [],
            "ID": [],
            "Score": [],
            "Total Comments": [],
            "Post URL": []
        }

        for post in subreddit.top(limit=post_limit, time_filter=time_filter):
            posts_dict["Title"].append(post.title)
            posts_dict["Post Text"].append(post.selftext)
            posts_dict["ID"].append(post.id)
            posts_dict["Score"].append(post.score)
            posts_dict["Total Comments"].append(post.num_comments)
            posts_dict["Post URL"].append(post.url)

        return pd.DataFrame(posts_dict)
    except Exception as e:
        st.error(f"Error fetching subreddit posts: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_post_by_url(_reddit, url):
    try:
        submission = _reddit.submission(url=url)

        post_data = {
            "Title": submission.title,
            "Post Text": submission.selftext,
            "ID": submission.id,
            "Score": submission.score,
            "Total Comments": submission.num_comments,
            "Post URL": submission.url
        }

        post_comments = []
        submission.comments.replace_more(limit=None)

        for comment in submission.comments.list():
            # Get parent ID - if it's a top-level comment, the parent is the submission
            parent_id = comment.parent_id
            is_top_level = comment.parent_id.startswith('t3_')  # t3_ prefix indicates a submission

            # For display purposes, clean up the parent_id by removing the prefix
            # t1_ prefix is for comments, t3_ prefix is for submissions
            clean_parent_id = parent_id[3:] if parent_id else None

            comment_data = {
                "Comment ID": comment.id,
                "Comment Text": comment.body,
                "Score": comment.score,
                "Author": str(comment.author),
                "Created UTC": comment.created_utc,
                "Parent ID": clean_parent_id,
                "Is Top Level": is_top_level
            }
            post_comments.append(comment_data)

        return pd.DataFrame([post_data]), pd.DataFrame(post_comments)
    except Exception as e:
        st.error(f"Error fetching post: {str(e)}")
        return pd.DataFrame(), pd.DataFrame()

def main():
    st.title("Reddit Data Scraper")

    # Initialize Reddit instance
    reddit = init_reddit()

    # Sidebar for input parameters
    st.sidebar.header("Settings")
    scrape_option = st.sidebar.radio(
        "Choose scraping option:",
        ["Subreddit Posts", "Specific Post by URL"]
    )

    if scrape_option == "Subreddit Posts":
        st.header("Subreddit Posts Scraper")

        # Input fields
        subreddit_name = st.text_input("Enter subreddit name:", "selfhosted")
        post_limit = st.slider("Number of posts to scrape:", 1, 100, 10)
        time_filter = st.selectbox(
            "Time filter:",
            ["day", "week", "month", "year", "all"]
        )

        if st.button("Scrape Subreddit"):
            with st.spinner("Scraping posts..."):
                try:
                    df = get_subreddit_posts(reddit, subreddit_name, post_limit, time_filter)
                    st.success(f"Successfully scraped {len(df)} posts!")

                    # Display the data
                    st.dataframe(df)

                    # Download button
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download CSV",
                        csv,
                        f"{subreddit_name}_posts.csv",
                        "text/csv",
                        key='download-csv'
                    )
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    else:
        st.header("Post URL Scraper")

        post_url = st.text_input("Enter Reddit post URL:")

        if st.button("Scrape Post"):
            with st.spinner("Scraping post and comments..."):
                try:
                    post_df, comments_df = get_post_by_url(reddit, post_url)

                    st.subheader("Post Details")
                    st.dataframe(post_df)

                    st.subheader(f"Comments ({len(comments_df)} total)")

                    # Add a checkbox to toggle between flat view and hierarchical info
                    show_hierarchy = st.checkbox("Show parent-child relationships", value=True)

                    if show_hierarchy:
                        # Display with hierarchy information
                        st.dataframe(comments_df)

                        # Add an explanation of the parent-child relationship
                        st.info("""
                        **Understanding Parent-Child Relationships:**
                        - **Comment ID**: Unique identifier for each comment
                        - **Parent ID**: ID of the parent comment or submission
                        - **Is Top Level**: True if the comment is a direct reply to the post, False if it's a reply to another comment
                        """)
                    else:
                        # Display without hierarchy columns for a cleaner view
                        st.dataframe(comments_df.drop(columns=["Parent ID", "Is Top Level", "Comment ID"], errors="ignore"))

                    # Download buttons
                    post_csv = post_df.to_csv(index=False).encode('utf-8')

                    # Always include all columns in the CSV download, regardless of display setting
                    # This ensures parent-child relationship data is always in the download
                    comments_csv = comments_df.to_csv(index=False).encode('utf-8')

                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "Download Post CSV",
                            post_csv,
                            "post_details.csv",
                            "text/csv",
                            key='download-post'
                        )
                    with col2:
                        st.download_button(
                            "Download Comments CSV",
                            comments_csv,
                            "comments.csv",
                            "text/csv",
                            key='download-comments'
                        )

                    # Add a note about the CSV content
                    st.caption("Note: The downloaded CSV will include all comment data including parent-child relationships, even if they're hidden in the display.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

