// JavaScript code to make the calculator work
// Get all the calculator buttons
const buttons = document.querySelectorAll('.calc-button');
const display = document.getElementById('display');

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
