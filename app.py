import streamlit as st
from typing import Dict, List
import json
from datetime import datetime
import os

def display_profile():
    """Display profile information"""
    # Custom CSS for profile section
    st.markdown("""
    <style>
    .profile-section {
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .profile-name {
        font-size: 36px;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 5px;
    }
    .github-id {
        font-size: 20px;
        color: #666;
        margin-top: 5px;
    }
    .github-link {
        text-decoration: none;
        color: #666;
        transition: color 0.3s ease;
    }
    .github-link:hover {
        color: #0366d6;
    }
    .profile-placeholder {
        width: 200px;
        height: 200px;
        background-color: #e9ecef;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

    # Profile section container
    with st.container():
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Create a placeholder for profile image
            st.markdown("""
            <div class="profile-placeholder">
                <span style="font-size: 40px;">👤</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Profile information
            st.markdown('<div class="profile-name">Altaf Sajdi</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="github-id">
                <a href="https://github.com/altaf-sajdi" class="github-link" target="_blank">
                    <svg height="20" width="20" style="display: inline-block; vertical-align: middle; margin-right: 5px;" viewBox="0 0 16 16">
                        <path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                    altaf-sajdi
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

class LibraryManager:
    def __init__(self):
        self.books: List[Dict] = []
        self.filename = "library.json"
        self._load_from_file()

    def add_book(self, title: str, author: str, year: int, genre: str, read_status: bool) -> None:
        """Add a new book to the library"""
        book = {
            'title': title.strip(),
            'author': author.strip(),
            'year': year,
            'genre': genre.strip(),
            'read_status': read_status,
            'date_added': datetime.now().strftime("%Y-%m-%d")
        }
        self.books.append(book)
        self._save_to_file()
        st.success("Book added successfully!")

    def remove_book(self, title: str) -> None:
        """Remove a book from the library by title"""
        for book in self.books:
            if book['title'].lower() == title.lower():
                self.books.remove(book)
                self._save_to_file()
                st.success("Book removed successfully!")
                return
        st.error(f"Book '{title}' not found in the library.")

    def search_books(self, query: str) -> List[Dict]:
        """Search for books by title or author"""
        query = query.lower().strip()
        return [
            book for book in self.books
            if query in book['title'].lower() or
               query in book['author'].lower()
        ]

    def get_statistics(self) -> Dict:
        """Calculate and return library statistics"""
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book['read_status'])
        unread_books = total_books - read_books
        
        # Calculate genre distribution
        genre_distribution = {}
        for book in self.books:
            genre = book['genre']
            genre_distribution[genre] = genre_distribution.get(genre, 0) + 1
        
        return {
            "total_books": total_books,
            "read_books": read_books,
            "unread_books": unread_books,
            "genre_distribution": genre_distribution
        }

    def _save_to_file(self) -> None:
        """Save library data to JSON file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, indent=4)
        except Exception as e:
            st.error(f"Error saving library data: {str(e)}")

    def _load_from_file(self) -> None:
        """Load library data from JSON file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []
        except Exception as e:
            st.error(f"Error loading library data: {str(e)}")
            self.books = []

def main():
    st.set_page_config(
        page_title="Personal Library Manager",
        page_icon="📚",
        layout="wide"
    )

    # Display profile information
    display_profile()
    
    st.title("📚 Personal Library Manager")
    
    # Initialize library manager
    if 'library' not in st.session_state:
        st.session_state.library = LibraryManager()

    # Sidebar for adding new books
    with st.sidebar:
        st.header("Add New Book")
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=1800, max_value=datetime.now().year, value=2024)
            genre = st.text_input("Genre")
            read_status = st.checkbox("I have read this book")
            
            if st.form_submit_button("Add Book"):
                if title and author and genre:
                    st.session_state.library.add_book(title, author, year, genre, read_status)
                else:
                    st.error("Please fill in all required fields.")

    # Main content area
    tab1, tab2, tab3 = st.tabs(["📖 Library", "🔍 Search", "📊 Statistics"])

    # Library Tab
    with tab1:
        st.header("Your Library")
        if not st.session_state.library.books:
            st.info("Your library is empty. Add some books using the sidebar!")
        else:
            for i, book in enumerate(st.session_state.library.books, 1):
                with st.expander(f"{i}. {book['title']} by {book['author']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Genre:** {book['genre']}")
                        st.write(f"**Year:** {book['year']}")
                        st.write(f"**Status:** {'Read' if book['read_status'] else 'Unread'}")
                        st.write(f"**Added:** {book['date_added']}")
                    with col2:
                        if st.button("Remove", key=f"remove_{i}"):
                            st.session_state.library.remove_book(book['title'])
                            st.rerun()

    # Search Tab
    with tab2:
        st.header("Search Books")
        search_query = st.text_input("Search by title or author")
        if search_query:
            results = st.session_state.library.search_books(search_query)
            if results:
                st.write(f"Found {len(results)} matching books:")
                for book in results:
                    st.write(f"- {book['title']} by {book['author']} ({book['year']})")
            else:
                st.info("No matching books found.")

    # Statistics Tab
    with tab3:
        st.header("Library Statistics")
        stats = st.session_state.library.get_statistics()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", stats['total_books'])
        with col2:
            st.metric("Books Read", stats['read_books'])
        with col3:
            st.metric("Books Unread", stats['unread_books'])
        
        if stats['total_books'] > 0:
            read_percentage = (stats['read_books'] / stats['total_books']) * 100
            st.write(f"Percentage of books read: {read_percentage:.1f}%")
            
            st.subheader("Genre Distribution")
            for genre, count in stats['genre_distribution'].items():
                st.write(f"{genre}: {count} books")

if __name__ == "__main__":
    main() 