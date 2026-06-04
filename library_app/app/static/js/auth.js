document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const errorBlock = document.getElementById('errorBlock');
            const errorMessage = document.getElementById('errorMessage');
            
            errorBlock.classList.add('hidden'); 

            const usernameInput = document.getElementById('username').value;
            const passwordInput = document.getElementById('password').value;
            try {
                const response = await fetch('/user/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: usernameInput,
                        password: passwordInput
                    })
                });

                if (response.ok) {
                    window.location.href = '/books'; 
                } else {
                    const errorData = await response.json();
                    
                    if (Array.isArray(errorData.detail)) {
                        errorMessage.innerText = errorData.detail[0].msg;
                    } else {
                        errorMessage.innerText = errorData.detail || 'Невірний логін або пароль';
                    }
                    errorBlock.classList.remove('hidden');
                }
            } catch (error) {
                errorMessage.innerText = 'Сталася помилка з`єднання з сервером.';
                errorBlock.classList.remove('hidden');
            }
        });
    }
});

