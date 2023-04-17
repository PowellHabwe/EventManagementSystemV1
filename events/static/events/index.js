
paypal.Buttons({
    style : {
        color: 'black',
        shape: 'pill'
    },
    createOrder: function (data, actions) {
        return actions.order.create({
            purchase_units : [{
                amount: {
                    value: '60'
                }
            }]
        });
    },
    onApprove: function (data, actions) {
        return actions.order.capture().then(function (details) {
            console.log(details)
            window.location.replace("http://localhost:8000/success")
        })
    },
    onCancel: function (data) {
        window.location.replace("http://localhost:8000/cancel")
    }
}).render('#paypal-payment-button');