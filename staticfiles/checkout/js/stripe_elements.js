/* Code snippet from Boutique Ado */
/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var productClientSecret = $('#id_product_client_secret').text().slice(1, -1);
var subscriptionClientSecret = $('#id_subscription_client_secret').text().slice(1, -1);

var stripe = Stripe(stripePublicKey);
var productElements = stripe.elements();
var subscriptionElements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
// Mount the card element for product payments if it exists
var productCardElement = document.getElementById('product-card-element');
if (productCardElement) {
    var productCard = productElements.create('card', { style: style });
    productCard.mount('#product-card-element');

    // Handle realtime validation errors on the card element
    productCard.addEventListener('change', function (event) {
        var errorDiv = document.getElementById('product-card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });
}

// Mount the card element for subscription payments if it exists
var subscriptionCardElement = document.getElementById('subscription-card-element');
if (subscriptionCardElement) {
    // Mount the card element for subscription payments
    var subscriptionCard = subscriptionElements.create('card', { style: style });
    subscriptionCard.mount('#subscription-card-element');

    subscriptionCard.addEventListener('change', function (event) {
        var errorDiv = document.getElementById('subscription-card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });
}

// Handle form submissions
['product-payment-form', 'subscription-payment-form'].forEach(function(formId) {
    var form = document.getElementById(formId);
    if (!form) return;
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();

        var isSubscription = formId === 'subscription-payment-form';
        var card = isSubscription ? subscriptionCard : productCard;
        card.update({ 'disabled': true });
        $('#submit-button').attr('disabled', true);
        $(form).fadeToggle(100);
        $('#loading-overlay').fadeToggle(100);

        var saveInfo = Boolean($('#id-save-info').attr('checked'));
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var clientSecret = isSubscription ? subscriptionClientSecret : productClientSecret;

        if (!isSubscription) {
            var postData = {
                'csrfmiddlewaretoken': csrfToken,
                'product_client_secret': productClientSecret,
                'save_info': saveInfo,
            };
        } else {
            var postData = {
                'csrfmiddlewaretoken': csrfToken,
                'subscription_client_secret': subscriptionClientSecret,
                'save_info': saveInfo,
            };
        }
        var url = '/checkout/cache_checkout_data/';

        // Prepare billing details
        var billingDetails = {
            name: $.trim(form.full_name.value),
            email: $.trim(form.email.value),
        };
        if (!isSubscription) {
            billingDetails.phone = $.trim(form.phone_number.value);
            billingDetails.address = {
                line1: $.trim(form.street_address1.value),
                line2: $.trim(form.street_address2.value),
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                state: $.trim(form.county.value),
            };
        }

        $.post(url, postData).done(function () {
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: billingDetails
                },
                shipping: !isSubscription ? {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        postal_code: $.trim(form.postcode.value),
                        state: $.trim(form.county.value),
                    }
                } : undefined,
            }).then(function(result) {
                if (result.error) {
                    var errorDiv = document.getElementById(isSubscription ? 'subscription-card-errors' : 'product-card-errors');
                    var html = `
                        <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                        </span>
                        <span>${result.error.message}</span>`;
                    $(errorDiv).html(html);
                    $(form).fadeToggle(100);
                    $('#loading-overlay').fadeToggle(100);
                    card.update({ 'disabled': false });
                    $('#submit-button').attr('disabled', false);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }
            });
        }).fail(function () {
            location.reload();
        })
    });
});
