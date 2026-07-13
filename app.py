import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_cad_stepped_top_beam():
    """ 2. คานลดระดับด้านบน (Stepped-Top Beam) พร้อม Detail ละเอียด """
    fig, ax = plt.subplots(figsize=(16, 7))
    base_length = 6800
    L1 = 2800  # ความยาวช่วงคานลึก (ซ้าย)
    d1 = 1200  # Deep Beam Depth
    d2 = 600   # Normal Beam Depth
    col_w = 400 # Column width
    
    # --- พิกัดเสารองรับ (Columns) ---
    col1 = patches.Rectangle((col_w, -600), col_w, 600, edgecolor='black', facecolor='#dcdde1', lw=1.5, hatch='//')
    col2 = patches.Rectangle((base_length - 2*col_w, -600), col_w, 600, edgecolor='black', facecolor='#dcdde1', lw=1.5, hatch='//')
    ax.add_patch(col1)
    ax.add_patch(col2)
    
    # --- พิกัดคอนกรีตคาน ---
    x_conc = [0, L1, L1, base_length, base_length, 0]
    y_conc = [d1, d1, d2, d2, 0, 0]
    poly = patches.Polygon(xy=list(zip(x_conc, y_conc)), closed=True, edgecolor='#111111', facecolor='#f8f9fa', lw=2.5)
    ax.add_patch(poly)
    
    cc = 40
    stirrup_color = '#7f8c8d'
    main_color = '#2980b9'
    diag_color = '#c0392b'
    
    # 1. เหล็กปลอก (Stirrups)
    for sx in range(cc+50, L1-50, 180):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d1-2*cc, lw=2, ec=stirrup_color, fc='none'))
    # บริเวณ D-Region (เพิ่มปลอกถี่พิเศษ)
    for sx in range(L1+20, L1+450, 80):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d2-2*cc, lw=2.5, ec='#e67e22', fc='none', linestyle='--')) 
    for sx in range(L1+450, base_length-cc-50, 150):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d2-2*cc, lw=2, ec=stirrup_color, fc='none'))
        
    hook = 150
    # 2. เหล็กเสริมหลักด้านล่าง (Bottom Rebar)
    by = cc + 15
    ax.plot([cc, base_length-cc], [by, by], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [by, by+hook, by+hook], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [by, by+hook, by+hook], color=main_color, lw=4)
    
    # 3. เหล็กเสริมหลักด้านบน ช่วงคานตื้น ล้วงเข้าคานลึก (Top Rebar Transition)
    ty2 = d2 - cc - 15
    Ld = 1400
    ax.plot([L1 - Ld, base_length-cc], [ty2, ty2], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [ty2, ty2-hook, ty2-hook], color=main_color, lw=4)
    ax.plot([L1 - Ld, L1 - Ld, L1 - Ld + 50], [ty2, ty2+hook, ty2+hook], color=main_color, lw=4) # งอฉากที่ปลาย Ld
    
    # 4. เหล็กเสริมหลักด้านบน ช่วงคานลึก
    ty1 = d1 - cc - 15
    ax.plot([cc, L1-cc], [ty1, ty1], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [ty1, ty1-hook, ty1-hook], color=main_color, lw=4)
    ax.plot([L1-cc, L1-cc], [ty1, ty2-50], color=main_color, lw=4) # งอทิ่มลงมาสอดใต้เหล็กบนคานตื้น
    
    # 5. เหล็กเสริมด้านข้าง (Skin Reinforcement)
    ax.plot([cc, L1-cc], [900, 900], color='#3498db', lw=2) 
    ax.plot([cc, base_length-cc], [300, 300], color='#3498db', lw=2) 
    
    # 6. เหล็กทแยงเย็บมุมหัก (Diagonal Crack Control)
    rx, ry = L1, d2
    diag_len = 1200
    angle = np.deg2rad(45)
    for offset in [-60, 0, 60]:
        dx = offset * np.cos(np.deg2rad(-45))
        dy = offset * np.sin(np.deg2rad(-45))
        sx = rx + dx - (diag_len/2)*np.cos(angle)
        sy = ry + dy - (diag_len/2)*np.sin(angle)
        ex = rx + dx + (diag_len/2)*np.cos(angle)
        ey = ry + dy + (diag_len/2)*np.sin(angle)
        ax.plot([sx, ex], [sy, ey], color=diag_color, lw=3.5)
        
    # --- Annotations & Dimensions ---
    # Centerlines
    ax.plot([col_w*1.5, col_w*1.5], [-800, d1+200], color='red', linestyle='-.', lw=1)
    ax.plot([base_length - col_w*1.5, base_length - col_w*1.5], [-800, d2+200], color='red', linestyle='-.', lw=1)
    
    # L_d Dimension
    dim_y = ty2 + 250
    ax.plot([L1 - Ld, L1], [dim_y, dim_y], color='black', lw=1.5)
    ax.plot([L1 - Ld, L1 - Ld], [ty2, dim_y+30], color='black', lw=1, linestyle=':')
    ax.plot([L1, L1], [ty2, dim_y+30], color='black', lw=1, linestyle=':')
    ax.annotate("", xy=(L1 - Ld, dim_y), xytext=(L1, dim_y), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(L1 - Ld/2, dim_y + 40, "Tension Dev. Length ($L_d$)\nRequired for Continuous Action", ha='center', fontsize=11, color='blue')

    # Depth Dimensions
    ax.annotate("", xy=(-100, 0), xytext=(-100, d1), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(-150, d1/2, "$D_1 = 1200$ mm", va='center', ha='right', rotation=90, fontsize=12)
    
    ax.annotate("", xy=(base_length+100, 0), xytext=(base_length+100, d2), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(base_length+150, d2/2, "$D_2 = 600$ mm", va='center', ha='left', rotation=270, fontsize=12)

    # Callouts
    arrow_props = dict(arrowstyle="->", color="black", lw=1.5)
    bbox_alert = dict(boxstyle="round,pad=0.3", fc="#ffeaa7", ec="#e17055", lw=1.5)
    
    ax.annotate("D-Region (Disturbed Zone)\nNon-Linear Strain Distribution", xy=(rx, ry), xytext=(rx - 700, ry + 400),
                arrowprops=arrow_props, bbox=bbox_alert, fontsize=11, fontweight='bold', color='#d35400')
                
    ax.annotate("Closed Hairpin Stirrups\n(Resist Concrete Spalling Force)", xy=(L1 + 200, d2-cc), xytext=(L1 + 600, d2 - 400),
                arrowprops=arrow_props, fontsize=11, color='#d35400')
                
    ax.text(col_w*1.5, -400, "Support A", ha='center', fontsize=12, fontweight='bold')
    ax.text(base_length - col_w*1.5, -400, "Support B", ha='center', fontsize=12, fontweight='bold')

    ax.set_title("Stepped-Top Beam Detail (Continuous Bending Moment Transfer)", fontsize=16, pad=20, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-400, base_length+400)
    ax.set_ylim(-800, d1+500)
    return fig

# --- Streamlit UI (เฉพาะฟังก์ชัน Stepped-Top) ---
st.set_page_config(layout="wide", page_title="Structural Beam Detailing System")
st.title("🏗️ Professional Beam Detailing Visualization System")

st.markdown("### คานลดระดับด้านบน (Stepped-Top Beam) พร้อม Detail ระดับวิศวกรรม")
st.pyplot(draw_cad_stepped_top_beam())

st.info("**หมายเหตุทางวิศวกรรม:** หากหน้างานจริงไม่สามารถล้วงเหล็ก $L_d$ ได้ลึกพอตามที่คำนวณ วิศวกรจะต้องเปลี่ยนสมมติฐานการออกแบบให้จุดเปลี่ยนระดับนี้เป็น **Hinge (M=0)** และออกแบบคานขวาให้เป็น Simple Beam แทน")
