# Synthetic Data Generator for invoices

With this script you will be able to generate a synthetic dataset for the Firewire PoC. It generates three files in the output directory: 
- clients.json
- recipients.json
- invoices.json

To run the script and generate the source dataset:

- Create the virtual environment:

```
python3 -mvenv .e
source .e/bin/activate
pip install -r requirements.txt
```

- Run the script

```
./gen.py
```

## Tuning Dataset

At the beginning of the script you can find a set of parameters to configure your generated dataset. 

- The invoice amount value is uniformly distributed between MIN_INVOICE_AMOUNT and MAX_INVOICE_AMOUNT
- Invoices' dates are distributed during the last year, starting on current date. Date range is defined in days so you can easly change it using DAYS_INVOICE_DATE_RANGE
- Invoices' payments are distributed during the following year. This range can be easily changed using DAYS_PAYMENT_DATE_RANGE
- NUM_INVOICES sets the number of invoices to generate
- NUM_CLIENTS sets the number of clients to generate
- NUM_RECIPIENTS sets the number of recipients to generate
- NUM_AGENTS sets the number of agents. It is used to generate the agent_id of the invoice. This value is uniformly distributed between 1 and NUM_AGENTS.

## Data Examples

Generated files has the following structure.

### Invoice

The field added_payments range from 1 to 5 being most probable to have 1 or 2 payments.

```json
{
    "id": 1,
    "agent_id": 10,
    "recipient_code": 6,
    "client_id": 2,
    "amount": 4765.5,
    "currency": "EUR",
    "added_payments": [{
        "payment_id": "a03547bf-fa83-42c9-b996-e3bdf291328b",
        "type": "LIVE",
        "added_at": "2020-07-15T09:08:07.904004"
    }, {
        "payment_id": "65866d56-3136-47c4-a6a0-c8d48c941bd6",
        "type": "MANUAL",
        "added_at": "2020-05-25T01:53:20.836004"
    }, {
        "payment_id": "6f719100-a1ed-4489-8daa-8ec72277539c",
        "type": "LIVE",
        "added_at": "2020-05-20T20:16:34.733417"
    }, {
        "payment_id": "70e9e4bd-0526-45b5-9c08-e334d64aa12a",
        "type": "MANUAL",
        "added_at": "2020-03-04T09:00:32.743273"
    }],
    "created_at": "2020-02-12T09:09:58.641100"
}
```

### Client

```json
{
    "id": 2,
    "company_name": "Walters-Davis",
    "company_country": "KWT"
}
```

### Recipient

```json
{
    "id": 9,
    "recipient_code": "MOIGV",
    "recipient_country": "DMA"
}
```
