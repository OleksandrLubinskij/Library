// app/static/js/books.js

async function deleteBook(id) {
    if (!confirm("Ви впевнені, що хочете видалити цю книгу?")) return;

    try {
        const response = await fetch(`/books/delete/${id}`, { 
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            document.getElementById(`book-${id}`).remove();
        } else {
            alert("Помилка при видаленні");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Не вдалося виконати запит");
    }
}