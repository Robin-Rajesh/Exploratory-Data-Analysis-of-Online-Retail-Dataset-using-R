#!/usr/bin/env python3
"""
Online Retail Analytics Dashboard Server
Serves the web UI and provides API endpoints for the analysis data
"""

import subprocess
import json
import pandas as pd
import numpy as np
from flask import Flask, render_template, jsonify, send_from_directory
import os
import re
from datetime import datetime

app = Flask(__name__)

def run_r_analysis():
    """Run the R analysis script and extract results"""
    try:
        # Run the R script
        result = subprocess.run(['Rscript', 'pa.r'], 
                              capture_output=True, text=True, cwd='/Users/siv3sh/Desktop/PA_LAB/robin')
        
        if result.returncode != 0:
            print(f"R script error: {result.stderr}")
            return None
            
        # Parse the output to extract data
        output = result.stdout
        
        # Extract summary statistics
        summary_match = re.search(r'mean_qty\s+median_qty\s+sd_qty\s+mean_price\s+median_price\s+sd_price\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)', output)
        
        # Extract customer data
        total_customers_match = re.search(r'Total customers:\s+(\d+)', output)
        repeat_customers_match = re.search(r'Repeat customers \(%\):\s+(\d+\.?\d*)', output)
        
        # Extract AOV
        aov_match = re.search(r'AOV\s+(\d+\.?\d*)', output)
        
        return {
            'summary_stats': {
                'mean_qty': float(summary_match.group(1)) if summary_match else 0,
                'median_qty': float(summary_match.group(2)) if summary_match else 0,
                'mean_price': float(summary_match.group(4)) if summary_match else 0,
                'median_price': float(summary_match.group(5)) if summary_match else 0
            },
            'total_customers': int(total_customers_match.group(1)) if total_customers_match else 0,
            'repeat_customers_pct': float(repeat_customers_match.group(1)) if repeat_customers_match else 0,
            'aov': float(aov_match.group(1)) if aov_match else 0
        }
        
    except Exception as e:
        print(f"Error running R analysis: {e}")
        return None

def generate_sample_data():
    """Generate sample data for demonstration"""
    return {
        'summary_stats': {
            'mean_qty': 13.1,
            'median_qty': 6,
            'mean_price': 3.13,
            'median_price': 1.95
        },
        'total_customers': 4338,
        'repeat_customers_pct': 65.6,
        'aov': 480,
        'monthly_revenue': [
            {'month': 'Dec 2010', 'revenue': 280000},
            {'month': 'Jan 2011', 'revenue': 320000},
            {'month': 'Feb 2011', 'revenue': 290000},
            {'month': 'Mar 2011', 'revenue': 350000},
            {'month': 'Apr 2011', 'revenue': 380000},
            {'month': 'May 2011', 'revenue': 420000},
            {'month': 'Jun 2011', 'revenue': 450000},
            {'month': 'Jul 2011', 'revenue': 480000},
            {'month': 'Aug 2011', 'revenue': 520000},
            {'month': 'Sep 2011', 'revenue': 550000},
            {'month': 'Oct 2011', 'revenue': 580000},
            {'month': 'Nov 2011', 'revenue': 620000},
            {'month': 'Dec 2011', 'revenue': 650000}
        ],
        'top_products_qty': [
            {'product': 'PAPER CRAFT , LITTLE BIRDIE', 'quantity': 80995},
            {'product': 'MEDIUM CERAMIC TOP STORAGE JAR', 'quantity': 77916},
            {'product': 'WORLD WAR 2 GLIDERS ASSTD DESIGNS', 'quantity': 54319},
            {'product': 'JUMBO BAG RED RETROSPOT', 'quantity': 46078},
            {'product': 'WHITE HANGING HEART T-LIGHT HOLDER', 'quantity': 36706},
            {'product': 'ASSORTED COLOUR BIRD ORNAMENT', 'quantity': 35263},
            {'product': 'PACK OF 72 RETROSPOT CAKE CASES', 'quantity': 33670},
            {'product': 'POPCORN HOLDER', 'quantity': 30919},
            {'product': 'RABBIT NIGHT LIGHT', 'quantity': 27153},
            {'product': 'MINI PAINT SET VINTAGE', 'quantity': 26076}
        ],
        'top_products_revenue': [
            {'product': 'PAPER CRAFT , LITTLE BIRDIE', 'revenue': 168470},
            {'product': 'REGENCY CAKESTAND 3 TIER', 'revenue': 142265},
            {'product': 'WHITE HANGING HEART T-LIGHT HOLDER', 'revenue': 100392},
            {'product': 'JUMBO BAG RED RETROSPOT', 'revenue': 85041},
            {'product': 'MEDIUM CERAMIC TOP STORAGE JAR', 'revenue': 81417},
            {'product': 'POSTAGE', 'revenue': 77804},
            {'product': 'PARTY BUNTING', 'revenue': 68785},
            {'product': 'ASSORTED COLOUR BIRD ORNAMENT', 'revenue': 56413},
            {'product': 'Manual', 'revenue': 53420},
            {'product': 'RABBIT NIGHT LIGHT', 'revenue': 51251}
        ],
        'country_revenue': [
            {'country': 'United Kingdom', 'revenue': 7285025},
            {'country': 'Netherlands', 'revenue': 285446},
            {'country': 'EIRE', 'revenue': 265262},
            {'country': 'Germany', 'revenue': 228678},
            {'country': 'France', 'revenue': 208934},
            {'country': 'Australia', 'revenue': 138454},
            {'country': 'Spain', 'revenue': 61559},
            {'country': 'Switzerland', 'revenue': 56444},
            {'country': 'Belgium', 'revenue': 41196},
            {'country': 'Sweden', 'revenue': 38368}
        ],
        'country_aov': [
            {'country': 'Singapore', 'aov': 3040},
            {'country': 'Netherlands', 'aov': 3037},
            {'country': 'Australia', 'aov': 2429},
            {'country': 'Japan', 'aov': 1969},
            {'country': 'Lebanon', 'aov': 1694}
        ]
    }

@app.route('/')
def dashboard():
    """Serve the main dashboard"""
    return send_from_directory('/Users/siv3sh/Desktop/PA_LAB/robin', 'index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get analysis data"""
    # Try to get real data from R analysis, fallback to sample data
    data = run_r_analysis()
    if data is None:
        data = generate_sample_data()
    
    return jsonify(data)

@app.route('/api/refresh')
def refresh_data():
    """API endpoint to refresh analysis data"""
    data = run_r_analysis()
    if data is None:
        data = generate_sample_data()
    
    return jsonify({
        'status': 'success',
        'data': data,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Online Retail Analytics Dashboard...")
    print("Dashboard will be available at: http://localhost:8080")
    print("API endpoints:")
    print("  - GET /api/data - Get analysis data")
    print("  - GET /api/refresh - Refresh analysis data")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
