# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from faker import Faker
from faker.providers import bank, misc, profile
from random import seed
from datetime import datetime, timedelta
import invoices
import pandas as pd
import json
from random import choices, randrange

MIN_INVOICE_AMOUNT = 1000.00
MAX_INVOICE_AMOUNT = 5000.00
DAYS_INVOICE_DATE_RANGE = 500
DAYS_PAYMENT_DATE_RANGE = +500
NUM_INVOICES = 10000000
NUM_CLIENTS = 5000
NUM_RECIPIENTS = 1500
NUM_AGENTS = 25

df_gtrends = pd.read_csv('amazon_5y_trends_interpolated.csv')
df_gtrends['date'] = pd.to_datetime(df_gtrends.date)

end = datetime.now()
start = end - timedelta(DAYS_INVOICE_DATE_RANGE)

end_date = end
start_date = start
# start_date = datetime.strptime(start, r'%Y%m%d')
df_gtrends = df_gtrends[df_gtrends.date >= start_date]
# end_date = datetime.strptime(end, r'%Y%m%d')
df_gtrends = df_gtrends[df_gtrends.date <= end_date]

print('Reading Google trends data to sample dates from it')
df_gtrends_1_day = pd.read_csv('amazon_trends_1_day.csv')
df_gtrends_1_day['datetime_utc'] = pd.to_datetime(df_gtrends_1_day.Time, utc=True)

new_index_second_resulution = pd.date_range(df_gtrends_1_day.datetime_utc.min(),
                                            df_gtrends_1_day.datetime_utc.max(),
                                            freq='s')
df_gtrends_1_day = df_gtrends_1_day.set_index('datetime_utc').reindex(new_index_second_resulution)
df_gtrends_1_day = df_gtrends_1_day.interpolate()
df_gtrends_1_day['time_utc'] = df_gtrends_1_day.index.time
df_gtrends_1_day = df_gtrends_1_day
df_gtrends = df_gtrends


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


def gen_invoices(fake):
    config = invoices.InvoiceConfig(DAYS_INVOICE_DATE_RANGE, DAYS_PAYMENT_DATE_RANGE, MIN_INVOICE_AMOUNT,
                                    MAX_INVOICE_AMOUNT, NUM_INVOICES, NUM_CLIENTS, NUM_RECIPIENTS, NUM_AGENTS,
                                    NUM_INVOICES)

    num_payments_arr = invoices.gen_payments_arr(config)

    amounts = invoices.gen_amounts(config)
    amount_counter = 0

    with open("output/invoices-synthetic-data100.json", "w") as file:
        amount_counter = 0
        amounts = invoices.gen_amounts(config)

        invoice_date = gen_datetime_invoice(config, df_gtrends_1_day, df_gtrends)
        r = randrange(500, 2000, 3)
        for i in range(NUM_INVOICES):
            print(str(i))
            if amount_counter == config.max_invoices:
                amount_counter = 0
                amounts = invoices.gen_amounts(config)
            if i % r == 0:
                invoice_date = gen_datetime_invoice(config, df_gtrends_1_day, df_gtrends)
                r = randrange(500, 2000, 3)
            json.dump(invoices.gen_invoice(config, i, fake, num_payments_arr, amounts[amount_counter], df_gtrends_1_day, df_gtrends, invoice_date), file)
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

    # print("Generating agents ...", NUM_AGENTS)
    # gen_agents(fake)
    # print("Done!")

    # print("Generating clients ...", NUM_CLIENTS)
    # gen_clients(fake)
    # print("Done!")

    # print("Generating recipients ...", NUM_RECIPIENTS)
    # gen_recipients(fake)
    # print("Done!")

    print("Generating invoices ... ", NUM_INVOICES)
    gen_invoices(fake)
    print("Done!")
