import pdfplumber
import os
import re

DATA_PATH = 'bank-statements'
PDF_ENDING = '.pdf'

def _get_year(lines):
    year_line = [line for line in lines if re.search(
        '^Kontoauszug Nummer\s\d{3}\s\/\s\d{4}\s', line)][0]
    year = year_line[25:29]
    return year


def _get_iban(lines):
    iban_line = [line for line in lines if re.search(
        '^Kontonummer\s\d{10}\s\/\sIBAN\s', line)][0]
    iban = iban_line[30:59]
    return iban


def _payment_is_outgoing(payment_type):
    ingoing_types = ['Zahlungseingang', 'Lohn, Gehalt, Rente']
    return payment_type not in ingoing_types

def _get_amount(basic_information_parts, payment_type):
    amount = basic_information_parts[len(basic_information_parts) - 1]
    amount = amount.replace('.', '')
    amount = amount.replace(',', '.')
    amount = float(amount)
    if _payment_is_outgoing(payment_type):
        amount = -amount
    return(amount)


def _get_payment_type(basic_information_parts):
    payment_type = basic_information_parts[2]
    if len(basic_information_parts) > 4:
        current_part_index = 3
        while current_part_index < (len(basic_information_parts) - 1):
            payment_type = '{} {}'.format(
                payment_type, basic_information_parts[current_part_index])
            current_part_index += 1
    return(payment_type)

def get_bank_data():
    bank_data = []
    for file_name in os.listdir(DATA_PATH):
        if file_name.endswith(PDF_ENDING):
            file_path = os.path.join(DATA_PATH, file_name)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    lines = text.split('\n')
                    if page.page_number == 1:
                        year = _get_year(lines)
                        iban = _get_iban(lines)
                    group_starts = [index for index, line in enumerate(
                        lines) if re.search('^(\d{2}(\.)){2}\s', line)]
                    for group_start in group_starts:
                        basic_information_string = lines[group_start]
                        basic_information_parts = basic_information_string.split(
                            ' ')
                        date = basic_information_parts[0]
                        date_parts = date.split('.')
                        day = date_parts[0]
                        month = date_parts[1]
                        payment_type = _get_payment_type(basic_information_parts)
                        amount = _get_amount(basic_information_parts, payment_type)
                        other_party = lines[group_start + 1]
                        bank_data.append({
                            'year': year,
                            'month': month,
                            'day': day,
                            'account': iban,
                            'other_party': other_party,
                            'payment_type': payment_type,
                            'amount': amount
                        })
    return(bank_data)
