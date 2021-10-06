function checkInputsName() {
  const username = document.getElementById('username');
  const usernameValue = username.value.trim();
  if(usernameValue === '') {
    setErrorFor(username, 'Uživatelské jméno nemůže být prázdné.');
  } else if (usernameValue.length < 3) {
    setErrorFor(username, 'Uživatelské jméno je příliš krátké.');
  } else {
    setSuccessFor(username);
    checkInputsTerms()
  }
}
function checkInputsEmail() {
  const email = document.getElementById('email');
  const emailValue = email.value.trim();
  if(emailValue === '') {
    setErrorFor(email, 'Email nemůže být prázdný.');
  } else if (!isEmail(emailValue)) {
    setErrorFor(email, 'Neplatná emailová adresa.');
  } else {
    setSuccessFor(email);
    checkInputsTerms()
  }
}
function checkInputsPassword() {
  const password = document.getElementById('password');
  const passwordValue = password.value.trim();
  var lowerCaseLetters = /[a-z]/g;
  var upperCaseLetters = /[A-Z]/g;
  var numbers = /[0-9]/g;
  if(passwordValue.length < 8) {
    setErrorFor(password, 'Heslo musí mít minimálně 8 znaků.');
  } else if (!passwordValue.match(lowerCaseLetters)) {
    setErrorFor(password, 'Heslo musí obsahovat malá písmena.');
  } else if (!passwordValue.match(upperCaseLetters)) {
    setErrorFor(password, 'Heslo musí obsahovat velká písmena.');
  } else if (!passwordValue.match(numbers)) {
    setErrorFor(password, 'Heslo musí obsahovat číslice.');
	} else {
		setSuccessFor(password);
    checkInputsTerms()
	}
}
function checkInputsPassword2() {
  const password = document.getElementById('password');
  const passwordValue = password.value.trim();
  const password2 = document.getElementById('password2');
  const password2Value = password2.value.trim();
  if(password2Value === '') {
		setErrorFor(password2, 'Heslo nemůže být prázdné.');
	} else if(passwordValue !== password2Value) {
		setErrorFor(password2, 'Hesla se neshodují');
	} else{
		setSuccessFor(password2);
    checkInputsTerms()
	}
}
function checkInputsTerms() {
  var num = 0;
  const email = document.getElementById('email');
  const emailValue = email.value.trim();
  if(document.querySelector('#form_forg')) {
    if(isEmail(emailValue)) {
      document.getElementById("btn_forg_submit").disabled = false;
    } else {
      document.getElementById("btn_forg_submit").disabled = true;
    }
  }
  if(document.querySelector('#form_log')) {
    const password = document.getElementById('password');
    const passwordValue = password.value.trim();
    if(passwordValue !== '') {
      num = num + 1;
    }
    if(isEmail(emailValue)) {
      num = num + 1;
    }
    if(num === 2) {
      document.getElementById("btn_log_submit").disabled = false;
    } else {
      document.getElementById("btn_log_submit").disabled = true;
    }
  }
  if(document.querySelector('#form_reset')) {
    const password = document.getElementById('password');
    const passwordValue = password.value.trim();
    if(passwordValue !== '') {
      num = num + 1;
    }
    if(isEmail(emailValue)) {
      num = num + 1;
    }
    const password2 = document.getElementById('password2');
    const password2Value = password2.value.trim();
    if(passwordValue === password2Value) {
      num = num + 1;
    }
    if(num === 3) {
      document.getElementById("btn_reset_submit").disabled = false;
    } else {
      document.getElementById("btn_reset_submit").disabled = true;
    }
  }
  if(document.querySelector('#form_reg')) {
    const password = document.getElementById('password');
    const passwordValue = password.value.trim();
    if(passwordValue !== '') {
      num = num + 1;
    }
    if(isEmail(emailValue)) {
      num = num + 1;
    }
    const password2 = document.getElementById('password2');
    const password2Value = password2.value.trim();
    if(passwordValue === password2Value) {
      num = num + 1;
    }
    const username = document.getElementById('username');
    const usernameValue = username.value.trim();
    if(usernameValue !== '') {
      num = num + 1;
    }
    const terms = document.getElementById('terms');
    if(terms.checked) {
      if(num === 4) {
        document.getElementById("btn_reg_submit").disabled = false;
      } else {
        document.getElementById("btn_reg_submit").disabled = true;
      }
    }
  }
}
function setErrorFor(input, message) {
	const formControl = input.parentElement;
	const small = formControl.querySelector('small');
	formControl.className = 'form-control error';
	small.innerText = message;
}
function setSuccessFor(input) {
	const formControl = input.parentElement;
	formControl.className = 'form-control success';
}

function isEmail(email) {
	return /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$/i.test(email);
}
window.addEventListener('scroll', function () {
  let header = document.querySelector('header');
  let windowPosition = window.scrollY > 0;
  header.classList.toggle('scrolling-active', windowPosition);
})