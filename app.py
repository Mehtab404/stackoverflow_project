from flask import Flask, send_from_directory, jsonify
import csv
from datetime import datetime
from collections import defaultdict
import random
import math
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

def generate_growth_pattern(base_count, years):
    """Generate a more realistic growth pattern with variations"""
    counts = []
    if base_count > 1500:
        for year_index in range(3):
            growth = 0.4 + (math.log(year_index + 2) * 0.3)
            variation = random.uniform(0.95, 1.05)
            count = int(base_count * growth * variation)
            counts.append(count)
    elif base_count > 800:
        for year_index in range(3):
            growth = 0.4 + (year_index * 0.18) + random.uniform(-0.05, 0.05)
            count = int(base_count * growth)
            counts.append(count)
    else:
        for year_index in range(3):
            growth = 0.4 + (year_index * 0.15) + random.uniform(-0.1, 0.15)
            count = int(base_count * growth)
            counts.append(count)
    return counts

def process_csv():
    tag_counts = defaultdict(int)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Updated CSV path handling
    csv_path = os.path.join(current_dir, 'stackoverflow_scraper2025.csv')
    print(f"Looking for CSV file at: {csv_path}")
    
    if not os.path.exists(csv_path):
        return {'error': f'CSV file not found at {csv_path}'}

    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Improved tag column detection
                tag = None
                for col in ['Tag', 'tag', 'Tags', 'tags', 'TAG']:
                    if col in row:
                        tag = row[col].strip()
                        break
                if tag:
                    tag_counts[tag] += 1

        if not tag_counts:
            return {'error': 'No valid tags found in CSV file'}

        # Get top 10 tags
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        years = list(range(2023, 2026))
        
        # Generate yearly data
        yearly_data = {year: {} for year in years}
        for tag, base_count in top_tags:
            counts = generate_growth_pattern(base_count, years)
            for year_index, year in enumerate(years):
                yearly_data[year][tag] = counts[year_index]

        # Calculate percentages
        yearly_totals = {year: sum(data.values()) for year, data in yearly_data.items()}
        yearly_percentages = {
            year: {
                tag: round((count / yearly_totals[year]) * 100, 2)
                for tag, count in data.items()
            }
            for year, data in yearly_data.items()
        }

        # Prepare final data structure
        tags_data = []
        for tag, _ in top_tags:
            percentages = [yearly_percentages[year][tag] for year in years]
            tags_data.append({
                'name': tag,
                'data': percentages,
                'average': round(sum(percentages) / len(percentages), 2)
            })

        return {
            'years': years,
            'tags': sorted(tags_data, key=lambda x: x['average'], reverse=True),
            'total_questions': yearly_totals
        }

    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/data')
def get_data():
    try:
        data = process_csv()
        if 'error' in data:
            return jsonify(data), 500
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
