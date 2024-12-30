document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('converterForm');
    const amount = document.getElementById('amount');
    const fromCurrency = document.getElementById('fromCurrency');
    const toCurrency = document.getElementById('toCurrency');
    const swapButton = document.getElementById('swapButton');
    const resultAmount = document.getElementById('resultAmount');
    const resultRate = document.getElementById('resultRate');

    // Función para obtener las cotizaciones actuales
    async function getCotizaciones() {
        try {
            const response = await fetch('/api/cotizaciones');
            const data = await response.json();
            return data.dollar_quotes;
        } catch (error) {
            console.error('Error al obtener cotizaciones:', error);
            return null;
        }
    }

    // Función para calcular las tasas basadas en las cotizaciones
    function calculateRates(cotizaciones) {
        const rates = {};
        const dollarTypes = {
            'BLUE': 'Dólar Blue',
            'OFICIAL': 'Dólar Oficial',
            'CRYPTO': 'Dólar Cripto',
            'TARJETA': 'Dólar Tarjeta',
            'MEP': 'Dólar MEP',
            'CCL': 'Dólar CCL'
        };

        // Crear tasas para ARS a USD y viceversa
        for (const [key, name] of Object.entries(dollarTypes)) {
            if (cotizaciones[name]) {
                const venta = parseFloat(cotizaciones[name].Venta);
                rates[`ARS_${key}`] = 1/venta;
                rates[`${key}_ARS`] = venta;
            }
        }

        return rates;
    }

    const currencyNames = {
        'ARS': 'Peso Argentino',
        'BLUE': 'Dólar Blue',
        'OFICIAL': 'Dólar Oficial',
        'CRYPTO': 'Dólar Cripto',
        'TARJETA': 'Dólar Tarjeta',
        'MEP': 'Dólar MEP',
        'CCL': 'Dólar CCL'
    };

    function initializeSelectors() {
        fromCurrency.innerHTML = '';
        toCurrency.innerHTML = '';

        const arsOption = new Option(currencyNames['ARS'], 'ARS');
        fromCurrency.add(arsOption);

        ['BLUE', 'OFICIAL', 'CRYPTO', 'TARJETA', 'MEP', 'CCL'].forEach(currency => {
            const option = new Option(currencyNames[currency], currency);
            toCurrency.add(option);
        });

        fromCurrency.value = 'ARS';
        toCurrency.value = 'BLUE';
    }

    async function updateResult() {
        const fromValue = fromCurrency.value;
        const toValue = toCurrency.value;
        const amountValue = parseFloat(amount.value);

        const cotizaciones = await getCotizaciones();
        if (!cotizaciones) return;

        const rates = calculateRates(cotizaciones);
        const rateKey = `${fromValue}_${toValue}`;
        const rate = rates[rateKey];
        
        if (rate) {
            const result = amountValue * rate;
            resultAmount.textContent = `1 ${currencyNames[toValue]} = $${(1/rate).toFixed(2)} Peso Argentino`;
            resultRate.textContent = '';
        }
    }

    // Event listeners
    amount.addEventListener('input', updateResult);
    fromCurrency.addEventListener('change', updateResult);
    toCurrency.addEventListener('change', updateResult);

    swapButton.addEventListener('click', () => {
        const fromValue = fromCurrency.value;
        const toValue = toCurrency.value;

        fromCurrency.innerHTML = '';
        const newFromOption = new Option(currencyNames[toValue], toValue);
        fromCurrency.add(newFromOption);

        toCurrency.innerHTML = '';
        const newToOption = new Option(currencyNames[fromValue], fromValue);
        toCurrency.add(newToOption);

        updateResult();
    });

    // Inicializar
    initializeSelectors();
    updateResult();
});