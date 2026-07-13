import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- Advanced Visualizations (Translated and Enhanced) ---

def draw_deep_beam_concept(base_length=600, level_diff=80):
    """
    Draws a 3-layer deep beam diagram: Geometry, Strut-and-Tie, and Reinforcement.
    All labels are in English.
    """
    total_depth = 100 + level_diff
    # Calculate aspect ratio to set fig size
    fig_width = 10
    fig_height = 10 # More height for 3 layers
    
    fig, axes = plt.subplots(3, 1, figsize=(fig_width, fig_height), sharex=True)
    fig.suptitle("Deep Beam: Strut-and-Tie Model & Reinforcement Layout", fontsize=16, fontweight='bold')
    
    # Common colors and styles
    concrete_color = '#e0e0e0'
    compression_color = '#3498db' # Blue for compression
    tension_color = '#e74c3c' # Red for tension
    main_rebar_color = tension_color
    skin_rebar_color = '#27ae60' # Green
    stirrup_color = '#f39c12' # Orange
    
    # LAYER 1: Geometry and Loading
    ax = axes[0]
    ax.set_title("Layer 1: Beam Geometry & External Loading", loc='left')
    rect = patches.Rectangle((0, 0), base_length, total_depth, linewidth=1.5, edgecolor='black', facecolor=concrete_color)
    ax.add_patch(rect)
    # Supports
    ax.plot([-20, base_length+20], [-10, -10], color='black', linewidth=1.5)
    for x in [0, base_length]:
        ax.add_patch(patches.Rectangle((x-15, -15), 30, 15, facecolor='#c0c0c0'))
    # Load arrow
    ax.arrow(base_length/2, total_depth+30, 0, -20, head_width=20, head_length=15, fc='black', ec='black')
    ax.text(base_length/2+25, total_depth+20, "Total Load", fontsize=11)
    
    # LAYER 2: Strut-and-Tie Model (STM)
    ax = axes[1]
    ax.set_title("Layer 2: Load Transfer via Strut-and-Tie Model (Conceptual)", loc='left')
    # Simplified truss representation
    load_point = [base_length/2, total_depth]
    support_points = [[0, 0], [base_length, 0]]
    # Compression struts (blue)
    for p in support_points:
        ax.plot([load_point[0], p[0]], [load_point[1], p[1]], color=compression_color, linestyle='--', linewidth=4, alpha=0.6)
    ax.text(base_length/4, total_depth/2, "Concrete Struts (Compression)", color=compression_color, rotation=-35, weight='bold')
    # Tension tie (red)
    ax.plot([support_points[0][0], support_points[1][0]], [support_points[0][1], support_points[1][1]], color=tension_color, linewidth=5, alpha=0.8)
    ax.text(base_length/2, -15, "Steel Tie (Tension)", color=tension_color, weight='bold', ha='center')
    ax.add_patch(patches.Circle(load_point, 5, facecolor='black'))
    for p in support_points:
        ax.add_patch(patches.Circle(p, 5, facecolor='black'))

    # LAYER 3: Detailing and Reinforcement
    ax = axes[2]
    ax.set_title("Layer 3: Detailed Reinforcement Layout", loc='left')
    rect = patches.Rectangle((0, 0), base_length, total_depth, linewidth=1.5, edgecolor='black', facecolor=concrete_color)
    ax.add_patch(rect)
    # 1. Main Tension Rebar (bottom)
    y_pos = 15
    ax.plot([20, base_length-20], [y_pos, y_pos], color=main_rebar_color, linewidth=4)
    ax.text(base_length/2, y_pos-10, "Main Tension Tie Bar", color=main_rebar_color, ha='center', fontsize=9)
    # 2. Skin Reinforcement (scaled number based on level_diff)
    num_skin_bars = int(total_depth / 35)
    for i in range(1, num_skin_bars):
        y_pos = i * 35 + 15
        if y_pos < total_depth - 15:
            ax.plot([15, base_length-15], [y_pos, y_pos], color=skin_rebar_color, linewidth=1, linestyle='-.')
    ax.text(base_length/2, num_skin_bars*35+10, "Skin Reinforcement for Shrinkage/Temp. Control", color=skin_rebar_color, ha='center', fontsize=9)
    # 3. Stirrups/Shear reinforcement
    for x in range(30, base_length-20, 40):
        ax.plot([x, x], [10, total_depth-10], color=stirrup_color, linewidth=1.5)
    ax.text(base_length/2, total_depth+10, "Stirrups/Shear Reinforcement", color=stirrup_color, ha='center', fontsize=9)
    
    # Setup shared properties
    for ax in axes:
        ax.set_xlim(-50, base_length + 50)
        ax.set_ylim(-30, total_depth + 60)
        ax.set_aspect('equal')
        ax.axis('off')
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    return fig

