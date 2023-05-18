import csv
from django.http import HttpResponse

def generate_payment_csv(paymentslip):
    receiver = paymentslip['receiver']
    response = HttpResponse(content_type='text/csv')
    filename_title = str(receiver) + '_KalpaLogisticsPayment.csv'
    response['Content-Disposition'] = "attachment; filename=" + filename_title

    writer = csv.writer(response)
    writer.writerow(['', '', '', 'Company:', 'Kalpa Logistics'])
    writer.writerow(['', '', '', 'Date:', paymentslip['created_at']])
    writer.writerow(['', '', '', 'Payment Related To:', paymentslip['sender']])
    writer.writerow([])
    writer.writerow([])
    writer.writerow(['S.N', 'Shipment Code', 'Customer', 'Mobile', 'Address', 'COD Amount', 'Status',
                     'Delivery Charge', 'COD Handling', 'Rejection', 'Delivered Amount'])

    a = 1
    for ship in paymentslip['shipments']:
        if ship['mode_of_payment'] == 'Already Paid':
            parcel_total = 0
            cod_handling_charge = 0
        else:
            parcel_total = ship['parcel_total']
            cod_handling_charge = ship['cod_handling_charge']
        if ship['shipment_status'] == 'Parcel Delivered':
            rejection_charge = 0
            delivered_amount = ship['parcel_total']
        else:
            rejection_charge = ship['rejection_handling_charge']
            delivered_amount = 0

        writer.writerow([a, ship['shipment_code'], ship['receiver_name'], ship['receiver_contact'],
                         ship['dropoff_street_address'], parcel_total, ship['shipment_status'], 
                         ship['shipping_charge'], cod_handling_charge, rejection_charge, delivered_amount])
        a += 1

    writer.writerow(['', '', '', '', '', '', '', 'TOTAL SHIPPING CHARE', paymentslip['shipping_charge']])
    writer.writerow(['', '', '', '', '', '', '', 'COD HANDLING', paymentslip['cod_handling_charge']])
    writer.writerow(['', '', '', '', '', '', '', 'REJECTION', paymentslip['rejection_handling_charge']])
    writer.writerow(['', '', '', '', '', '', '', 'TOTAL SERVICE CHARGE', paymentslip['total_shipping_amount']])
    writer.writerow(['', '', '', '', '', '', '', 'TOTAL COD AMT', paymentslip['cod_amount']])
    writer.writerow(['', '', '', '', '', '', '', 'NET AMOUNT', paymentslip['net_payable_amount']])

    return response
paymentslip = {
    "receiver": "John Doe",
    "created_at": "2022-03-09",
    "sender": "Jane Doe",
    "shipments": [
        {
            "shipment_code": "SHIP1",
            "receiver_name": "John Doe",
            "receiver_contact": "1234567890",
            "dropoff_street_address": "123 Main St.",
            "mode_of_payment": "Cash on Delivery",
            "parcel_total": 1000,
            "shipment_status": "Parcel Delivered",
            "shipping_charge": 50,
            "cod_handling_charge": 20,
            "rejection_handling_charge": 0
        },
        {
            "shipment_code": "SHIP2",
            "receiver_name": "John Doe",
            "receiver_contact": "1234567890",
            "dropoff_street_address": "456 Main St.",
            "mode_of_payment": "Already Paid",
            "parcel_total": 500,
            "shipment_status": "In Transit",
            "shipping_charge": 25,
            "cod_handling_charge": 0,
            "rejection_handling_charge": 10
        }
    ],
    "shipping_charge": 75,
    "cod_handling_charge": 20,
    "rejection_handling_charge": 10,
    "total_shipping_amount": 100,
    "cod_amount": 1500,
    "net_payable_amount": 1600
}

generate_payment_csv(paymentslip)