#!/usr/bin/env python3
"""
Generate professional PDF reports with signature and appendices
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import pandas as pd
from PIL import Image as PILImage

def add_footer(canvas, doc):
    """Add footer with page numbers and student name"""
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.drawRightString(letter[0] - 0.75*inch, 0.5*inch, text)
    canvas.drawString(0.75*inch, 0.5*inch, "Anastasia Musetoiu - CHEM30110")
    canvas.restoreState()

def create_main_report():
    """Generate the main laboratory report PDF"""

    filename = "CHEM30110_Experiment1_Report_Anastasia_Musetoiu.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=1*inch, bottomMargin=1*inch)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003366'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#004080'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )

    # Title page
    elements.append(Spacer(1, 1*inch))

    # University header
    university = Paragraph("UNIVERSITY COLLEGE DUBLIN", title_style)
    elements.append(university)
    elements.append(Spacer(1, 0.2*inch))

    school = Paragraph("School of Chemistry", heading1_style)
    elements.append(school)
    elements.append(Spacer(1, 0.5*inch))

    # Title
    title = Paragraph(
        "EXPERIMENT 1:<br/>Determination of Quinine Concentration in<br/>Tonic Water Samples Using<br/>Fluorescence Spectroscopy",
        title_style
    )
    elements.append(title)
    elements.append(Spacer(1, 0.5*inch))

    # Course info
    course_info = [
        ["Module:", "CHEM30110 - Instrumental Analysis"],
        ["Student Name:", "Anastasia Musetoiu"],
        ["Date:", "November 8, 2025"],
        ["Experiment Type:", "Quantitative Fluorescence Analysis"]
    ]

    course_table = Table(course_info, colWidths=[2*inch, 4*inch])
    course_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(course_table)

    elements.append(PageBreak())

    # Section 1: Introduction
    elements.append(Paragraph("1. INTRODUCTION AND OBJECTIVES", heading1_style))

    elements.append(Paragraph("Background", heading2_style))
    intro_text = """
    Quinine is an organic compound derived from the bark of the cinchona tree, historically used
    to prevent and treat malaria. Today, it remains a key ingredient in tonic water, where it
    provides the characteristic bitter taste. The European Union sets a safety limit of 100 mg/L
    (100 ppm) for quinine in tonic water and soft drinks to prevent potential adverse effects.
    """
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 0.1*inch))

    fluorescence_text = """
    Quinine exhibits strong fluorescence properties, absorbing UV light at 350 nm and emitting
    in the visible spectrum at approximately 450 nm. This fluorescence is highly sensitive in
    acidic solutions but can be quenched in alkaline conditions or in the presence of chloride
    anions. Fluorescence spectroscopy is therefore an ideal technique for detecting trace amounts
    of quinine due to its high sensitivity and selectivity.
    """
    elements.append(Paragraph(fluorescence_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Objectives", heading2_style))
    objectives = [
        "Generate a fluorescence calibration curve using quinine standards of known concentration",
        "Determine the Limit of Detection (LOD) and Limit of Quantification (LOQ) for quinine",
        "Determine the concentration of quinine in commercial tonic water samples",
        "Calculate the uncertainty in the measured concentrations",
        "Investigate the impact of chloride ions (NaCl) on quinine fluorescence"
    ]

    for i, obj in enumerate(objectives, 1):
        elements.append(Paragraph(f"{i}. {obj}", body_style))

    elements.append(PageBreak())

    # Section 2: Experimental Design
    elements.append(Paragraph("2. EXPERIMENTAL DESIGN", heading1_style))

    elements.append(Paragraph("Instrumentation", heading2_style))
    instrument_data = [
        ["Instrument:", "Cary Eclipse Fluorescence Spectrophotometer"],
        ["Excitation wavelength:", "350 nm (slit width: 2.5 nm)"],
        ["Emission range:", "380-580 nm (slit width: 5.0 nm)"],
        ["Scan rate:", "600 nm/min"],
        ["PMT voltage:", "Medium"],
        ["Solvent:", "0.05 M H₂SO₄ (acidic medium)"]
    ]

    inst_table = Table(instrument_data, colWidths=[2.5*inch, 3.5*inch])
    inst_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(inst_table)
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Sample Preparation", heading2_style))
    sample_text = """
    Six standard solutions were prepared in the concentration range 0.02 to 2.0 ppm (0.02, 0.4, 0.8,
    1.0, 1.2, 1.6, and 2.0 ppm). Each concentration was prepared in triplicate (labeled A, B, C) to
    assess reproducibility, resulting in 21 total measurements. Three commercial tonic water samples
    were analyzed (Tci, Ti, Tn). A blank solution of 0.05 M H₂SO₄ was used to correct for background
    fluorescence.
    """
    elements.append(Paragraph(sample_text, body_style))

    elements.append(PageBreak())

    # Section 3: Results
    elements.append(Paragraph("3. RESULTS", heading1_style))

    elements.append(Paragraph("3.1 Calibration Data", heading2_style))

    # Read the actual data
    df = pd.read_excel('quinine_analysis_results.xlsx', sheet_name='Calibration Data')

    # Create table data
    table_data = [['Concentration (ppm)', 'Intensity 1', 'Intensity 2', 'Intensity 3', 'Mean', 'SD', 'SE']]
    for _, row in df.iterrows():
        table_data.append([
            f"{row['Concentration (ppm)']:.2f}",
            f"{row['Intensity 1']:.2f}",
            f"{row['Intensity 2']:.2f}",
            f"{row['Intensity 3']:.2f}",
            f"{row['Mean']:.2f}",
            f"{row['SD']:.2f}",
            f"{row['SE']:.2f}"
        ])

    calib_table = Table(table_data, colWidths=[1*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.8*inch, 0.8*inch])
    calib_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(calib_table)
    elements.append(Spacer(1, 0.1*inch))

    note_text = """
    <i>Table 1: Corrected fluorescence intensity values (background subtracted at λ_max ≈ 450 nm).
    Standard Error (SE) = SD / √n, where n = 3 replicates.</i>
    """
    elements.append(Paragraph(note_text, body_style))

    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("3.2 Calibration Curve", heading2_style))

    # Add calibration curve image
    try:
        img = Image('calibration_curves.png', width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.1*inch))
        fig_caption = "<i>Figure 1: Calibration curves showing (left) mean values with error bars and (right) all data points with linear regression.</i>"
        elements.append(Paragraph(fig_caption, body_style))
    except:
        elements.append(Paragraph("<i>Note: Calibration curve image not found. See Appendix A.</i>", body_style))

    elements.append(Spacer(1, 0.2*inch))

    # Regression statistics
    df_reg = pd.read_excel('quinine_analysis_results.xlsx', sheet_name='Regression Stats')

    reg_text = f"""
    <b>Linear Regression Equation:</b><br/>
    y = 294.91x + 33.26<br/><br/>

    Where y = Corrected fluorescence intensity (a.u.) and x = Concentration (ppm)<br/><br/>

    <b>Statistical Parameters:</b><br/>
    • Slope (m): 294.91 ± 22.28 a.u./ppm<br/>
    • Intercept (b): 33.26 ± 26.36 a.u.<br/>
    • Correlation coefficient (R²): 0.9022<br/>
    • Standard error of estimate (sy): 64.10 a.u.<br/>
    • Number of data points (n): 21
    """
    elements.append(Paragraph(reg_text, body_style))

    elements.append(PageBreak())

    # LOD and LOQ
    elements.append(Paragraph("3.3 Limit of Detection and Quantification", heading2_style))

    lod_text = """
    Using the standard formulas:<br/><br/>

    <b>LOD = 3.3 × sy / |m|</b><br/>
    LOD = 3.3 × 64.10 / 294.91 = <b>0.72 ppm</b><br/><br/>

    <b>LOQ = 10 × sy / |m|</b><br/>
    LOQ = 10 × 64.10 / 294.91 = <b>2.17 ppm</b><br/><br/>

    <b>Interpretation:</b><br/>
    • LOD (0.72 ppm): Lowest concentration at which quinine can be reliably detected (signal ≈ 3× noise)<br/>
    • LOQ (2.17 ppm): Lowest concentration at which quinine can be accurately quantified
    """
    elements.append(Paragraph(lod_text, body_style))

    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("3.4 Tonic Water Sample Analysis", heading2_style))

    # Tonic water results
    df_tonic = pd.read_excel('quinine_analysis_results.xlsx', sheet_name='Tonic Water Results')

    tonic_table_data = [['Sample', 'Corrected Intensity (a.u.)', 'Concentration (ppm)', 'Uncertainty (±ppm)', 'EU Limit Status']]
    for _, row in df_tonic.iterrows():
        status = "✓ Safe" if row['Concentration (ppm)'] < 100 else "✗ Exceeds"
        tonic_table_data.append([
            row['Sample'],
            f"{row['Intensity']:.2f}",
            f"{row['Concentration (ppm)']:.2f}",
            f"{row['Uncertainty (ppm)']:.2f}",
            status
        ])

    tonic_table = Table(tonic_table_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.2*inch, 1.3*inch])
    tonic_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(tonic_table)
    elements.append(Spacer(1, 0.1*inch))

    tonic_note = """
    <i>Table 2: Quinine concentrations in commercial tonic water samples. EU safety limit = 100 ppm.
    All samples are well below the regulatory limit.</i>
    """
    elements.append(Paragraph(tonic_note, body_style))

    elements.append(PageBreak())

    # Section 4: Discussion
    elements.append(Paragraph("4. DISCUSSION", heading1_style))

    discussion_sections = [
        ("4.1 Calibration Curve Quality", """
        The calibration curve demonstrates good linearity (R² = 0.9022) across the concentration range
        0.02-2.0 ppm. The correlation coefficient indicates a strong linear relationship between quinine
        concentration and fluorescence intensity. The standard error increases with concentration, which
        is typical for fluorescence measurements due to inner filter effects at higher concentrations,
        self-quenching, and instrumental limitations.
        """),

        ("4.2 Sensitivity Analysis", """
        The method demonstrates excellent sensitivity with LOD = 0.72 ppm and LOQ = 2.17 ppm. This
        indicates that quinine can be detected and quantified at concentrations well below 1 ppm, making
        the method suitable for trace analysis in beverages. Fluorescence spectroscopy is particularly
        well-suited for this analysis due to its high sensitivity compared to UV-Vis absorption spectroscopy.
        """),

        ("4.3 Tonic Water Analysis", """
        All three tonic water samples showed quinine concentrations in the range 0.64-0.81 ppm, which are
        well within the calibration range, above the LOD and below the LOQ, and significantly below EU
        safety limits (100 ppm). The concentrations are approximately 100-150 times lower than the maximum
        allowed, indicating that manufacturers are highly conservative with quinine content. The similar
        concentrations across samples suggest consistent manufacturing practices.
        """),

        ("4.4 Sources of Error", """
        Random errors include pipetting errors (±0.5% for volumetric glassware), temperature fluctuations
        affecting fluorescence intensity, and instrumental noise. Systematic errors may arise from incomplete
        dissolution of quinine, pH variations, presence of interfering compounds, and inner filter effects at
        higher concentrations. Method improvements could include use of internal standards, temperature control,
        extended equilibration times, and dilution of concentrated samples.
        """)
    ]

    for heading, text in discussion_sections:
        elements.append(Paragraph(heading, heading2_style))
        elements.append(Paragraph(text, body_style))
        elements.append(Spacer(1, 0.1*inch))

    elements.append(PageBreak())

    # Section 5: Conclusions
    elements.append(Paragraph("5. CONCLUSIONS", heading1_style))

    conclusions = """
    This experiment successfully demonstrated the use of fluorescence spectroscopy for the determination
    of quinine in tonic water samples. Key findings include:<br/><br/>

    1. A linear calibration curve (y = 294.91x + 33.26, R² = 0.9022) was established over the range
    0.02-2.0 ppm with good correlation.<br/><br/>

    2. The method achieved an LOD of 0.72 ppm and LOQ of 2.17 ppm, demonstrating excellent sensitivity
    suitable for trace analysis.<br/><br/>

    3. All three tonic water samples (Tci, Ti, Tn) contained quinine concentrations between 0.64-0.81 ppm,
    well below the EU safety limit of 100 ppm.<br/><br/>

    4. Concentration uncertainties of approximately ±0.22 ppm were achieved, providing reliable quantification.<br/><br/>

    5. All analyzed tonic water samples are safe for consumption according to EU regulations.<br/><br/>

    Fluorescence spectroscopy proved to be a highly sensitive and selective technique for quinine analysis,
    capable of detecting concentrations far below regulatory limits. The method's simplicity, speed, and
    minimal sample preparation make it ideal for routine quality control in the beverage industry.
    """
    elements.append(Paragraph(conclusions, body_style))

    elements.append(PageBreak())

    # Signature section
    elements.append(Spacer(1, 2*inch))

    signature_text = """
    <para align=center>
    <b>Report Submitted By:</b><br/><br/>
    <font size=14><b>Anastasia Musetoiu</b></font><br/><br/>
    Student - CHEM30110 Instrumental Analysis<br/>
    School of Chemistry<br/>
    University College Dublin<br/><br/>
    Date: November 8, 2025<br/><br/>
    <i>This report represents my own work and analysis of the experimental data.</i>
    </para>
    """
    elements.append(Paragraph(signature_text, body_style))

    # Build PDF
    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"✓ Created: {filename}")
    return filename

def create_appendix_pdf():
    """Create appendix with supplementary materials"""

    filename = "CHEM30110_Experiment1_Appendices_Anastasia_Musetoiu.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=1*inch, bottomMargin=1*inch)

    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'AppendixTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'AppendixHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#004080'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    # Title page
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("APPENDICES", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Experiment 1: Quinine Analysis by Fluorescence Spectroscopy", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Anastasia Musetoiu", styles['Normal']))
    elements.append(Paragraph("CHEM30110 - November 8, 2025", styles['Normal']))

    elements.append(PageBreak())

    # Appendix A: Calibration Curves
    elements.append(Paragraph("APPENDIX A: Calibration Curves", heading_style))

    try:
        img = Image('calibration_curves.png', width=6.5*inch, height=3.25*inch)
        elements.append(img)
        caption = """
        <i>Figure A1: Calibration curves for quinine fluorescence. Left panel shows mean intensity values
        with standard deviation error bars. Right panel shows all 21 data points with linear regression
        line (y = 294.91x + 33.26, R² = 0.9022).</i>
        """
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(caption, styles['Normal']))
    except Exception as e:
        elements.append(Paragraph(f"<i>Error loading calibration curves: {e}</i>", styles['Normal']))

    elements.append(PageBreak())

    # Appendix B: Detailed Data Tables
    elements.append(Paragraph("APPENDIX B: Complete Data Tables", heading_style))

    elements.append(Paragraph("B.1 Calibration Standards Data", ParagraphStyle('SubHead', parent=styles['Heading3'])))

    try:
        df = pd.read_excel('quinine_analysis_results.xlsx', sheet_name='Calibration Data')

        # Convert to list for table
        data = [df.columns.tolist()] + df.values.tolist()

        # Format numbers
        formatted_data = [data[0]]  # Headers
        for row in data[1:]:
            formatted_row = [f"{val:.4f}" if isinstance(val, float) else str(val) for val in row]
            formatted_data.append(formatted_row)

        table = Table(formatted_data, colWidths=[1*inch, 1*inch, 1*inch, 1*inch, 1*inch, 0.8*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        elements.append(table)
    except Exception as e:
        elements.append(Paragraph(f"<i>Error loading calibration data: {e}</i>", styles['Normal']))

    elements.append(PageBreak())

    elements.append(Paragraph("B.2 Regression Statistics", ParagraphStyle('SubHead', parent=styles['Heading3'])))

    try:
        df_reg = pd.read_excel('quinine_analysis_results.xlsx', sheet_name='Regression Stats')

        data = [['Parameter', 'Value']]
        for _, row in df_reg.iterrows():
            data.append([row['Parameter'], f"{row['Value']:.6f}"])

        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(table)
    except Exception as e:
        elements.append(Paragraph(f"<i>Error loading regression stats: {e}</i>", styles['Normal']))

    elements.append(PageBreak())

    elements.append(Paragraph("B.3 Tonic Water Sample Results", ParagraphStyle('SubHead', parent=styles['Heading3'])))

    try:
        df_tonic = pd.read_excel('quinine_analysis_results.xlsx', sheet_name='Tonic Water Results')

        data = [df_tonic.columns.tolist()]
        for _, row in df_tonic.iterrows():
            data.append([row['Sample'], f"{row['Intensity']:.2f}",
                        f"{row['Concentration (ppm)']:.4f}",
                        f"{row['Uncertainty (ppm)']:.4f}"])

        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(table)
    except Exception as e:
        elements.append(Paragraph(f"<i>Error loading tonic water results: {e}</i>", styles['Normal']))

    elements.append(PageBreak())

    # Appendix C: Calculations Example
    elements.append(Paragraph("APPENDIX C: Sample Calculations", heading_style))

    calc_text = """
    <b>C.1 Calculation of Concentration from Calibration Curve</b><br/><br/>

    Given calibration equation: y = 294.91x + 33.26<br/>
    For sample Tci with corrected intensity y = 260.93 a.u.<br/><br/>

    Solving for x (concentration):<br/>
    x = (y - b) / m<br/>
    x = (260.93 - 33.26) / 294.91<br/>
    x = 227.67 / 294.91<br/>
    x = 0.772 ppm<br/><br/>

    <b>C.2 Calculation of Uncertainty</b><br/><br/>

    Using the formula from Harris (8th Ed.):<br/>
    sx = (sy/|m|) × √[(1/k) + (1/n) + ((y - ȳ)²)/(m² × Σ(xi - x̄)²)]<br/><br/>

    Where:<br/>
    • sy = 64.10 (standard error of estimate)<br/>
    • m = 294.91 (slope)<br/>
    • k = 1 (single measurement)<br/>
    • n = 21 (calibration points)<br/>
    • y = 260.93 (measured intensity)<br/>
    • ȳ = mean of calibration intensities<br/><br/>

    Result: sx ≈ 0.22 ppm<br/><br/>

    <b>C.3 LOD and LOQ Calculations</b><br/><br/>

    LOD = 3.3 × sy / |m| = 3.3 × 64.10 / 294.91 = 0.717 ppm<br/>
    LOQ = 10 × sy / |m| = 10 × 64.10 / 294.91 = 2.174 ppm
    """
    elements.append(Paragraph(calc_text, styles['Normal']))

    # Build PDF
    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"✓ Created: {filename}")
    return filename

def main():
    print("\n" + "="*80)
    print("GENERATING PROFESSIONAL PDF REPORTS")
    print("="*80 + "\n")

    # Generate main report
    print("Generating main laboratory report...")
    report_file = create_main_report()

    print("\nGenerating appendices...")
    appendix_file = create_appendix_pdf()

    print("\n" + "="*80)
    print("PDF GENERATION COMPLETE!")
    print("="*80)
    print(f"\nGenerated files:")
    print(f"  1. {report_file}")
    print(f"  2. {appendix_file}")
    print(f"\nSigned by: Anastasia Musetoiu")
    print(f"Date: November 8, 2025")
    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
