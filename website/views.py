from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for
import pandas as pd
import re

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    data = current_app.config['DATA']
    results = None
    searched = False
    part_number = None
    drawn_or_welded = None
    bracket = None
    pigtail = None

    # Cleaning
    data['Part Number'] = data['Part Number'].astype('string').str.strip()
    data['Drawn or Welded'] = data['Drawn or Welded'].astype('string').str.strip()
    data['Bracket'] = data['Bracket'].astype('string').str.strip()
    data['Pigtail'] = data['Pigtail'].astype('string').str.strip()

    part_numbers_list = data['Part Number'].dropna().unique()
    drawn_or_welded_list = data['Drawn or Welded'].dropna().unique()
    bracket_list = data['Bracket'].dropna().unique()
    pigtail_list = data['Pigtail'].dropna().unique()

    # Drop-down part number sort
    part_numbers_list = [str(pn).strip() for pn in part_numbers_list if str(pn).strip() != '']

    def sort_part_numbers(s):
        s = s.strip()
        if not s:
            return (float('inf'), '')
        first_char = s[0]
        if first_char.isdigit():
            match = re.match(r'^(\d+)', s)
            if match:
                num = int(match.group(1))
                return (0, num, s) 
            else:
                return (1, s.lower()) 
        else:
            return (1, s.lower())
    
    sorted_part_numbers = sorted(part_numbers_list, key=sort_part_numbers)

    if request.method == 'POST':
        part_number = request.form.get('part_number').strip()
        drawn_or_welded = request.form.get('drawn_or_welded', '').strip()
        bracket = request.form.get('bracket', '').strip()
        pigtail = request.form.get('pigtail', '').strip()
        searched = True

        # Target row
        target_row = data[data['Part Number'] == part_number]
        if not target_row.empty:
            target_row = target_row.iloc[0]

            mask = (
                (data['Brand'] == target_row['Brand']) &
                (data['Subcategory'] == target_row['Subcategory']) &
                (data['Shape'] == target_row['Shape']) &
                (data['Size'] == target_row['Size']) &
                (data['Depth/Heights'] == target_row['Depth/Heights'])
            )

            clamp_value = target_row['Clamp']
            # Clamp is null
            if pd.isna(clamp_value) or clamp_value == '':
                mask &= (
                    (data['Clamp'].isna() | (data['Clamp'] == '')) &
                    (data['KO Type'] == target_row['KO Type']) &
                    (data['KO Max_Size'] == target_row['KO Max_Size']) &
                    (data['Capacity (CUBIC INCHES)'] == target_row['Capacity (CUBIC INCHES)'])
                )
            # Clamp is MC/NM
            else:
                mask &= (
                    (data['Clamp'] == clamp_value) &
                    (data['Capacity (CUBIC INCHES)'] == target_row['Capacity (CUBIC INCHES)'])
                )
            
            # Optional filter
            if drawn_or_welded:
                mask &= (data['Drawn or Welded'] == drawn_or_welded)
            if bracket:
                mask &= (data['Bracket'] == bracket)
            if pigtail:
                mask &= (data['Pigtail'] == pigtail)

            results = data[mask]

            results = results.fillna('')
        else:
            # No part number found
            results = pd.DataFrame()  #null df

    return render_template(
        'home.html',
        results=results,
        part_number=part_number,
        searched=searched,
        part_numbers_list=sorted_part_numbers,
        drawn_or_welded=drawn_or_welded,
        drawn_or_welded_list=drawn_or_welded_list,
        bracket=bracket,
        bracket_list=bracket_list,
        pigtail=pigtail,
        pigtail_list=pigtail_list
    )