document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".delete-author-btn");
    
    deleteButtons.forEach(button => {
        button.addEventListener("click", async (event) => {
            const authorId = event.target.getAttribute("data-author-id");
            
            if (!confirm("УВАГА! Видалення автора призведе до каскадного видалення ВСІХ його книг за ТЗ. Продовжити?")) {
                return;
            }
            
            try {
                const response = await fetch(`/api/authors/${authorId}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    window.location.reload();
                } else {
                    alert("Помилка видалення автора з бази даних.");
                }
            } catch (error) {
                console.error("Error deleting author:", error);
                alert("Сталася мережева помилка.");
            }
        });
    });
});