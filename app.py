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

# --- นำไปแทนที่ส่วน Streamlit UI เดิมในหน้าหลัก ---
st.set_page_config(layout="wide", page_title="Structural Beam Detailing")
st.title("🏗️ CAD-Style Beam Reinforcement Detailing")

st.markdown("### คานดรอปท้อง / เปลี่ยนผ่านความลึก (Stepped-Bottom / Deep Beam Transition)")
st.pyplot(draw_cad_transition_deep_beam())

# สามารถเก็บ Z-Beam ของเดิมไว้ต่อด้านล่างได้ครับ
