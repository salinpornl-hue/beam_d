import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_cad_deep_beam(base_length=6000, depth=1200):
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # 1. Concrete Outline
    rect = patches.Rectangle((0, 0), base_length, depth, linewidth=2, edgecolor='#111111', facecolor='#f8f9fa')
    ax.add_patch(rect)
    
    cc = 40 # Clear cover
    
    # 2. Stirrups (Grey)
    spacing = 250
    stirrup_x = range(cc + 50, base_length - cc, spacing)
    for x in stirrup_x:
        stirrup = patches.Rectangle((x, cc), 20, depth - 2*cc, linewidth=1.5, edgecolor='#7f8c8d', facecolor='none')
        ax.add_patch(stirrup)
        
    # 3. Main Bottom Rebar (Light Blue)
    rebar_y = cc + 15
    hook_len = 150
    ax.plot([cc, base_length - cc], [rebar_y, rebar_y], color='#3498db', linewidth=4)
    # Hooks
    ax.plot([cc, cc, cc+50], [rebar_y, rebar_y + hook_len, rebar_y + hook_len], color='#3498db', linewidth=4)
    ax.plot([base_length - cc, base_length - cc, base_length - cc - 50], [rebar_y, rebar_y + hook_len, rebar_y + hook_len], color='#3498db', linewidth=4)
    
    # 4. Main Top Rebar (Light Blue)
    top_y = depth - cc - 15
    ax.plot([cc, base_length - cc], [top_y, top_y], color='#3498db', linewidth=3)
    ax.plot([cc, cc, cc+50], [top_y, top_y - hook_len, top_y - hook_len], color='#3498db', linewidth=3)
    ax.plot([base_length - cc, base_length - cc, base_length - cc - 50], [top_y, top_y - hook_len, top_y - hook_len], color='#3498db', linewidth=3)
    
    # 5. Skin Reinforcement
    num_skin_bars = int(depth / 300)
    for i in range(1, num_skin_bars):
        y_pos = i * 300
        ax.plot([cc, base_length - cc], [y_pos, y_pos], color='#2980b9', linewidth=2, linestyle='-')

    ax.set_title("Deep Beam Reinforcement Detailing", fontsize=14, pad=15)
    ax.set_xlim(-200, base_length + 200)
    ax.set_ylim(-100, depth + 100)
    ax.set_aspect('equal')
    ax.axis('off')
    
    return fig

