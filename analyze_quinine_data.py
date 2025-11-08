#!/usr/bin/env python3
"""
Complete analysis script for Quinine Fluorescence Experiment
Based on CHEM30110 Experiment 1 requirements
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import glob

def read_fluorescence_csv(filepath):
    """
    Read fluorescence CSV and extract intensity at emission maximum (~450 nm)
    Returns the maximum intensity value and its wavelength
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Get label and data
    label = lines[0].strip().split(',')[0]

    # Parse data (skip first 2 lines: label and headers)
    wavelengths = []
    intensities = []

    for line in lines[2:]:
        parts = line.strip().split(',')
        if len(parts) >= 2 and parts[0] and parts[1]:
            try:
                wl = float(parts[0])
                intensity = float(parts[1])
                wavelengths.append(wl)
                intensities.append(intensity)
            except ValueError:
                break  # Stop when we hit metadata

    if not intensities:
        return label, 0, 0

    # Find maximum intensity around 450 nm (emission maximum for quinine)
    # Look in range 440-460 nm
    max_intensity = 0
    max_wavelength = 0

    for wl, intensity in zip(wavelengths, intensities):
        if 440 <= wl <= 460:
            if intensity > max_intensity:
                max_intensity = intensity
                max_wavelength = wl

    # If no peak found in that range, use global maximum
    if max_intensity == 0:
        max_idx = np.argmax(intensities)
        max_intensity = intensities[max_idx]
        max_wavelength = wavelengths[max_idx]

    return label, max_wavelength, max_intensity

