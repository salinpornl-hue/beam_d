import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_cad_transition_deep_beam():
    """
    วาดคานที่เปลี่ยนระดับจากคานปกติ เป็น Deep Beam (Stepped-Bottom)
    """
    fig, ax = plt.subplots(figsize=(14, 5))
    
    base_length = 6000
    L1 = 2200  # ความยาวช่วงคานปกติ (ซ้าย)
    d1 = 600   # ความลึกคานปกติ
    d2 = 1200  # ความลึก Deep Beam
    
    # 1. พิกัดคอนกรีต (สมมติให้หลังคานด้านบนเรียบเสมอกัน และดรอปท้องคานลง)
    x_conc = [0, base_length, base_length, L1, L1, 0]
    y_conc = [d2, d2, 0, 0, d2-d1, d2-d1]
    poly = patches.Polygon(xy=list(zip(x_conc, y_conc)), closed=True, edgecolor='#111111', facecolor='#f8f9fa', lw=2)
    ax.add_patch(poly)
    
    cc = 40
    stirrup_color = '#95a5a6'
    main_color = '#3498db'
    diag_color = '#c0392b'
    
    # 2. เหล็กปลอก (Stirrups)
    # ช่วงคานปกติ (ซ้าย)
    for sx in range(cc+50, L1-50, 150):
        ax.add_patch(patches.Rectangle((sx, d2-d1+cc), 30, d1-2*cc, lw=2, ec=stirrup_color, fc='none'))
    # ช่วง Deep Beam (ขวา)
    for sx in range(L1+50, base_length-cc-50, 200):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d2-2*cc, lw=2, ec=stirrup_color, fc='none'))
        
    # 3. เหล็กเสริมหลักด้านบน (Main Top Rebar - วิ่งยาวตลอดแนว)
    hook = 150
    ty = d2 - cc - 15
    ax.plot([cc, base_length-cc], [ty, ty], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [ty, ty-hook, ty-hook], color=main_color, lw=4) # งอขอซ้าย
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [ty, ty-hook, ty-hook], color=main_color, lw=4) # งอขอขวา
    
    # 4. เหล็กเสริมหลักด้านล่าง ช่วงคานปกติ (ล้วงทะลุเข้าไปใน Deep Beam)
    by1 = d2 - d1 + cc + 15
    Ld = 1200 # ระยะล้วง (Development Length)
    ax.plot([cc, L1 + Ld], [by1, by1], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [by1, by1+hook, by1+hook], color=main_color, lw=4)
    # งอฉากที่ปลายระยะล้วงเพื่อยึดเหนี่ยว
    ax.plot([L1 + Ld, L1 + Ld, L1 + Ld - 50], [by1, by1-hook, by1-hook], color=main_color, lw=4)
    
    # 5. เหล็กเสริมหลักด้านล่าง ช่วง Deep Beam
    by2 = cc + 15
    ax.plot([L1+cc, base_length-cc], [by2, by2], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [by2, by2+hook, by2+hook], color=main_color, lw=4)
    # ฝั่งซ้ายงอขึ้นเพื่อหยุดในคอนกรีต
    ax.plot([L1+cc, L1+cc], [by2, by1-50], color=main_color, lw=4)
    ax.plot([L1+cc, L1+cc+50], [by1-50, by1-50], color=main_color, lw=4)
    
    # 6. เหล็กเสริมด้านข้าง (Skin Reinforcement)
    ax.plot([cc, base_length-cc], [900, 900], color='#2980b9', lw=2.5) # วิ่งยาวตลอดคาน
    ax.plot([L1+cc, base_length-cc], [300, 300], color='#2980b9', lw=2.5) # เฉพาะช่วง Deep Beam
    
    # 7. เหล็กเสริมทแยงมุมกันร้าว (Diagonal Crack Control ที่มุม Re-entrant)
    rx, ry = L1, d2-d1
    diag_len = 1400
    angle = np.deg2rad(45)
    for offset in [-50, 0, 50]:
        dx = offset * np.cos(np.deg2rad(-45))
        dy = offset * np.sin(np.deg2rad(-45))
        
        sx = rx + dx - (diag_len/2)*np.cos(angle)
        sy = ry + dy - (diag_len/2)*np.sin(angle)
        ex = rx + dx + (diag_len/2)*np.cos(angle)
        ey = ry + dy + (diag_len/2)*np.sin(angle)
        
        ax.plot([sx, ex], [sy, ey], color=diag_color, lw=3)
        # ขอเกี่ยวปลายเหล็กทแยง
        hook_sz = 60
        ax.plot([ex, ex + hook_sz*np.cos(angle-np.pi/2)], [ey, ey + hook_sz*np.sin(angle-np.pi/2)], color=diag_color, lw=3)
        ax.plot([sx, sx - hook_sz*np.cos(angle-np.pi/2)], [sy, sy - hook_sz*np.sin(angle-np.pi/2)], color=diag_color, lw=3)
        
    # 8. คำอธิบายและลูกศร
    arrow_props = dict(arrowstyle="->", color="black", lw=1.5)
    
    ax.text(L1/2, d2 - d1/2, "Normal Beam\nDepth = 600 mm", ha='center', va='center', fontsize=12, alpha=0.5)
    ax.text(L1 + (base_length-L1)/2, d2/2, "Deep Beam Segment\nDepth = 1200 mm", ha='center', va='center', fontsize=12, alpha=0.5)
    
    ax.annotate("Main bottom tension bar\nanchored into deep segment ($L_d$)", 
                xy=(L1 + Ld/2, by1), xytext=(L1 + Ld/2, by1 + 250),
                arrowprops=arrow_props, fontsize=11, ha='center')
                
    ax.annotate("Diagonal Crack Control Bars\nat Soffit Step", 
                xy=(rx + 200, ry + 200), xytext=(rx + 800, ry + 400),
                arrowprops=arrow_props, bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="black", lw=1), fontsize=11, ha='left')

    ax.set_title("Stepped-Bottom Beam: Transitioning to Deep Beam", fontsize=16, pad=20, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    
    ax.set_xlim(-200, base_length+200)
    ax.set_ylim(-100, d2+300)
    
    return fig

def draw_cad_z_beam():
    """
    วาด Z-Beam เน้นจุดวิกฤต Re-entrant Corner
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Geometry
    d0 = 600
    level_diff = 800
    w1, w2 = 1800, 1800
    step_w = 400
    
    # Concrete Coordinates
    x = [0, w1+step_w, w1+step_w, w1+w2+step_w, w1+w2+step_w, w1, w1, 0]
    y = [d0+level_diff, d0+level_diff, d0, d0, 0, 0, level_diff, level_diff]
    poly = patches.Polygon(xy=list(zip(x, y)), closed=True, edgecolor='black', facecolor='#f8f9fa', linewidth=2.5)
    ax.add_patch(poly)
    
    cc = 40
    re_entrant_x, re_entrant_y = w1, level_diff
    
    # 1. Stirrups (Grey)
    stirrup_color = '#95a5a6'
    stirrup_lw = 2
    for sx in range(cc+50, w1-50, 150):
        ax.add_patch(patches.Rectangle((sx, level_diff+cc), 30, d0-2*cc, lw=stirrup_lw, ec=stirrup_color, fc='none'))
    for sx in range(w1+20, w1+step_w-20, 120):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d0+level_diff-2*cc, lw=stirrup_lw, ec=stirrup_color, fc='none'))
    for sx in range(w1+step_w+50, w1+w2+step_w-50, 150):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d0-2*cc, lw=stirrup_lw, ec=stirrup_color, fc='none'))

    # 2. Main Reinforcement (Light Blue)
    main_color = '#3498db'
    main_lw = 4
    hook = 150
    
    # Top Compression Steel
    t1_y = level_diff + d0 - cc - 10
    ax.plot([cc, w1+step_w-cc], [t1_y, t1_y], color=main_color, lw=main_lw)
    ax.plot([cc, cc, cc+100], [t1_y, t1_y-hook, t1_y-hook], color=main_color, lw=main_lw)
    ax.plot([w1+step_w-cc, w1+step_w-cc], [t1_y, level_diff-100], color=main_color, lw=main_lw)
    
    t2_y = d0 - cc - 10
    ax.plot([w1+cc, w1+w2+step_w-cc], [t2_y, t2_y], color=main_color, lw=main_lw)
    ax.plot([w1+w2+step_w-cc, w1+w2+step_w-cc, w1+w2+step_w-cc-100], [t2_y, t2_y-hook, t2_y-hook], color=main_color, lw=main_lw)
    
    # Bottom Tension Steel
    b1_y = level_diff + cc + 10
    ax.plot([cc, w1+step_w-cc], [b1_y, b1_y], color=main_color, lw=main_lw)
    ax.plot([cc, cc, cc+100], [b1_y, b1_y+hook, b1_y+hook], color=main_color, lw=main_lw)
    
    b2_y = cc + 10
    ax.plot([w1+step_w+100, w1+w2+step_w-cc], [b2_y, b2_y], color=main_color, lw=main_lw)
    ax.plot([w1+w2+step_w-cc, w1+w2+step_w-cc, w1+w2+step_w-cc-100], [b2_y, b2_y+hook, b2_y+hook], color=main_color, lw=main_lw)
    ax.plot([w1+step_w+100, w1+cc], [b2_y, b2_y], color=main_color, lw=main_lw)
    ax.plot([w1+cc, w1+cc], [b2_y, d0+100], color=main_color, lw=main_lw)

    # 3. Corner L-Bar (Dark Blue)
    lbar_color = '#2980b9'
    lbar_y_left = level_diff + cc + 40
    lbar_y_right = d0 - cc - 40
    ax.plot([w1-800, w1+cc+30], [lbar_y_left, lbar_y_left], color=lbar_color, lw=3.5)
    ax.plot([w1+cc+30, w1+cc+30], [lbar_y_left, lbar_y_right], color=lbar_color, lw=3.5)
    ax.plot([w1+cc+30, w1+step_w+800], [lbar_y_right, lbar_y_right], color=lbar_color, lw=3.5)
    
    # 4. Diagonal Crack Control Bars (Red)
    diag_color = '#c0392b'
    diag_length = 1800
    angle = np.deg2rad(45)
    
    for offset in [-60, 0, 60]:
        dx = offset * np.cos(np.deg2rad(-45))
        dy = offset * np.sin(np.deg2rad(-45))
        
        start_x = re_entrant_x + dx - (diag_length/2)*np.cos(angle)
        start_y = re_entrant_y + dy - (diag_length/2)*np.sin(angle)
        end_x = re_entrant_x + dx + (diag_length/2)*np.cos(angle)
        end_y = re_entrant_y + dy + (diag_length/2)*np.sin(angle)
        
        ax.plot([start_x, end_x], [start_y, end_y], color=diag_color, lw=3.5)
        
        hook_sz = 60
        ax.plot([end_x, end_x + hook_sz*np.cos(angle-np.pi/2), end_x + hook_sz*np.cos(angle-np.pi/2) - hook_sz*np.cos(angle)], 
                [end_y, end_y + hook_sz*np.sin(angle-np.pi/2), end_y + hook_sz*np.sin(angle-np.pi/2) - hook_sz*np.sin(angle)], 
                color=diag_color, lw=3.5)
        
        ax.plot([start_x, start_x - hook_sz*np.cos(angle-np.pi/2), start_x - hook_sz*np.cos(angle-np.pi/2) + hook_sz*np.cos(angle)], 
                [start_y, start_y - hook_sz*np.sin(angle-np.pi/2), start_y - hook_sz*np.sin(angle-np.pi/2) + hook_sz*np.sin(angle)], 
                color=diag_color, lw=3.5)

    # 5. Annotations and Callouts
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
    
    ax.set_xlim(-200, w1+w2+step_w+200)
    ax.set_ylim(-400, d0+level_diff+400)
    
    return fig

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="Structural Beam Detailing")
st.title("🏗️ CAD-Style Beam Reinforcement Detailing")
st.markdown("ภาพจำลองแบบก่อสร้าง (Shop Drawing) แสดงการจัดเหล็กเสริมตามมาตรฐานวิศวกรรม")
st.markdown("---")

# ส่วนที่ 1: คานดรอปท้อง (Transition to Deep Beam)
st.subheader("1. คานดรอปท้อง / เปลี่ยนผ่านความลึก (Stepped-Bottom Transition)")
st.pyplot(draw_cad_transition_deep_beam())

st.markdown("---")

# ส่วนที่ 2: คานหักมุม (Stepped Beam / Z-Beam)
st.subheader("2. คานหักมุม (Stepped Beam / Z-Beam)")
st.pyplot(draw_cad_z_beam())
