#!/bin/bash
# curl -v -X POST "https://api-m.sandbox.paypal.com/v1/oauth2/token" \
#     -u "AWKOv7j_ZEWsl1RaStutpPNcZamT8apNW9u9lW9yZrf94yi5HV7yEy2dJb-lhv1ibPgBwu4Xkd8JuCIa:EEv8bkqjlOKmXYSfC3J8YccDQWlMX8ZRLeQC3uLDbmYq7xlOZyye4CSOr1RFBfknzd85rQH1Is5Cxols" \
#     -H "Content-Type: application/x-www-form-urlencoded" \
#     -d "grant_type=client_credentials"
# curl -v -X POST https://api-m.sandbox.paypal.com/v1/catalogs/products -H "Content-Type: application/json"   -H "Authorization: Bearer A21AAJxgL3Jvw-j8ihXIQPZbIK-L5DbsdxfZaeLUAqVhWMGRcu5kde535LPAKfmNhekW7QdO5oY-kW-58HB764uAl_nM-y3JA"   -H "PayPal-Request-Id: PRODUCT-18062020-001"   -d '{"name": "Forecast football winners","description": "Forecast football winners","type": "SERVICE","category": "SOFTWARE" }'
#productd id PROD-83W24542UP825562C
curl -v -k -X POST https://api-m.sandbox.paypal.com/v1/billing/plans \
  -H "Accept: application/json" \
  -H "Authorization: Bearer A21AAJxgL3Jvw-j8ihXIQPZbIK-L5DbsdxfZaeLUAqVhWMGRcu5kde535LPAKfmNhekW7QdO5oY-kW-58HB764uAl_nM-y3JA" \
  -H "Content-Type: application/json" \
  -H "PayPal-Request-Id: PLAN-18062020-001" \
  -d '{
      "product_id": "PROD-83W24542UP825562C",
      "name": "Basic Plan",
      "description": "Basic plan",
      "billing_cycles": [
        {
          "frequency": {
            "interval_unit": "MONTH",
            "interval_count": 1
          },
          "tenure_type": "TRIAL",
          "sequence": 1,
          "total_cycles": 1
        },
        {
          "frequency": {
            "interval_unit": "MONTH",
            "interval_count": 1
          },
          "tenure_type": "REGULAR",
          "sequence": 2,
          "total_cycles": 12,
          "pricing_scheme": {
            "fixed_price": {
              "value": "10",
              "currency_code": "USD"
            }
          }
        }
      ],
      "payment_preferences": {
        "auto_bill_outstanding": true,
        "setup_fee": {
          "value": "10",
          "currency_code": "USD"
        },
        "setup_fee_failure_action": "CONTINUE",
        "payment_failure_threshold": 3
      },
      "taxes": {
        "percentage": "10",
        "inclusive": false
      }
    }'

    <div id="paypal-button-container-P-8RU57748RN9114711MP2GXBA"></div>
<script src="https://www.paypal.com/sdk/js?client-id=AdVxKNkSiLtGgXdRN9Js1Ug5NYYntesaMHat3P_m_9TSi_YCfxXTTSH0RTVShSN2wIVms1pbiBRpHKm6&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
<script>
  paypal.Buttons({
      style: {
          shape: 'pill',
          color: 'blue',
          layout: 'vertical',
          label: 'subscribe'
      },
      createSubscription: function(data, actions) {
        return actions.subscription.create({
          /* Creates the subscription */
          plan_id: 'P-8RU57748RN9114711MP2GXBA'
        });
      },
      onApprove: function(data, actions) {
        alert(data.subscriptionID); // You can add optional success message for the subscriber here
      }
  }).render('#paypal-button-container-P-8RU57748RN9114711MP2GXBA'); // Renders the PayPal button
</script>