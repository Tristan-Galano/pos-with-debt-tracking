// JavaScript code to make the calculator work
// Get all the calculator buttons
const buttons = document.querySelectorAll('.calc-button');
const display = document.getElementById('display');
const disnumberInputplay = document.getElementById('display');

let currentInput = '';

buttons.forEach(button => {
    button.addEventListener('click', () => {
        const value = button.getAttribute('data-value');
        
        if (value === 'C') {
            currentInput = '';
            display.value = '';
        } else if (value === '=') {
            try {
                currentInput = eval(currentInput).toString();
                display.value = currentInput;
            } catch (e) {
                display.value = 'Error';
                currentInput = '';
            }
        } else {
            currentInput += value;
            display.value = currentInput;
        }
    });
});

document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevents default submission

    const formData = new FormData(this);

    fetch('http://127.0.0.1:5000//tansaction', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      // Process the response data
      console.log('Success:', data);
      // You can update the page content here without reloading
      display.value = '';
      disnumberInputplay.value = '';
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  });