def main():
    print("="*80)
    print("QUININE FLUORESCENCE ANALYSIS - EXPERIMENT 1")
    print("="*80)

    # Define concentrations based on the experiment design
    # From PDF: 6 standards evenly spaced from 0.02 to 2 ppm
    # Based on intensity trends (higher intensity = lower concentration)
    # A7, B7, C7 are marked as 1ppm
    concentrations = {
        '1': 2.0,   # A1, B1, C1 (lowest intensity)
        '2': 1.6,   # A2, B2, C2
        '3': 1.2,   # A3, B3, C3
        '4': 0.8,   # A4, B4, C4
        '5': 0.4,   # A5, B5, C5
        '6': 0.02,  # A6, B6, C6 (highest intensity)
        '7_1ppm': 1.0  # A7_1ppm, B7_1ppm, C7_1ppm (verification sample)
    }

    # Read blank
    blank_label, blank_wl, blank_intensity = read_fluorescence_csv('blank .csv')
    print(f"\nBlank intensity at {blank_wl:.1f} nm: {blank_intensity:.2f}")

    # Read all standard samples
    data_dict = {}

    for set_letter in ['A', 'B', 'C']:
        for conc_key in concentrations.keys():
            if conc_key == '7_1ppm':
                filename = f"{set_letter}7_1ppm.csv"
            else:
                filename = f"{set_letter}{conc_key}.csv"

            label, wl, intensity = read_fluorescence_csv(filename)
            corrected_intensity = intensity - blank_intensity

            conc = concentrations[conc_key]
            if conc not in data_dict:
                data_dict[conc] = []

            data_dict[conc].append({
                'sample': label,
                'wavelength': wl,
                'raw_intensity': intensity,
                'corrected_intensity': corrected_intensity
            })

            print(f"{filename}: λ_max={wl:.1f} nm, I={intensity:.2f}, I_corrected={corrected_intensity:.2f}")

    # Create DataFrame for analysis
    analysis_data = []
    for conc in sorted(data_dict.keys()):
        intensities = [d['corrected_intensity'] for d in data_dict[conc]]
        mean_int = np.mean(intensities)
        std_int = np.std(intensities, ddof=1)
        se_int = std_int / np.sqrt(len(intensities))

        analysis_data.append({
            'Concentration (ppm)': conc,
            'Intensity 1': intensities[0],
            'Intensity 2': intensities[1],
            'Intensity 3': intensities[2],
            'Mean': mean_int,
            'SD': std_int,
            'SE': se_int
        })

    df_analysis = pd.DataFrame(analysis_data)

    print("\n" + "="*80)
    print("TABLE 1: Corrected Intensity Values (Background Subtracted)")
    print("="*80)
    print(df_analysis.to_string(index=False))

    # Linear regression for calibration curve
    concentrations_array = df_analysis['Concentration (ppm)'].values
    means_array = df_analysis['Mean'].values

    # Perform linear regression using all data points (not just means)
    all_concs = []
    all_intensities = []
    for conc in sorted(data_dict.keys()):
        for d in data_dict[conc]:
            all_concs.append(conc)
            all_intensities.append(d['corrected_intensity'])

    all_concs = np.array(all_concs)
    all_intensities = np.array(all_intensities)

    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(all_concs, all_intensities)

    # LINEST equivalent - get more detailed statistics
    n = len(all_concs)
    predictions = slope * all_concs + intercept
    residuals = all_intensities - predictions
    ss_residuals = np.sum(residuals**2)
    sy = np.sqrt(ss_residuals / (n - 2))  # Standard error of estimate

    # Standard error of slope
    sx_squared = np.sum((all_concs - np.mean(all_concs))**2)
    sm = sy / np.sqrt(sx_squared)

    # Standard error of intercept
    sb = sy * np.sqrt(1/n + np.mean(all_concs)**2 / sx_squared)

    print("\n" + "="*80)
    print("CALIBRATION CURVE - Linear Regression Statistics")
    print("="*80)
    print(f"Equation: y = {slope:.4f}x + {intercept:.4f}")
    print(f"Slope (m): {slope:.4f} ± {sm:.4f}")
    print(f"Intercept (b): {intercept:.4f} ± {sb:.4f}")
    print(f"R² = {r_value**2:.6f}")
    print(f"Standard error of estimate (sy): {sy:.4f}")
    print(f"Number of data points: {n}")

    # Calculate LOD and LOQ
    LOD = 3.3 * sy / abs(slope)
    LOQ = 10 * sy / abs(slope)

    print("\n" + "="*80)
    print("LIMIT OF DETECTION (LOD) AND QUANTIFICATION (LOQ)")
    print("="*80)
    print(f"LOD = 3.3 × sy / m = 3.3 × {sy:.4f} / {abs(slope):.4f} = {LOD:.4f} ppm")
    print(f"LOQ = 10 × sy / m = 10 × {sy:.4f} / {abs(slope):.4f} = {LOQ:.4f} ppm")

    # Plot calibration curves
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Mean values with error bars
    axes[0].errorbar(concentrations_array, means_array, yerr=df_analysis['SD'].values,
                     fmt='o-', capsize=5, markersize=8, linewidth=2,
                     label='Mean ± SD')
    axes[0].set_xlabel('Concentration (ppm)', fontsize=12)
    axes[0].set_ylabel('Corrected Intensity (a.u.)', fontsize=12)
    axes[0].set_title('Calibration Curve - Mean Values with Error Bars', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Plot 2: All data points with regression line
    axes[1].scatter(all_concs, all_intensities, alpha=0.6, s=50, label='All data points')
    x_line = np.linspace(0, max(all_concs)*1.1, 100)
    y_line = slope * x_line + intercept
    axes[1].plot(x_line, y_line, 'r-', linewidth=2,
                 label=f'y = {slope:.2f}x + {intercept:.2f}\nR² = {r_value**2:.4f}')
    axes[1].set_xlabel('Concentration (ppm)', fontsize=12)
    axes[1].set_ylabel('Corrected Intensity (a.u.)', fontsize=12)
    axes[1].set_title('Calibration Curve - All Data Points', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    plt.tight_layout()
    plt.savefig('calibration_curves.png', dpi=300, bbox_inches='tight')
    print("\n✓ Saved calibration_curves.png")

    # Analyze tonic water samples
    print("\n" + "="*80)
    print("TONIC WATER SAMPLES ANALYSIS")
    print("="*80)

    tonic_samples = ['Tci.csv', 'Ti.csv', 'Tn.csv']
    tonic_results = []

    for sample_file in tonic_samples:
        try:
            label, wl, intensity = read_fluorescence_csv(sample_file)
            corrected_intensity = intensity - blank_intensity

            # Calculate concentration using calibration curve
            # y = mx + b => x = (y - b) / m
            concentration = (corrected_intensity - intercept) / slope

            # Calculate uncertainty in concentration using the formula from PDF page 19
            k = 1  # single measurement of unknown
            x_mean = np.mean(all_concs)
            sum_xi_minus_xmean_sq = np.sum((all_concs - x_mean)**2)

            sx = (sy / abs(slope)) * np.sqrt(
                (1/k) + (1/n) +
                ((corrected_intensity - np.mean(all_intensities))**2) /
                (slope**2 * sum_xi_minus_xmean_sq)
            )

            tonic_results.append({
                'Sample': label,
                'Intensity': corrected_intensity,
                'Concentration (ppm)': concentration,
                'Uncertainty (ppm)': sx
            })

            print(f"\n{sample_file}:")
            print(f"  Corrected Intensity: {corrected_intensity:.2f}")
            print(f"  Concentration: {concentration:.3f} ± {sx:.3f} ppm")
            print(f"  (or {concentration:.2f}₍{str(sx)[:2]}₎ ± {sx:.2f}₍{str(sx)[:1]}₎ ppm)")

        except FileNotFoundError:
            print(f"  {sample_file} not found")

    # Create summary report
    print("\n" + "="*80)
    print("SUMMARY REPORT")
    print("="*80)
    print(f"\n1. Calibration curve created using {n} data points (6 concentrations × 3 replicates)")
    print(f"2. Linear relationship: y = {slope:.2f}x + {intercept:.2f} (R² = {r_value**2:.4f})")
    print(f"3. Limit of Detection: {LOD:.4f} ppm")
    print(f"4. Limit of Quantification: {LOQ:.4f} ppm")
    print(f"5. EU safety limit for quinine in tonic water: 100 mg/L = 100 ppm")

    if tonic_results:
        print(f"\n6. Tonic Water Analysis Results:")
        for result in tonic_results:
            conc = result['Concentration (ppm)']
            unc = result['Uncertainty (ppm)']
            print(f"   {result['Sample']}: {conc:.2f} ± {unc:.2f} ppm")
            if conc < 100:
                print(f"      ✓ Within EU safety limits")
            else:
                print(f"      ✗ EXCEEDS EU safety limits!")

    # Save results to Excel
    with pd.ExcelWriter('quinine_analysis_results.xlsx', engine='openpyxl') as writer:
        df_analysis.to_excel(writer, sheet_name='Calibration Data', index=False)

        # Regression stats
        reg_stats = pd.DataFrame({
            'Parameter': ['Slope (m)', 'Intercept (b)', 'R²', 'Std Error (sy)',
                         'Slope StdErr (sm)', 'Intercept StdErr (sb)',
                         'LOD (ppm)', 'LOQ (ppm)'],
            'Value': [slope, intercept, r_value**2, sy, sm, sb, LOD, LOQ]
        })
        reg_stats.to_excel(writer, sheet_name='Regression Stats', index=False)

        # Tonic water results
        if tonic_results:
            df_tonic = pd.DataFrame(tonic_results)
            df_tonic.to_excel(writer, sheet_name='Tonic Water Results', index=False)

    print("\n✓ Saved quinine_analysis_results.xlsx")
    print("\n" + "="*80)

if __name__ == '__main__':
    main()
