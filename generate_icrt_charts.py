"""
ICRT Chart Generation Script
Generates all figures for the Iterative Cross-Model Red Teaming paper
Figures: 1 (Model Break Rates), 2 (Domain Break Rates), 3 (Heatmap),
         4 (Iteration Analysis), 5 (Semantic Laundering Taxonomy)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set style for professional appearance
plt.style.use('default')
sns.set_palette("husl")

# Create output directory if it doesn't exist
output_dir = "icrt_charts"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Generating ICRT Charts...")
print(f"Output directory: {output_dir}/\n")

# ============================================================================
# FIGURE 1: Model Break Rates (Bar Chart)
# ============================================================================
def generate_figure1():
    """Generate Figure 1: Overall Break Rate by Model (as Target)"""
    models = ['Claude', 'ChatGPT', 'Gemini']
    rates = [3.3, 10.0, 82.5]
    colors = ['#1A7A1A', '#E67E00', '#C0392B']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(models, rates, color=colors, width=0.6, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 2, 
                f'{rate}%', ha='center', va='bottom', fontweight='bold', fontsize=13)
    
    ax.set_ylabel('Break Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 1: Overall Break Rate by Model (as Target)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.3, linewidth=1.5, label='50% threshold')
    ax.legend(fontsize=10)
    
    # Remove spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    
    # Add grid for readability
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig1_model_break_rates.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 1 saved: fig1_model_break_rates.png")
    plt.close()

# ============================================================================
# FIGURE 2: Domain Break Rates (Bar Chart)
# ============================================================================
def generate_figure2():
    """Generate Figure 2: Break Rate by Risk Domain"""
    domains = ['Bio/Chem', 'Cybersecurity', 'Manipulation']
    rates = [0.0, 35.1, 58.3]
    colors = ['#1A7A1A', '#E67E00', '#C0392B']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(domains, rates, color=colors, width=0.6, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        if rate == 0:
            label = '0%\n(No Breaks)'
            ax.text(bar.get_x() + bar.get_width()/2, height + 1.5, label, 
                   ha='center', va='bottom', fontweight='bold', fontsize=11)
        else:
            ax.text(bar.get_x() + bar.get_width()/2, height + 1.5, f'{rate}%', 
                   ha='center', va='bottom', fontweight='bold', fontsize=13)
    
    ax.set_ylabel('Break Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 2: Break Rate by Risk Domain', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 75)
    
    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    
    # Add grid
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig2_domain_break_rates.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 2 saved: fig2_domain_break_rates.png")
    plt.close()

# ============================================================================
# FIGURE 3: Attacker vs Target Heatmap (6-Cell Matrix with NA for Self-Attacks)
# ============================================================================
def generate_figure3():
    """Generate Figure 3: Breaks by Attacker-Target Pair (No Self-Attacks)"""
    # Create data based on the 6-cell attack matrix from the paper
    # Rows = Attacker Models, Columns = Target Models
    # No model attacks itself - those cells show NA
    # Data from section 3.4 and results:
    # Gemini attacks: Claude (Cybersecurity) = 2, ChatGPT (Bio/Chem) = 0
    # Claude attacks: Gemini (Cybersecurity) = 18, ChatGPT (Manipulation) = 6
    # ChatGPT attacks: Gemini (Manipulation) = 29, Claude (Bio/Chem) = 0
    
    # Create custom data with NaN for self-attacks
    data = pd.DataFrame({
        'Claude': [2, np.nan, 0],        # Gemini -> Claude, Claude -> Claude (NA), ChatGPT -> Claude
        'ChatGPT': [0, 6, np.nan],       # Gemini -> ChatGPT, Claude -> ChatGPT, ChatGPT -> ChatGPT (NA)
        'Gemini': [np.nan, 18, 29]       # Gemini -> Gemini (NA), Claude -> Gemini, ChatGPT -> Gemini
    }, index=['Gemini\n(Attacker)', 'Claude\n(Attacker)', 'ChatGPT\n(Attacker)'])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create custom colormap that handles NaN
    import matplotlib.colors as mcolors
    
    # Create heatmap with custom annotations
    sns.heatmap(data, annot=False, cmap='YlOrRd', linewidths=2.5, 
                linecolor='white', ax=ax, cbar_kws={'label': 'Number of Breaks'},
                vmin=0, vmax=30, square=True)
    
    # Add custom annotations (numbers and NA)
    for i in range(len(data.index)):
        for j in range(len(data.columns)):
            value = data.iloc[i, j]
            if pd.isna(value):
                text = ax.text(j + 0.5, i + 0.65, 'NA', ha='center', va='center',
                              fontsize=14, fontweight='bold', color='#333333')
            else:
                text = ax.text(j + 0.5, i + 0.65, f'{int(value)}', ha='center', va='center',
                              fontsize=16, fontweight='bold', color='black')
    
    ax.set_title('Figure 3: Breaks by Attacker-Target Pair', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Target Model', fontsize=12, fontweight='bold')
    ax.set_ylabel('Attacker Model', fontsize=12, fontweight='bold')
    
    # Rotate labels for better readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=11)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig3_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 3 saved: fig3_heatmap.png")
    plt.close()

# ============================================================================
# FIGURE 4: Break Rate by Iteration
# ============================================================================
def generate_figure4():
    """Generate Figure 4: Break Rate by Iteration Number"""
    iterations = ['Iteration 1\n(Initial)', 'Iteration 2\n(Refined)', 'Iteration 3\n(Escalated)']
    rates = [30.0, 28.8, 34.5]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(iterations, rates, color='#1A56DB', alpha=0.85, width=0.6, 
                  edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.8, f'{rate}%', 
               ha='center', va='bottom', fontweight='bold', fontsize=13)
    
    ax.set_ylabel('Break Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 4: Break Rate by Iteration Number', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 45)
    
    # Add reference line at mean
    mean_rate = np.mean(rates)
    ax.axhline(y=mean_rate, color='red', linestyle='--', alpha=0.5, linewidth=2, 
               label=f'Mean: {mean_rate:.1f}%')
    ax.legend(fontsize=10)
    
    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    
    # Add grid
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig4_iterations.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 4 saved: fig4_iterations.png")
    plt.close()

# ============================================================================
# FIGURE 5: Semantic Laundering Taxonomy (Block Diagram with Color Coding)
# ============================================================================
def generate_figure5():
    """Generate Figure 5: Semantic Laundering Attack Taxonomy with Break Status"""
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    ax.text(8, 10.5, 'Figure 5: Semantic Laundering Attack Types', 
           fontsize=18, fontweight='bold', ha='center')
    
    # Define taxonomy with break status
    # RED = Resulted in Break(s), GREEN = Detected/Blocked
    taxonomy = {
        'Professional Framing': [
            ('CTF Competition', 'red'),           # Claude P7 - BROKE
            ('Pen-test Documentation', 'green'),   # Various - blocked
            ('B2B Engineering Docs', 'green')      # Various - blocked
        ],
        'Educational Framing': [
            ('Training Module', 'red'),            # ChatGPT P8 - BROKE
            ('Research/Inoculation', 'green'),     # Various - blocked
            ('Documentary Advisor', 'green')       # Various - blocked
        ],
        'Creative Framing': [
            ('Fiction Writing', 'red'),            # Gemini P2 - BROKE
            ('Roleplay Character', 'red'),         # Gemini P1 - BROKE
            ('Mentor/Life Coach', 'red')           # Gemini P1, ChatGPT P5 - BROKE
        ],
        'Technical Framing': [
            ('Localhost Targeting', 'red'),        # Claude P10 - BROKE
            ('Developer Terminology', 'green'),    # Various - blocked
            ('Dual-Use Reframing', 'green')        # Various - blocked
        ]
    }
    
    # Color mapping
    color_map = {
        'red': '#FADBD8',      # Light red background
        'green': '#D5F4E6'     # Light green background
    }
    
    border_map = {
        'red': '#C0392B',      # Dark red border
        'green': '#27AE60'     # Dark green border
    }
    
    # Y positions for categories
    y_positions = [8.5, 6.5, 4.5, 2.5]
    
    for idx, (category, examples) in enumerate(taxonomy.items()):
        y = y_positions[idx]
        
        # Draw category box
        category_box = FancyBboxPatch((0.2, y-0.35), 2.2, 0.7, 
                                      boxstyle="round,pad=0.08", 
                                      edgecolor='black', facecolor='#E8E8E8',
                                      linewidth=2.5)
        ax.add_patch(category_box)
        ax.text(1.3, y, category, fontsize=12, fontweight='bold', 
               ha='center', va='center')
        
        # Draw arrow
        ax.arrow(2.5, y, 0.5, 0, head_width=0.2, head_length=0.15, 
                fc='black', ec='black', linewidth=2)
        
        # Draw example boxes
        box_width = 2.0
        start_x = 3.3
        spacing = 4.2
        
        for i, (example, status) in enumerate(examples):
            x = start_x + (i * spacing)
            
            # Example box with status-based colors
            example_box = FancyBboxPatch((x-box_width/2, y-0.35), box_width, 0.7,
                                        boxstyle="round,pad=0.08",
                                        edgecolor=border_map[status], 
                                        facecolor=color_map[status],
                                        linewidth=2.5)
            ax.add_patch(example_box)
            ax.text(x, y, example, fontsize=10, ha='center', va='center', 
                   fontweight='bold')
    
    # Add legend at bottom
    legend_y = 0.9
    ax.text(0.3, legend_y + 0.3, 'Status Legend:', fontsize=12, fontweight='bold')
    
    # Red box - Resulted in Break
    legend_box1 = FancyBboxPatch((2.2, legend_y-0.25), 0.5, 0.5,
                                 boxstyle="round,pad=0.05",
                                 edgecolor='#C0392B', facecolor='#FADBD8',
                                 linewidth=2.5)
    ax.add_patch(legend_box1)
    ax.text(3.2, legend_y, 'Resulted in Break(s)', fontsize=11, va='center', fontweight='bold')
    
    # Green box - Detected/Blocked
    legend_box2 = FancyBboxPatch((7.0, legend_y-0.25), 0.5, 0.5,
                                 boxstyle="round,pad=0.05",
                                 edgecolor='#27AE60', facecolor='#D5F4E6',
                                 linewidth=2.5)
    ax.add_patch(legend_box2)
    ax.text(8.0, legend_y, 'Detected/Blocked', fontsize=11, va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/fig5_semantic_laundering_taxonomy.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 5 saved: fig5_semantic_laundering_taxonomy.png")
    plt.close()

# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """Generate all figures"""
    try:
        generate_figure1()
        generate_figure2()
        generate_figure3()
        generate_figure4()
        generate_figure5()
        
        print(f"\n" + "="*60)
        print(f"✓ All charts generated successfully!")
        print(f"Output location: {os.path.abspath(output_dir)}/")
        print("="*60)
        print("\nGenerated files:")
        print("  1. fig1_model_break_rates.png")
        print("  2. fig2_domain_break_rates.png")
        print("  3. fig3_heatmap.png (3x3 matrix with NA for self-attacks)")
        print("  4. fig4_iterations.png")
        print("  5. fig5_semantic_laundering_taxonomy.png (with red/green color coding)")
        
    except Exception as e:
        print(f"Error generating charts: {e}")
        raise

if __name__ == "__main__":
    main()