



// Función para verificar si el número es mayor a 50 y mostrar una alerta

function checkNumber() {
  var numberInput = document.getElementsByName("pokemon")[0].value;
  var parsedNumber = parseInt(numberInput);
  if (parsedNumber > 50) {
      alert("Se permite la busqueda a este Pokémon, pero por favor, \n buscar Pokémon con su id menor a 50.");
  }
}

// Agrega el evento onsubmit al formulario para llamar a la función de verificación
document.getElementsByTagName("form")[0].onsubmit = function () {
  checkNumber();
};

/*Estas dos funciones son para activar los sonidos de dos botones,
  tanto btn=Informacion y btn=Busqueda que tiene imagen de lupa 
*/
function playSound() {
var sound = document.getElementById('clickSound');
sound.currentTime = 1; 
sound.play();
sound.addEventListener('ended', function() {
  sound.currentTime = 5.999;
});
}

function playSound_dex() {
  var sound = document.getElementById('clickSound-dex');
  sound.currentTime = 1; 
  sound.play();
  sound.addEventListener('ended', function() {
      sound.currentTime = 5.999;
});
}


/*Esta función no permite que se generen espacios. si el usuario genera algun espacio 
le sale un alerta para que ingrese un elemento valido*/
function validateAndSubmitForm() {
  var userInput = document.getElementById('inputField').value;
  var trimmedValue = userInput.trim();
  if (trimmedValue === "") {
      alert("Por favor, ingrese un valor válido.");
      return false;
  }
  document.getElementById('inputField').value = trimmedValue;
  return true;
}
document.getElementById('inputField').addEventListener('input', function() {
  validateAndSubmitForm();
});


