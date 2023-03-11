const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const badCredentials = document.getElementById("bad-credentials");
const loginButton = document.getElementById("login-button");
loginButton.addEventListener("click", onLogin);

function onLogin(event) {
  event.preventDefault();

  const username = usernameInput.value;
  const password = passwordInput.value;

  let inputError = false;
  if (username.trim() === "") {
    usernameInput.classList.add("error");
    inputError = true;
  } else {
    usernameInput.classList.remove("error");
  }
  if (password.trim() === "") {
    passwordInput.classList.add("error");
    inputError = true;
  } else {
    passwordInput.classList.remove("error");
  }
  if (inputError) return;

  usernameInput.classList.remove("error");
  passwordInput.classList.remove("error");

  /*
  
    Enter backend call here

  
  */

  if (false /*Call success */) {
    /* Do something */
  } else {
    badCredentials.classList.remove("hidden");
  }
}
