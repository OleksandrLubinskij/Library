document.addEventListener("DOMContentLoaded", () => {
  // === БЛОК 1: ДИНАМІЧНИЙ ВХІД ТА РЕЄСТРАЦІЯ ===
  // Отримуємо елементи універсальної форми (якщо вони є на поточній сторінці)
  const authForm = document.getElementById("authForm");
  
  if (authForm) {
    let currentMode = "login"; // Поточний стан форми: 'login' або 'register'

    const pageTitle = document.getElementById("pageTitle");
    const formTitle = document.getElementById("formTitle");
    const submitBtn = document.getElementById("submitBtn");
    const toggleText = document.getElementById("toggleText");
    const toggleAuthModeBtn = document.getElementById("toggleAuthModeBtn");
    
    const errorBlock = document.getElementById("errorBlock");
    const errorMessage = document.getElementById("errorMessage");

    // 1.1. Логіка перемикання інтерфейсу (Вхід <-> Реєстрація)
    if (toggleAuthModeBtn) {
      toggleAuthModeBtn.addEventListener("click", () => {
        // Ховаємо блок помилок при зміні режиму
        errorBlock.classList.add("hidden");

        if (currentMode === "login") {
          currentMode = "register";
          if (pageTitle) pageTitle.innerText = "Реєстрація у бібліотеці";
          formTitle.innerText = "Створення акаунту";
          submitBtn.innerText = "Зареєструватися";
          toggleText.innerText = "Вже є акаунт?";
          toggleAuthModeBtn.innerText = "Увійти";
        } else {
          currentMode = "login";
          if (pageTitle) pageTitle.innerText = "Вхід до бібліотеки";
          formTitle.innerText = "Вхід в систему";
          submitBtn.innerText = "Увійти";
          toggleText.innerText = "Ще не маєте акаунту?";
          toggleAuthModeBtn.innerText = "Зареєструватися";
        }
      });
    }

    // 1.2. Обробка відправки (сабміту) універсальної форми
    authForm.addEventListener("submit", async (e) => {
      e.preventDefault(); // Залізно блокуємо перезавантаження сторінки

      errorBlock.classList.add("hidden");

      const usernameInput = document.getElementById("username").value.trim();
      const passwordInput = document.getElementById("password").value;

      // Динамічно підставляємо потрібний ендпоінт залежно від обраного режиму
      const endpoint = currentMode === "login" ? "/user/login" : "/user/register";

      console.log(`[${currentMode.toUpperCase()}] Відправка запиту на: ${endpoint}`);

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: usernameInput,
            password: passwordInput,
          }),
        });

        if (response.ok) {
          if (currentMode === "login") {
            // Перенаправляємо на список книг у разі успішного входу
            window.location.href = "/books";
          } else {
            // Якщо це була успішна реєстрація — повідомляємо користувача,
            // очищуємо пароль та автоматично перемикаємо форму в режим входу
            alert("Реєстрація успішна! Тепер ви можете увійти у свій акаунт.");
            document.getElementById("password").value = "";
            if (toggleAuthModeBtn) toggleAuthModeBtn.click();
          }
        } else {
          const errorData = await response.json();
          
          // Валідація помилок FastAPI/Pydantic (якщо повернувся масив `detail`)
          if (Array.isArray(errorData.detail)) {
            errorMessage.innerText = errorData.detail[0].msg;
          } else {
            errorMessage.innerText = errorData.detail || "Невірний логін або пароль";
          }
          errorBlock.classList.remove("hidden");
        }
      } catch (error) {
        console.error("Помилка відправки форми:", error);
        errorMessage.innerText = "Сталася помилка з'єднання з сервером.";
        errorBlock.classList.remove("hidden");
      }
    });
  }

  // === БЛОК 2: ЛОГІКА ВИХОДУ З СИСТЕМИ (LOGOUT) ===
  // Оскільки цей скрипт підключається глобально через base.html,
  // кнопка виходу може бути присутня на будь-якій захищеній сторінці сайту
  const logoutBtn = document.getElementById("logoutBtn");

  if (logoutBtn) {
    logoutBtn.addEventListener("click", async (e) => {
      e.preventDefault();

      try {
        const response = await fetch("/user/logout", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          // Після очищення Cookies перекидаємо користувача на сторінку авторизації
          window.location.href = "/login";
        } else {
          alert("Сталася помилка при виході з системи.");
        }
      } catch (error) {
        console.error("Помилка з'єднання з сервером під час логауту:", error);
      }
    });
  }
});