def draw_cad_z_beam():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Geometry
    d0 = 600
    level_diff = 800
    w1, w2 = 1800, 1800 # Width of left and right segments
    step_w = 400 # Width of the overlapping step
    
    # Concrete Coordinates
    x = [0, w1+step_w, w1+step_w, w1+w2+step_w, w1+w2+step_w, w1, w1, 0]
    y = [d0+level_diff, d0+level_diff, d0, d0, 0, 0, level_diff, level_diff]
    poly = patches.Polygon(xy=list(zip(x, y)), closed=True, edgecolor='black', facecolor='#f8f9fa', linewidth=2.5)
    ax.add_patch(poly)
    
    cc = 40 # Clear cover
    re_entrant_x, re_entrant_y = w1, level_diff
    
    # --- 1. Stirrups (Grey) ---
    stirrup_color = '#95a5a6'
    stirrup_lw = 2
    # Left beam stirrups
    for sx in range(cc+50, w1-50, 150):
        ax.add_patch(patches.Rectangle((sx, level_diff+cc), 30, d0-2*cc, lw=stirrup_lw, ec=stirrup_color, fc='none'))
    # Middle overlapping stirrups (Step area)
    for sx in range(w1+20, w1+step_w-20, 120):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d0+level_diff-2*cc, lw=stirrup_lw, ec=stirrup_color, fc='none'))
    # Right beam stirrups
    for sx in range(w1+step_w+50, w1+w2+step_w-50, 150):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d0-2*cc, lw=stirrup_lw, ec=stirrup_color, fc='none'))

    # --- 2. Main Reinforcement (Light Blue) ---
    main_color = '#3498db'
    main_lw = 4
    hook = 150
    
    # Top Compression Steel (Left -> Mid)
    t1_y = level_diff + d0 - cc - 10
    ax.plot([cc, w1+step_w-cc], [t1_y, t1_y], color=main_color, lw=main_lw)
    ax.plot([cc, cc, cc+100], [t1_y, t1_y-hook, t1_y-hook], color=main_color, lw=main_lw) # Left hook
    ax.plot([w1+step_w-cc, w1+step_w-cc], [t1_y, level_diff-100], color=main_color, lw=main_lw) # Anchor down
    
    # Top Compression Steel (Right)
    t2_y = d0 - cc - 10
    ax.plot([w1+cc, w1+w2+step_w-cc], [t2_y, t2_y], color=main_color, lw=main_lw)
    ax.plot([w1+w2+step_w-cc, w1+w2+step_w-cc, w1+w2+step_w-cc-100], [t2_y, t2_y-hook, t2_y-hook], color=main_color, lw=main_lw) # Right hook
    
    # Bottom Tension Steel (Left)
    b1_y = level_diff + cc + 10
    ax.plot([cc, w1+step_w-cc], [b1_y, b1_y], color=main_color, lw=main_lw)
    ax.plot([cc, cc, cc+100], [b1_y, b1_y+hook, b1_y+hook], color=main_color, lw=main_lw) # Left hook
    
    # Bottom Tension Steel (Right -> Mid)
    b2_y = cc + 10
    ax.plot([w1+step_w+100, w1+w2+step_w-cc], [b2_y, b2_y], color=main_color, lw=main_lw)
    ax.plot([w1+w2+step_w-cc, w1+w2+step_w-cc, w1+w2+step_w-cc-100], [b2_y, b2_y+hook, b2_y+hook], color=main_color, lw=main_lw) # Right hook
    ax.plot([w1+step_w+100, w1+cc], [b2_y, b2_y], color=main_color, lw=main_lw) # Anchor left
    ax.plot([w1+cc, w1+cc], [b2_y, d0+100], color=main_color, lw=main_lw) # Anchor up

    # --- 3. Corner L-Bar (Dark Blue) ---
    lbar_color = '#2980b9'
    lbar_y_left = level_diff + cc + 40
    lbar_y_right = d0 - cc - 40
    ax.plot([w1-800, w1+cc+30], [lbar_y_left, lbar_y_left], color=lbar_color, lw=3.5) # Horizontal top
    ax.plot([w1+cc+30, w1+cc+30], [lbar_y_left, lbar_y_right], color=lbar_color, lw=3.5) # Vertical drop
    ax.plot([w1+cc+30, w1+step_w+800], [lbar_y_right, lbar_y_right], color=lbar_color, lw=3.5) # Horizontal bottom
    
    # --- 4. Diagonal Crack Control Bars (Red) ---
    diag_color = '#c0392b'
    diag_length = 1800
    angle = np.deg2rad(45)
    
    for offset in [-60, 0, 60]:
        # Center of diagonal bar adjusted by offset
        dx = offset * np.cos(np.deg2rad(-45))
        dy = offset * np.sin(np.deg2rad(-45))
        
        start_x = re_entrant_x + dx - (diag_length/2)*np.cos(angle)
        start_y = re_entrant_y + dy - (diag_length/2)*np.sin(angle)
        end_x = re_entrant_x + dx + (diag_length/2)*np.cos(angle)
        end_y = re_entrant_y + dy + (diag_length/2)*np.sin(angle)
        
        ax.plot([start_x, end_x], [start_y, end_y], color=diag_color, lw=3.5)
        
        # 180-degree hooks for diagonal bars (Simplified drawing)
        hook_sz = 60
        ax.plot([end_x, end_x + hook_sz*np.cos(angle-np.pi/2), end_x + hook_sz*np.cos(angle-np.pi/2) - hook_sz*np.cos(angle)], 
                [end_y, end_y + hook_sz*np.sin(angle-np.pi/2), end_y + hook_sz*np.sin(angle-np.pi/2) - hook_sz*np.sin(angle)], 
                color=diag_color, lw=3.5)
        
        ax.plot([start_x, start_x - hook_sz*np.cos(angle-np.pi/2), start_x - hook_sz*np.cos(angle-np.pi/2) + hook_sz*np.cos(angle)], 
                [start_y, start_y - hook_sz*np.sin(angle-np.pi/2), start_y - hook_sz*np.sin(angle-np.pi/2) + hook_sz*np.sin(angle)], 
                color=diag_color, lw=3.5)

    # --- 5. Annotations and Callouts ---
    bbox_props = dict(boxstyle="square,pad=0.3", fc="white", ec="black", lw=1)
    arrow_props = dict(arrowstyle="->", color="black", lw=1.5)
    
    ax.annotate("Compression Steel", xy=(w1-400, t1_y), xytext=(w1-800, t1_y+150),
                arrowprops=arrow_props, fontsize=11, ha='center')
                
    ax.annotate("Main Tension", xy=(w1-600, b1_y), xytext=(w1-800, b1_y-150),
                arrowprops=arrow_props, fontsize=11, ha='center')
                
    ax.annotate("Corner L-Bar", xy=(w1+cc+30, (lbar_y_left+lbar_y_right)/2), xytext=(w1+800, (lbar_y_left+lbar_y_right)/2 + 100),
                arrowprops=arrow_props, fontsize=11, ha='center')
                
    ax.annotate("Stirrups", xy=(w1+w2+step_w-400, d0-cc), xytext=(w1+w2+step_w-200, d0+100),
                arrowprops=arrow_props, fontsize=11, ha='center')
                
    ax.annotate("Diagonal Crack Control Steel\nwith proper $L_d$ anchorage.", 
                xy=(re_entrant_x + 300, re_entrant_y + 300), xytext=(re_entrant_x + 1000, re_entrant_y + 400),
                arrowprops=arrow_props, bbox=bbox_props, fontsize=11, ha='center')
                
    ax.annotate("Diagonal Steel with\nstir re-entrant bars.", 
                xy=(re_entrant_x - 300, re_entrant_y - 300), xytext=(re_entrant_x - 700, re_entrant_y - 450),
                arrowprops=arrow_props, fontsize=11, ha='center')
                
    # L_d Anchorage Dimension Line
    dim_y = -150
    ax.plot([w1+cc+30, w1+step_w+800], [dim_y, dim_y], color='black', lw=1)
    ax.plot([w1+cc+30, w1+cc+30], [dim_y-30, lbar_y_right-20], color='black', lw=1, linestyle=':')
    ax.plot([w1+step_w+800, w1+step_w+800], [dim_y-30, lbar_y_right-20], color='black', lw=1, linestyle=':')
    ax.annotate("", xy=(w1+cc+30, dim_y), xytext=(w1+step_w+800, dim_y), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text((w1+cc+30 + w1+step_w+800)/2, dim_y-80, "$L_d$ Anchorage", ha='center', fontsize=12)

    ax.set_title("Stepped Beam / Re-entrant Corner Detailing", fontsize=16, pad=20, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Extend plot limits to fit callouts
    ax.set_xlim(-200, w1+w2+step_w+200)
    ax.set_ylim(-400, d0+level_diff+400)
    
    return fig

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="Structural Beam Detailing")
st.title("🏗️ CAD-Style Beam Reinforcement Detailing")
st.markdown("ภาพจำลองแบบก่อสร้าง (Shop Drawing) แสดงการจัดเหล็กเสริมตามมาตรฐานวิศวกรรม")

st.markdown("### คานเพิ่มความลึก (Deep Beam)")
st.pyplot(draw_cad_deep_beam())

st.markdown("---")

st.markdown("### คานหักมุม (Stepped Beam / Z-Beam)")
st.pyplot(draw_cad_z_beam())
