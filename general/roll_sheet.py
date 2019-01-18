#!/usr/bin/env python3

# Get a sheet of pre-rolled values that I can tick off during combat.
from random import randint

from fpdf import FPDF

def get_rolls(num=30, dice=[2,3,4,6,8,10,12,20,100]):
    rolls = {}
    # First, get the random ones that will help seed the rest of the rolls
    r = []
    for i in range(num):
        r.append(randint(1, 5))
        rolls["seed"] = r

    for die in dice:
        r = []
        for i in range(num):
            r.append(randint(1, die))
        rolls[die] = r

    return rolls

def output_pdf(all_rolls, fn="rolls.pdf", dice=["seed",2,3,4,6,8,10,12,20,100]):
    pdf = FPDF(orientation="L")
    pdf.set_font('Courier', size=14)
    for rolls in all_rolls:
        pdf.add_page()
        for die in dice:
            # text = str(d) + ": " + " ".join([str(x) for x in rolls[die]])
            text = str(die) + ": " + " ".join([str(x) for x in rolls[die]])
            pdf.multi_cell(w=0, h=7, txt=text, border=1)
    pdf.output(fn)

all_rolls = []
for i in range(5):
    all_rolls.append(get_rolls(num=50))

output_pdf(all_rolls)
