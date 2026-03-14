#!/usr/bin/env python3
"""
Script to analyze Generate application CSV files and extract:
1. Academic year distribution (freshmen, sophomore, junior, senior, 5th year, masters 1st, masters 2nd)
2. Major distribution (CS, Business Administration, CS + Business Administration as separate categories)
"""

import pandas as pd
import os
import re
from collections import defaultdict, Counter

def normalize_academic_year(year_str):
    """Normalize academic year strings to standard categories"""
    if pd.isna(year_str) or year_str == "":
        return "Unknown"
    
    year_str = str(year_str).lower().strip()
    
    # Check for masters first (more specific patterns)
    if any(term in year_str for term in ['masters 1st', 'masters first', 'm1', 'master 1st', 'last year of masters']):
        return "Masters 1st"
    elif any(term in year_str for term in ['masters 2nd', 'masters second', 'm2', 'master 2nd']):
        return "Masters 2nd"
    elif 'master' in year_str:
        return "Masters (unspecified)"
    
    # Handle numeric values - need to check if they're in masters context
    # For now, we'll assume single digits could be either undergrad or masters
    # We'll need to cross-reference with major information for better accuracy
    
    # Map various year formats to standard categories
    if any(term in year_str for term in ['freshman', '1st', 'first']):
        return "Freshman"
    elif any(term in year_str for term in ['sophomore', '2nd', 'second']):
        return "Sophomore"
    elif any(term in year_str for term in ['junior', '3rd', 'third']):
        return "Junior"
    elif any(term in year_str for term in ['senior', '4th', 'fourth']):
        return "Senior"
    elif any(term in year_str for term in ['5th', 'fifth']):
        return "5th Year"
    else:
        return "Other"

def normalize_major(major_str):
    """Normalize major strings to show all majors"""
    if pd.isna(major_str) or major_str == "":
        return "Unknown"
    
    major_str = str(major_str).strip()
    
    # Check for CS + Business Administration combination first (treat as one combined major)
    if ('computer science' in major_str.lower() and 'business' in major_str.lower()) or \
       ('cs' in major_str.lower() and 'business' in major_str.lower()) or \
       ('computer science' in major_str.lower() and 'administration' in major_str.lower()):
        return "CS + Business Administration"
    
    # Return the major as-is for all other cases (showing all majors)
    else:
        return major_str

def analyze_csv_files():
    """Analyze all CSV files in the directory"""
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'Fillout' in f]
    
    academic_years = Counter()
    majors = Counter()
    total_applications = 0
    
    print("Analyzing CSV files...")
    print("=" * 50)
    
    for file in csv_files:
        print(f"\nProcessing: {file}")
        try:
            df = pd.read_csv(file)
            
            # Find the relevant columns
            year_col = None
            major_col = None
            
            for col in df.columns:
                if 'year' in col.lower() and 'september' in col.lower():
                    year_col = col
                elif 'major' in col.lower() and 's)' in col.lower():
                    major_col = col
            
            if year_col and major_col:
                print(f"  Found columns: '{year_col}' and '{major_col}'")
                
                # Process each row to get both year and major for better classification
                for _, row in df.iterrows():
                    year_val = row[year_col]
                    major_val = row[major_col]
                    
                    # Normalize major first
                    normalized_major = normalize_major(major_val)
                    majors[normalized_major] += 1
                    
                    # Normalize year, but also check if it's a masters student based on major
                    normalized_year = normalize_academic_year_with_major(year_val, major_val)
                    academic_years[normalized_year] += 1
                
                total_applications += len(df)
                print(f"  Processed {len(df)} applications")
            else:
                print(f"  Skipping - missing required columns")
                
        except Exception as e:
            print(f"  Error processing {file}: {e}")
    
    return academic_years, majors, total_applications

def normalize_academic_year_with_major(year_str, major_str):
    """Normalize academic year strings with context from major information"""
    if pd.isna(year_str) or year_str == "":
        return "Unknown"
    
    year_str = str(year_str).lower().strip()
    major_str = str(major_str).lower().strip() if not pd.isna(major_str) else ""
    
    # Check for masters first (more specific patterns)
    if any(term in year_str for term in ['masters 1st', 'masters first', 'm1', 'master 1st', 'last year of masters']):
        return "Masters 1st"
    elif any(term in year_str for term in ['masters 2nd', 'masters second', 'm2', 'master 2nd']):
        return "Masters 2nd"
    elif 'master' in year_str:
        return "Masters (unspecified)"
    
    # Check if major indicates graduate program
    is_graduate_major = any(term in major_str for term in ['ms', 'master', 'masters', 'graduate'])
    
    # Handle numeric values with context
    if year_str == "1":
        if is_graduate_major:
            return "Masters 1st"
        else:
            return "Freshman"
    elif year_str == "2":
        if is_graduate_major:
            return "Masters 2nd"
        else:
            return "Sophomore"
    
    # Map various year formats to standard categories
    if any(term in year_str for term in ['freshman', '1st', 'first']):
        return "Freshman"
    elif any(term in year_str for term in ['sophomore', '2nd', 'second']):
        return "Sophomore"
    elif any(term in year_str for term in ['junior', '3rd', 'third']):
        return "Junior"
    elif any(term in year_str for term in ['senior', '4th', 'fourth']):
        return "Senior"
    elif any(term in year_str for term in ['5th', 'fifth']):
        return "5th Year"
    else:
        return "Other"

def main():
    academic_years, majors, total_applications = analyze_csv_files()
    
    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    
    print(f"\nTotal Applications Analyzed: {total_applications}")
    
    print("\n📚 ACADEMIC YEAR DISTRIBUTION:")
    print("-" * 40)
    year_order = ["Freshman", "Sophomore", "Junior", "Senior", "5th Year", "Masters 1st", "Masters 2nd", "Masters (unspecified)", "Other", "Unknown"]
    
    for year in year_order:
        if year in academic_years:
            count = academic_years[year]
            percentage = (count / total_applications) * 100
            print(f"{year:20}: {count:3d} ({percentage:5.1f}%)")
    
    print("\n🎓 MAJOR DISTRIBUTION (ALL MAJORS):")
    print("-" * 50)
    
    # Sort majors by count (descending)
    sorted_majors = sorted(majors.items(), key=lambda x: x[1], reverse=True)
    
    for major, count in sorted_majors:
        percentage = (count / total_applications) * 100
        print(f"{major:40}: {count:3d} ({percentage:5.1f}%)")
    
    # Summary for the specific requirements
    print("\n" + "=" * 60)
    print("SUMMARY FOR REQUIREMENTS")
    print("=" * 60)
    
    print("\n✅ Academic Years (7 categories):")
    for year in ["Freshman", "Sophomore", "Junior", "Senior", "5th Year", "Masters 1st", "Masters 2nd"]:
        count = academic_years.get(year, 0)
        print(f"  - {year}: {count}")
    
    print(f"\n✅ Total Number of Different Majors: {len(majors)}")
    print("\n📊 Top 10 Most Common Majors:")
    for i, (major, count) in enumerate(sorted_majors[:10], 1):
        percentage = (count / total_applications) * 100
        print(f"  {i:2d}. {major}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()
