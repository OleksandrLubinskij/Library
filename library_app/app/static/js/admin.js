document.addEventListener("DOMContentLoaded", () => {
    
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            const targetTabId = event.target.getAttribute("data-tab");

            tabContents.forEach(content => content.classList.add("hidden"));
            tabButtons.forEach(btn => {
                btn.classList.remove("text-indigo-600", "border-b-2", "border-indigo-600");
                btn.classList.add("text-gray-500");
            });

            document.getElementById(targetTabId).classList.remove("hidden");
            event.target.classList.add("text-indigo-600", "border-b-2", "border-indigo-600");
            event.target.classList.remove("text-gray-500");
        });
    });

    const createBookForm = document.getElementById("create-book-form");
    if (createBookForm) {
        createBookForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const title = document.getElementById("book-title").value;
            const genre = document.getElementById("book-genre").value;
            const release_year = parseInt(document.getElementById("book-release-year").value);
            const author_id = parseInt(document.getElementById("book-author-id").value);

            const response = await fetch("/books/create", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, genre, release_year, author_id })
            });

            if (response.ok) {
                alert("Книгу успішно додано!");
                window.location.href = "/books";
            } else {
                alert("Помилка створення книги. Перевірте, чи існує автор із таким ID, та правильність введених даних.");
            }
        });
    }

    const createAuthorForm = document.getElementById("create-author-form");
    if (createAuthorForm) {
        createAuthorForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const firstname = document.getElementById("author_firstname").value;
            const lastname = document.getElementById("author_lastname").value;

            const response = await fetch("/authors/create", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ firstname, lastname })
            });

            if (response.ok) {
                alert("Автора успішно додано!");
                window.location.href = "/authors";
            } else {
                alert("Помилка при створенні автора.");
            }
        });
    }

    const loadBookBtn = document.getElementById("load-book-btn");
    const updateBookForm = document.getElementById("update-book-form");

    if (loadBookBtn) {
        loadBookBtn.addEventListener("click", async () => {
            const id = document.getElementById("edit-book-id").value;
            if (!id) return alert("Будь ласка, вкажіть ID книги.");

            const response = await fetch(`/books/book_by_id/${id}`);
            if (response.ok) {
                const bookData = await response.json();
                
                document.getElementById("edit-book-title").value = bookData.title;
                document.getElementById("edit-book-genre").value = bookData.genre || "";
                document.getElementById("edit-book-release-year").value = bookData.release_year || "";
                document.getElementById("edit-book-author-id").value = bookData.author_id;
                
                updateBookForm.classList.remove("hidden");
            } else {
                alert("Книгу з таким ID не знайдено в системі.");
                updateBookForm.classList.add("hidden");
            }
        });
    }

    if (updateBookForm) {
        updateBookForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const id = document.getElementById("edit-book-id").value;
            const title = document.getElementById("edit-book-title").value;
            const genre = document.getElementById("edit-book-genre").value;
            const release_year = parseInt(document.getElementById("edit-book-release-year").value);
            const author_id = parseInt(document.getElementById("edit-book-author-id").value);

            const response = await fetch(`/books/edit/${id}`, {
                method: "PATCH", 
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, genre, release_year, author_id })
            });

            if (response.ok) {
                alert("Дані книги успішно оновлено!");
                window.location.href = "/books";
            } else {
                alert("Помилка оновлення даних. Перевірте правильність ID автора.");
            }
        });
    }
});