from typing import Dict, List

class LibraryManager:
    def __init__(self):
        # Initialize empty list to store books
        self.books: List[Dict] = []

    def add_book(self, title: str, author: str, year: int, genre: str, read_status: bool) -> None:
        """Add a new book to the library"""
        # Create a dictionary to store book details
        book = {
            'title': title.strip(),
            'author': author.strip(),
            'year': year,
            'genre': genre.strip(),
            'read_status': read_status
        }
        # Add the book to our list
        self.books.append(book)
        print("Book added successfully!")

    def remove_book(self, title: str) -> None:
        """Remove a book from the library by title"""
        # Find the book with matching title (case-insensitive)
        for book in self.books:
            if book['title'].lower() == title.lower():
                self.books.remove(book)
                print("Book removed successfully!")
                return
        print(f"Book '{title}' not found in the library.")

    def search_books(self, query: str) -> List[Dict]:
        """Search for books by title or author"""
        query = query.lower().strip()
        # Return all books where query matches title or author
        return [
            book for book in self.books
            if query in book['title'].lower() or
               query in book['author'].lower()
        ]

    def display_books(self) -> None:
        """Display all books in the library"""
        if not self.books:
            print("\nNo books in the library.")
            return

        print("\nYour Library:")
        for i, book in enumerate(self.books, 1):
            status = "Read" if book['read_status'] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

    def get_statistics(self) -> Dict:
        """Calculate and return library statistics"""
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book['read_status'])
        
        return {
            "total_books": total_books,
            "read_books": read_books,
            "unread_books": total_books - read_books
        }

def get_valid_year() -> int:
    """Get a valid publication year from user"""
    while True:
        try:
            year = int(input("Enter the publication year: "))
            if 1800 <= year <= 2024:  # Simple year validation
                return year
            print("Please enter a year between 1800 and 2024")
        except ValueError:
            print("Please enter a valid year.")

def get_valid_input(prompt: str) -> str:
    """Get non-empty input from user"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")

def get_yes_no(prompt: str) -> bool:
    """Get yes/no input from user"""
    while True:
        response = input(prompt).lower().strip()
        if response in ['yes', 'y']:
            return True
        if response in ['no', 'n']:
            return False
        print("Please enter 'yes' or 'no'")

def main():
    # Create library manager instance
    library = LibraryManager()

    print("Welcome to your Personal Library Manager!")
    
    while True:
        # Display menu
        print("\nMenu")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        
        choice = input("\nEnter your choice: ")

        if choice == "1":
            # Add a new book
            print("\nAdd a Book")
            title = get_valid_input("Enter the book title: ")
            author = get_valid_input("Enter the author: ")
            year = get_valid_year()
            genre = get_valid_input("Enter the genre: ")
            read_status = get_yes_no("Have you read this book? (yes/no): ")
            library.add_book(title, author, year, genre, read_status)

        elif choice == "2":
            # Remove a book
            print("\nRemove a Book")
            title = get_valid_input("Enter the title of the book to remove: ")
            library.remove_book(title)

        elif choice == "3":
            # Search for a book
            print("\nSearch for a Book")
            query = get_valid_input("Enter search term (title or author): ")
            results = library.search_books(query)
            
            if results:
                print("\nMatching Books:")
                for i, book in enumerate(results, 1):
                    status = "Read" if book['read_status'] else "Unread"
                    print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
            else:
                print("\nNo matching books found.")

        elif choice == "4":
            # Display all books
            library.display_books()

        elif choice == "5":
            # Display statistics
            stats = library.get_statistics()
            print("\nDisplay Statistics")
            print(f"Total books: {stats['total_books']}")
            if stats['total_books'] > 0:
                read_percentage = (stats['read_books'] / stats['total_books']) * 100
                print(f"Percentage read: {read_percentage:.1f}%")

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
