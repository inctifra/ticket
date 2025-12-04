export function formatCurrencyDynamic(selector = '.currency', locale = 'en-US') {
    $(selector).each(function() {
        let amount = $(this).data('amount') ?? $(this).text();
        let currency = $(this).data('currency') ?? 'USD'; // default USD
        amount = Number(amount);

        if (!isNaN(amount)) {
            const formatted = new Intl.NumberFormat(locale, {
                style: 'currency',
                currency: currency,
            }).format(amount);

            $(this).text(formatted);
        }
    });
}
