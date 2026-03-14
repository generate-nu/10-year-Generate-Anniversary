#!/usr/bin/env python3
"""
Script to analyze which Northeastern colleges applicants belong to based on their majors
"""

import pandas as pd
import os
from collections import Counter

def get_college_from_major(major_str):
    """Map major to Northeastern college"""
    if pd.isna(major_str) or major_str == "":
        return "Unknown"
    
    major_str = str(major_str).lower().strip()
    
    # Khoury College of Computer Sciences
    if any(term in major_str for term in ['computer science', 'cs', 'data science', 'artificial intelligence', 'ai', 'cybersecurity', 'software engineering', 'information systems', 'bioinformatics']):
        return "Khoury College of Computer Sciences"
    
    # College of Engineering
    elif any(term in major_str for term in ['engineering', 'mechanical', 'electrical', 'computer engineering', 'chemical', 'industrial', 'bioengineering']):
        return "College of Engineering"
    
    # D'Amore-McKim School of Business
    elif any(term in major_str for term in ['business', 'finance', 'marketing', 'entrepreneurship', 'economics', 'management', 'accounting', 'international business']):
        return "D'Amore-McKim School of Business"
    
    # College of Science
    elif any(term in major_str for term in ['biology', 'chemistry', 'physics', 'mathematics', 'math', 'behavioral neuroscience', 'psychology', 'health science']):
        return "College of Science"
    
    # College of Arts, Media and Design
    elif any(term in major_str for term in ['design', 'media', 'arts', 'interaction design', 'music', 'communications', 'journalism']):
        return "College of Arts, Media and Design"
    
    # College of Social Sciences and Humanities
    elif any(term in major_str for term in ['political science', 'law', 'philosophy', 'linguistics', 'criminal justice', 'social', 'humanities']):
        return "College of Social Sciences and Humanities"
    
    # Bouvé College of Health Sciences
    elif any(term in major_str for term in ['pharmacy', 'pharmd', 'health', 'nursing', 'public health']):
        return "Bouvé College of Health Sciences"
    
    # College of Professional Studies
    elif any(term in major_str for term in ['project management', 'professional', 'masters', 'ms', 'graduate']):
        return "College of Professional Studies"
    
    else:
        return "Unknown"

def analyze_colleges():
    """Analyze college distribution from major data"""
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'Fillout' in f]
    
    colleges = Counter()
    total_applications = 0
    
    print("Analyzing colleges from major data...")
    print("=" * 50)
    
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            
            # Find the major column
            major_col = None
            for col in df.columns:
                if 'major' in col.lower() and 's)' in col.lower():
                    major_col = col
                    break
            
            if major_col:
                print(f"Processing: {file}")
                
                for _, row in df.iterrows():
                    major_val = row[major_col]
                    college = get_college_from_major(major_val)
                    colleges[college] += 1
                    total_applications += 1
                
                print(f"  Processed {len(df)} applications")
            else:
                print(f"Skipping {file} - no major column found")
                
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    return colleges, total_applications

def main():
    colleges, total_applications = analyze_colleges()
    
    print("\n" + "=" * 60)
    print("NORTHEASTERN COLLEGES ANALYSIS")
    print("=" * 60)
    
    print(f"\nTotal Applications Analyzed: {total_applications}")
    
    print("\n🏛️ COLLEGE DISTRIBUTION:")
    print("-" * 50)
    
    # Sort colleges by count (descending)
    sorted_colleges = sorted(colleges.items(), key=lambda x: x[1], reverse=True)
    
    for college, count in sorted_colleges:
        percentage = (count / total_applications) * 100
        print(f"{college:40}: {count:3d} ({percentage:5.1f}%)")
    
    print(f"\n✅ Total Number of Different Colleges Represented: {len(colleges)}")
    
    # Count how many of the 9 Northeastern colleges are represented
    northeastern_colleges = [
        "Khoury College of Computer Sciences",
        "College of Engineering", 
        "D'Amore-McKim School of Business",
        "College of Science",
        "College of Arts, Media and Design",
        "College of Social Sciences and Humanities",
        "Bouvé College of Health Sciences",
        "College of Professional Studies",
        "Mills College at Northeastern"
    ]
    
    represented_colleges = [college for college in northeastern_colleges if college in colleges]
    print(f"✅ Number of Northeastern Colleges Represented: {len(represented_colleges)} out of 9")
    
    print("\n📊 Represented Colleges:")
    for college in represented_colleges:
        count = colleges[college]
        percentage = (count / total_applications) * 100
        print(f"  - {college}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()
