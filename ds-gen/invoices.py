# Functions for generating synthetic invoices data

from faker import Faker
from faker.providers import bank, misc
from random import randint, seed, random, choice, choices
import numpy as np
import pandas as pd
from typing import NamedTuple
from datetime import datetime, timedelta


class InvoiceConfig(NamedTuple):
    days_invoice_date_range: int
    days_payment_date_range: int
    min_invoice_amount: float
    max_invoice_amount: float
    num_records: int
    max_clients: int
    max_recipients: int
    max_agents: int
    max_invoices: int


def gen_datetime_invoice(config, df_gtrends_1_day, df_gtrends):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    time = choices(df_gtrends_1_day['time_utc'].values,
                                        weights=df_gtrends_1_day['amazon: (United States)'].values,
                                        k=1)
    date = choices(df_gtrends['date'].values,
                                        weights=df_gtrends['amazon'].values,
                                        k=1)
    d = pd.to_datetime(str(date[0]))
    # date = d.strftime('%Y-%m-%d') + ' ' + time[0].strftime('%H:%M:%S')
    return d.combine(d, time[0])

    # end = datetime.now()
    # start = end - timedelta(config.days_invoice_date_range)
    # return start + (end - start) * random()


def gen_datetime_payment(invoice_date, config):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    # payment dates must always be after the invoice date

    start = invoice_date
    end = start + timedelta(config.days_payment_date_range)
    return start + (end - start) * random()


def gen_amounts(config):
    return np.random.gamma(2, 2, config.max_invoices)


def gen_payments_arr(config):
    num_payments = [1, 2, 3, 4, 5]
    prob = [0.245, 0.6, 0.1, 0.05, 0.005]
    return np.random.choice(num_payments, config.num_records, prob)


def gen_payments(config, invoice_id, invoice_date, fake, num_payments_arr):
    payments = []
    for _ in range(np.take(num_payments_arr, invoice_id)):
        payments.append({
            "payment_id": fake.uuid4(),
            "type": choice(["MANUAL", "LIVE"]),
            "added_at": gen_datetime_payment(invoice_date, config).isoformat()
        })

    return payments


def gen_invoice(config, i, fake, num_payments_arr, amount, df_gtrends_1_day, df_gtrends, invoice_date):
    # invoice_date = gen_datetime_invoice(config, df_gtrends_1_day, df_gtrends)
    return {
        "id": i+1,
        "agent_id": randint(1, 25),
        "recipient_code": fake.random_int(min=1, max=config.max_recipients, step=1),
        "client_id": fake.random_int(min=1, max=config.max_clients, step=1),
        "amount": amount,
        "currency": choice(["EUR", "GBP", "USD"]),
        "added_payments": gen_payments(config, i, invoice_date, fake, num_payments_arr),
        "created_at": invoice_date.isoformat()
    }
