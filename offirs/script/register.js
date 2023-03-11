const nameInput = document.getElementById("name");
const otherGamesInput = document.getElementById("other-games");
const registerButton = document.getElementById("register-button");
registerButton.addEventListener("click", onRegister);

let registerClicked = false;

function onRegister(event) {
  event.preventDefault();
  if (registerClicked) return;

  const characterName = nameInput.value;
  const otherGames = otherGamesInput.checked;

  if (characterName.trim() === "") {
    nameInput.classList.add("error");
    return;
  }

  nameInput.classList.remove("error");
  registerClicked = true;
  registerButton.classList.toggle("register-button--clicked");
  registerButton.innerText = "Registering...";

  /*
  
    Enter backend call here

  
  */

  if (true /*Call success */) {
    registerButton.innerText = "Registration Complete!";
  } else {
    registerButton.innerText = "Error";
  }
}