def draw_z_beam_concept(base_length=600, level_diff=80):
    """
    Draws a Z-shaped beam detailing diagram with clear contextual labeling
    and an expanded critical section view. All labels are in English.
    """
    # Define geometry points
    x = [0, 300, 300, base_length, base_length, 260, 260, 0]
    # The bottom profile height d0 is fixed, the total top height scales
    d0 = 50 
    h_lower = 100
    h_upper = 100 + level_diff # Variable upper section height
    
    y_upper_top = h_upper + d0 + 100
    y_upper_bot = h_upper + d0
    y_lower_top = h_lower + d0
    y_lower_bot = d0

    # Calculate coordinates
    p = [
        [0, y_upper_top], [300, y_upper_top], [300, y_lower_top], [base_length, y_lower_top],
        [base_length, d0], [260, d0], [260, y_upper_bot], [0, y_upper_bot]
    ]
    
    fig_width = 12
    fig_height = 8 # More width for expanded section
    fig, axes = plt.subplots(1, 2, figsize=(fig_width, fig_height), width_ratios=[1.8, 1])
    fig.suptitle("Z-Shaped Beam Detailing: Controlling Re-entrant Corner Stress", fontsize=16, fontweight='bold')
    
    concrete_color = '#e0e0e0'
    main_rebar_color = '#27ae60'
    critical_rebar_color = '#e74c3c'
    critical_zone_color = 'red'

    # LEFT AXIS: Main Context & Load Flow
    ax = axes[0]
    ax.set_title("Main Beam Context & Reinforcement Flow", loc='left')
    poly = patches.Polygon(xy=p, closed=True, edgecolor='black', facecolor=concrete_color, linewidth=2)
    ax.add_patch(poly)
    
    # 1. Main Reinforcement (flow through context)
    # Upper part main bars
    ax.plot([20, 280], [y_upper_top-15, y_upper_top-15], color=main_rebar_color, linewidth=3)
    ax.plot([280, 280], [y_upper_top-15, y_lower_bot+15], color=main_rebar_color, linewidth=3, linestyle='-.') # Link down
    # Lower part main bars
    ax.plot([320, base_length-20], [y_lower_bot+15, y_lower_bot+15], color=main_rebar_color, linewidth=3)
    ax.plot([320, 320], [y_lower_bot+15, y_upper_top-15], color=main_rebar_color, linewidth=3, linestyle='-.') # Link up

    # Highlight CRITICAL detail
    ax.text(300, (y_upper_bot + y_lower_top)/2, "Re-entrant Corner:\nHigh Stress Concentration", color='red', ha='center', weight='bold')
    ax.add_patch(patches.Circle((300, y_upper_bot), 25, color=critical_zone_color, alpha=0.3))
    
    # Labels and annotations for context
    ax.plot([-50, 0], [y_upper_bot+50, y_upper_bot+50], color='black', linewidth=1)
    ax.plot([base_length, base_length+50], [y_lower_bot+50, y_lower_bot+50], color='black', linewidth=1)
    ax.text(-50, y_upper_bot+60, "Upper Floor/Roof Slab", fontsize=9, ha='center')
    ax.text(base_length+50, y_lower_bot+60, "Lower Floor Slab", fontsize=9, ha='center')

    # Dim lines for scaling section
    ax.plot([-30, -30], [y_upper_bot, y_upper_top], color='gray', linewidth=1, marker='|')
    ax.text(-40, (y_upper_bot + y_upper_top)/2, "Scales with \nLevel Diff", color='gray', fontsize=8, va='center', ha='right')

    # Setup axis properties
    ax.set_xlim(-100, base_length + 100)
    ax.set_ylim(-30, y_upper_top + 80)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # RIGHT AXIS: Expanded Critical Detail
    ax = axes[1]
    ax.set_title("Expanded View: Re-entrant Corner Detailing", loc='left')
    
    # Focus geometry
    crop_poly = patches.Polygon(xy=[p[1], p[2], p[6]], closed=True, edgecolor='black', facecolor=concrete_color, linewidth=2.5)
    ax.add_patch(crop_poly)
    ax.add_patch(patches.Circle((300, y_upper_bot), 30, color=critical_zone_color, alpha=0.3))
    
    # 2. Main Reinforcement (closeup)
    ax.plot([280, 280], [y_upper_top-5, y_lower_bot+5], color=main_rebar_color, linewidth=4)
    ax.plot([320, 320], [y_lower_bot+5, y_upper_top-5], color=main_rebar_color, linewidth=4)

    # 3. Critical Diagonal Bars
    # Placement needs to be robust for scaling. Link top corner p[2] to bottom corner p[6].
    num_diag_bars = 3
    spacing = 15
    for i in range(num_diag_bars):
        offset = (i - num_diag_bars//2) * spacing
        start_p = [260, y_upper_bot + offset + level_diff/2]
        end_p = [340, y_upper_bot + offset - level_diff/2]
        ax.plot([start_p[0], end_p[0]], [start_p[1], end_p[1]], color=critical_rebar_color, linewidth=3, linestyle='-.')

    ax.text(300, y_upper_bot+40, "Crucial Diagonal Bars to Control Cracking", color=critical_rebar_color, ha='center', fontsize=9)
    ax.text(300, y_upper_bot, "Stress\nConcentration\nZone", color=critical_zone_color, ha='center', fontsize=11, weight='bold')
    
    # Setup axis properties
    ax.set_xlim(250, 350)
    ax.set_ylim(y_upper_bot-100, y_upper_top+20)
    # Manually make aspect equal based on zoom
    # ax.set_aspect('equal') # May not work well for closeup
    ax.axis('off')
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    return fig

# --- Streamlit UI (Translated) ---
st.set_page_config(page_title="Advanced Beam Detailing Viewer", layout="wide")

st.title("🏗️ Beam Reinforcement & Stress Visualization")
st.markdown("This program simulates load transfer and reinforcement detailing for non-standard beams. For improved clarity, the visualizations are now multi-layered.")
st.markdown("---")

# Layout with two columns (Parameters & Visualization)
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("⚙️ Parameter Controls")
    beam_type = st.radio(
        "Select Structure Type:",
        ("Deep Beam (High Depth)", "Z-Shaped Beam (Stepped section)")
    )
    
    level_diff = st.slider(
        "Level Difference/Height Increase (cm):", 
        min_value=20, 
        max_value=200, 
        value=80, 
        step=10,
        help="Adjust to see dynamic changes in beam geometry and reinforcement layout."
    )
    
    st.markdown("---")
    st.subheader("💡 Key Engineering Concepts")
    if beam_type == "Deep Beam (High Depth)":
        st.info("**Deep Beam:** For beams with high depth-to-span ratios, the load transfer mechanism shifts from bending to **Strut-and-Tie**. Crucially, **Skin Reinforcement** (horizontal web bars) must be provided to control crack width caused by temperature and shrinkage.")
    else:
        st.warning("**Z-Shaped Beam:** The critical point is the **Re-entrant Corner**, which experiences extremely high tensile stress concentrations. Special **Diagonal Bars** are essential to prevent a diagonal failure plane from developing. Main top/bottom rebar must also be adequately anchored.")

with col2:
    st.subheader("📊 Structural Visualization")
    if beam_type == "Deep Beam (High Depth)":
        fig = draw_deep_beam_concept(base_length=600, level_diff=level_diff)
    else:
        fig = draw_z_beam_concept(base_length=600, level_diff=level_diff)
        
    st.pyplot(fig)
