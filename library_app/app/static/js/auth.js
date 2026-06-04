document.addEventListener("DOMContentLoaded", () => {
  const authForm = document.getElementById("authForm");
  
  if (authForm) {
    let currentMode = "login";

    const pageTitle = document.getElementById("pageTitle");
    const formTitle = document.getElementById("formTitle");
    const submitBtn = document.getElementById("submitBtn");
    const toggleText = document.getElementById("toggleText");
    const toggleAuthModeBtn = document.getElementById("toggleAuthModeBtn");
    
    const errorBlock = document.getElementById("errorBlock");
    const errorMessage = document.getElementById("errorMessage");

    if (toggleAuthModeBtn) {
      toggleAuthModeBtn.addEventListener("click", () => {
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

    authForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      errorBlock.classList.add("hidden");

      const usernameInput = document.getElementById("username").value.trim();
      const passwordInput = document.getElementById("password").value;

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
            window.location.href = "/books";
          } else {
            alert("Реєстрація успішна! Тепер ви можете увійти у свій акаунт.");
            document.getElementById("password").value = "";
            if (toggleAuthModeBtn) toggleAuthModeBtn.click();
          }
        } else {
          const errorData = await response.json();
          
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