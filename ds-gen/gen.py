# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from faker import Faker
from faker.providers import bank, misc, profile
from random import seed
from datetime import datetime
import invoices
import numpy as np
import json

MIN_INVOICE_AMOUNT = 1000.00
MAX_INVOICE_AMOUNT = 5000.00
DAYS_INVOICE_DATE_RANGE = 365
DAYS_PAYMENT_DATE_RANGE = +365
NUM_INVOICES = 40000000
NUM_CLIENTS = 5000
NUM_RECIPIENTS = 1500
NUM_AGENTS = 25


def gen_invoices(fake):
    config = invoices.InvoiceConfig(DAYS_INVOICE_DATE_RANGE, DAYS_PAYMENT_DATE_RANGE, MIN_INVOICE_AMOUNT,
                                    MAX_INVOICE_AMOUNT, NUM_INVOICES, NUM_CLIENTS, NUM_RECIPIENTS, NUM_AGENTS,
                                    NUM_INVOICES)

    num_payments_arr = invoices.gen_payments_arr(config)

    amounts = invoices.gen_amounts(config)
    amount_counter = 0

    with open("output/invoices-synthetic-data.json", "w") as file:
        amount_counter = 0
        amounts = invoices.gen_amounts(config)

        for i in range(NUM_INVOICES):
            if amount_counter == config.max_invoices:
                amount_counter = 0
                amounts = invoices.gen_amounts(config)
            json.dump(invoices.gen_invoice(config, i, fake, num_payments_arr, amounts[amount_counter]), file)
            amount_counter = amount_counter + 1
            file.write("\n")


def gen_recipient(i, fake):
    return {
        "id": i,
        "recipient_code": fake.unique.bothify(text='?????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        "recipient_country": fake.country_code(representation='alpha-3')
    }


def gen_recipients(fake):
    with open("output/recipients-synthetic-data.json", "w") as file:
        for i in range(NUM_RECIPIENTS):
            json.dump(gen_recipient(i + 1, fake), file)
            file.write("\n")


def gen_client(i, fake):
    return {
        "id": i,
        "company_name": fake.unique.company(),
        "company_country": fake.country_code(representation='alpha-3')
    }


def gen_clients(fake):
    with open("output/clients-synthetic-data.json", "w") as file:
        for i in range(NUM_CLIENTS):
            json.dump(gen_client(i + 1, fake), file)
            file.write("\n")


def gen_agent(i, fake):
    return {
        "id": i,
        "agent_name": (fake.profile("name"))['name']
    }


def gen_agents(fake):
    with open("output/agents-synthetic-data.json", "w") as file:
        for i in range(NUM_AGENTS):
            json.dump(gen_agent(i + 1, fake), file)
            file.write("\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    seed(datetime.now())
    fake = Faker()
    fake.add_provider(bank)
    fake.add_provider(misc)
    fake.add_provider(profile)

    print("Generating agents ...", NUM_AGENTS)
    gen_agents(fake)
    print("Done!")

    #    print("Generating clients ...", NUM_CLIENTS)
    #    gen_clients(fake)
    #    print("Done!")

    #    print("Generating recipients ...", NUM_RECIPIENTS)
    #    gen_recipients(fake)
    #    print("Done!")

    print("Generating invoices ... ", NUM_INVOICES)
    gen_invoices(fake)
    print("Done!")
