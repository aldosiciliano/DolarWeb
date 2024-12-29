document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('converterForm');
    const amount = document.getElementById('amount');
    const fromCurrency = document.getElementById('fromCurrency');
    const toCurrency = document.getElementById('toCurrency');
    const swapButton = document.getElementById('swapButton');
    const resultAmount = document.getElementById('resultAmount');
    const resultRate = document.getElementById('resultRate');

    // Tasas de cambio actualizadas para cada tipo de dólar
    const rates = {
        'ARS_BLUE': 1/1215,
        'ARS_OFICIAL': 1/1051,
        'ARS_CRYPTO': 1/1200,  // Ejemplo
        'ARS_TARJETA': 1/1050  // Ejemplo
    };

    // Función para actualizar el resultado
    function updateResult() {
        const fromValue = fromCurrency.value;
        const toValue = toCurrency.value;
        const amountValue = parseFloat(amount.value);

        const rateKey = `${fromValue}_${toValue}`;
        const rate = rates[rateKey];
        
        const result = amountValue * rate;
        const dollarType = toValue.charAt(0).toUpperCase() + toValue.slice(1).toLowerCase();
        resultAmount.textContent = `$${amountValue} ${fromValue} = $${result.toFixed(2)} USD (${dollarType})`;
        resultRate.textContent = `1 USD = ${(1/rate).toFixed(2)} ${fromValue}`;
    }

    // Event listeners
    amount.addEventListener('input', updateResult);
    fromCurrency.addEventListener('change', updateResult);
    toCurrency.addEventListener('change', updateResult);

    // Función para intercambiar monedas
    swapButton.addEventListener('click', function() {
        const tempValue = fromCurrency.value;
        fromCurrency.value = toCurrency.value;
        toCurrency.value = tempValue;
        updateResult();
    });

    // Inicializar
    updateResult();
}); 