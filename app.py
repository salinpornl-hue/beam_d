import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ==========================================
# 1. คานลดระดับด้านล่าง (Stepped-Bottom)
# ==========================================
def draw_cad_transition_deep_beam():
    fig, ax = plt.subplots(figsize=(14, 6))
    base_length = 6000
    L1 = 2200  
    d1 = 600   
    d2 = 1200  
    
    x_conc = [0, base_length, base_length, L1, L1, 0]
    y_conc = [d2, d2, 0, 0, d2-d1, d2-d1]
    poly = patches.Polygon(xy=list(zip(x_conc, y_conc)), closed=True, edgecolor='#111111', facecolor='#f8f9fa', lw=2)
    ax.add_patch(poly)
    
    cc = 40
    stirrup_color = '#95a5a6'
    main_color = '#3498db'
    diag_color = '#c0392b'
    
    for sx in range(cc+50, L1-50, 150):
        ax.add_patch(patches.Rectangle((sx, d2-d1+cc), 30, d1-2*cc, lw=2, ec=stirrup_color, fc='none'))
    for sx in range(L1+50, base_length-cc-50, 200):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d2-2*cc, lw=2, ec=stirrup_color, fc='none'))
        
    hook = 150
    ty = d2 - cc - 15
    ax.plot([cc, base_length-cc], [ty, ty], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [ty, ty-hook, ty-hook], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [ty, ty-hook, ty-hook], color=main_color, lw=4)
    
    by1 = d2 - d1 + cc + 15
    Ld_bottom = 1200 
    ax.plot([cc, L1 + Ld_bottom], [by1, by1], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [by1, by1+hook, by1+hook], color=main_color, lw=4)
    ax.plot([L1 + Ld_bottom, L1 + Ld_bottom, L1 + Ld_bottom - 50], [by1, by1-hook, by1-hook], color=main_color, lw=4)
    
    by2 = cc + 15
    ax.plot([L1+cc, base_length-cc], [by2, by2], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [by2, by2+hook, by2+hook], color=main_color, lw=4)
    ax.plot([L1+cc, L1+cc], [by2, by1-50], color=main_color, lw=4)
    
    ax.plot([cc, base_length-cc], [900, 900], color='#2980b9', lw=2.5) 
    ax.plot([L1+cc, base_length-cc], [300, 300], color='#2980b9', lw=2.5) 
    
    # เหล็กทแยงมุมกันร้าว
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
        hook_sz = 60
        ax.plot([ex, ex + hook_sz*np.cos(angle-np.pi/2)], [ey, ey + hook_sz*np.sin(angle-np.pi/2)], color=diag_color, lw=3)
        ax.plot([sx, sx - hook_sz*np.cos(angle-np.pi/2)], [sy, sy - hook_sz*np.sin(angle-np.pi/2)], color=diag_color, lw=3)
    
    # --- ระบุระยะ L_d ชัดเจน ---
    dim_y = by1 + 180
    ax.plot([L1, L1 + Ld_bottom], [dim_y, dim_y], color='black', lw=1.5)
    ax.plot([L1, L1], [by1, dim_y+30], color='black', lw=1, linestyle='--')
    ax.plot([L1 + Ld_bottom, L1 + Ld_bottom], [by1, dim_y+30], color='black', lw=1, linestyle='--')
    ax.annotate("", xy=(L1, dim_y), xytext=(L1 + Ld_bottom, dim_y), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(L1 + Ld_bottom/2, dim_y + 40, "Tension Dev. Length ($L_d$)", ha='center', fontsize=12, fontweight='bold', color='#2c3e50')
    
    # --- Annotations (เอาของเดิมกลับมา) ---
    arrow_props = dict(arrowstyle="->", color="black", lw=1.5)
    ax.text(L1/2, d2 - d1/2, "Normal Beam\nDepth = 600 mm", ha='center', va='center', fontsize=12, alpha=0.5)
    ax.text(L1 + (base_length-L1)/2, d2/2, "Deep Beam Segment\nDepth = 1200 mm", ha='center', va='center', fontsize=12, alpha=0.5)
    ax.annotate("Main bottom tension bar\nanchored into deep segment ($L_d$)", xy=(L1 + Ld_bottom/2, by1), xytext=(L1 + Ld_bottom/2, by1 + 300), arrowprops=arrow_props, fontsize=11, ha='center')
    ax.annotate("Diagonal Crack Control Bars\nat Soffit Step", xy=(rx + 200, ry + 200), xytext=(rx + 800, ry + 400), arrowprops=arrow_props, bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="black", lw=1), fontsize=11, ha='left')

    ax.set_title("Stepped-Bottom Beam: Transition Details", fontsize=16, pad=20, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-200, base_length+200)
    ax.set_ylim(-100, d2+400)
    return fig

# ==========================================
# 2. คานลดระดับด้านบน (Stepped-Top)
# ==========================================
def draw_cad_stepped_top_beam():
    fig, ax = plt.subplots(figsize=(16, 7))
    base_length = 6800
    L1 = 2800  
    d1 = 1200  
    d2 = 600   
    col_w = 400 
    
    col1 = patches.Rectangle((col_w, -600), col_w, 600, edgecolor='black', facecolor='#dcdde1', lw=1.5, hatch='//')
    col2 = patches.Rectangle((base_length - 2*col_w, -600), col_w, 600, edgecolor='black', facecolor='#dcdde1', lw=1.5, hatch='//')
    ax.add_patch(col1)
    ax.add_patch(col2)
    
    x_conc = [0, L1, L1, base_length, base_length, 0]
    y_conc = [d1, d1, d2, d2, 0, 0]
    poly = patches.Polygon(xy=list(zip(x_conc, y_conc)), closed=True, edgecolor='#111111', facecolor='#f8f9fa', lw=2.5)
    ax.add_patch(poly)
    
    cc = 40
    stirrup_color = '#7f8c8d'
    main_color = '#2980b9'
    diag_color = '#c0392b'
    
    for sx in range(cc+50, L1-50, 180):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d1-2*cc, lw=2, ec=stirrup_color, fc='none'))
    for sx in range(L1+20, L1+450, 80):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d2-2*cc, lw=2.5, ec='#e67e22', fc='none', linestyle='--')) 
    for sx in range(L1+450, base_length-cc-50, 150):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d2-2*cc, lw=2, ec=stirrup_color, fc='none'))
        
    hook = 150
    by = cc + 15
    ax.plot([cc, base_length-cc], [by, by], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [by, by+hook, by+hook], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [by, by+hook, by+hook], color=main_color, lw=4)
    
    ty2 = d2 - cc - 15
    Ld_top = 1500 
    ax.plot([L1 - Ld_top, base_length-cc], [ty2, ty2], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [ty2, ty2-hook, ty2-hook], color=main_color, lw=4)
    ax.plot([L1 - Ld_top, L1 - Ld_top, L1 - Ld_top + 50], [ty2, ty2+hook, ty2+hook], color=main_color, lw=4) 
    
    ty1 = d1 - cc - 15
    ax.plot([cc, L1-cc], [ty1, ty1], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [ty1, ty1-hook, ty1-hook], color=main_color, lw=4)
    ax.plot([L1-cc, L1-cc], [ty1, ty2-50], color=main_color, lw=4) 
    
    ax.plot([cc, L1-cc], [900, 900], color='#3498db', lw=2) 
    ax.plot([cc, base_length-cc], [300, 300], color='#3498db', lw=2) 
    
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
        
    # --- ระบุระยะ L_dh ---
    dim_y_top = ty2 + 250
    ax.plot([L1 - Ld_top, L1], [dim_y_top, dim_y_top], color='black', lw=1.5)
    ax.plot([L1 - Ld_top, L1 - Ld_top], [ty2, dim_y_top+30], color='black', lw=1, linestyle='--')
    ax.plot([L1, L1], [ty2, dim_y_top+30], color='black', lw=1, linestyle='--')
    ax.annotate("", xy=(L1 - Ld_top, dim_y_top), xytext=(L1, dim_y_top), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(L1 - Ld_top/2, dim_y_top + 40, "Hooked Dev. Length ($L_{dh}$)\nCritical section at face of step", ha='center', fontsize=11, fontweight='bold', color='#2c3e50')

    ax.plot([col_w*1.5, col_w*1.5], [-800, d1+200], color='red', linestyle='-.', lw=1)
    ax.plot([base_length - col_w*1.5, base_length - col_w*1.5], [-800, d2+200], color='red', linestyle='-.', lw=1)

    # --- Annotations (เอาของเดิมกลับมา) ---
    arrow_props = dict(arrowstyle="->", color="black", lw=1.5)
    bbox_alert = dict(boxstyle="round,pad=0.3", fc="#ffeaa7", ec="#e17055", lw=1.5)
    
    ax.annotate("D-Region (Disturbed Zone)\nNon-Linear Strain Distribution", xy=(rx, ry), xytext=(rx - 700, ry + 400), arrowprops=arrow_props, bbox=bbox_alert, fontsize=11, fontweight='bold', color='#d35400')
    ax.annotate("Closed Hairpin Stirrups\n(Resist Concrete Spalling Force)", xy=(L1 + 200, d2-cc), xytext=(L1 + 600, d2 - 400), arrowprops=arrow_props, fontsize=11, color='#d35400')
    
    ax.annotate("", xy=(-100, 0), xytext=(-100, d1), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(-150, d1/2, "$D_1 = 1200$ mm", va='center', ha='right', rotation=90, fontsize=12)
    ax.annotate("", xy=(base_length+100, 0), xytext=(base_length+100, d2), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(base_length+150, d2/2, "$D_2 = 600$ mm", va='center', ha='left', rotation=270, fontsize=12)
                
    ax.text(col_w*1.5, -400, "Support A", ha='center', fontsize=12, fontweight='bold')
    ax.text(base_length - col_w*1.5, -400, "Support B", ha='center', fontsize=12, fontweight='bold')

    ax.set_title("Stepped-Top Beam Detail", fontsize=16, pad=20, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-400, base_length+400)
    ax.set_ylim(-800, d1+500)
    return fig

# ==========================================
# 3. คานหักมุม (Z-Beam)
# ==========================================
def draw_cad_z_beam():
    fig, ax = plt.subplots(figsize=(14, 9))
    d0 = 600
    level_diff = 800
    w1, w2 = 1800, 1800
    step_w = 400
    
    x = [0, w1+step_w, w1+step_w, w1+w2+step_w, w1+w2+step_w, w1, w1, 0]
    y = [d0+level_diff, d0+level_diff, d0, d0, 0, 0, level_diff, level_diff]
    poly = patches.Polygon(xy=list(zip(x, y)), closed=True, edgecolor='black', facecolor='#f8f9fa', linewidth=2.5)
    ax.add_patch(poly)
    
    cc = 40
    re_entrant_x, re_entrant_y = w1, level_diff
    
    stirrup_color = '#95a5a6'
    stirrup_lw = 2
    for sx in range(cc+50, w1-50, 150):
        ax.add_patch(patches.Rectangle((sx, level_diff+cc), 30, d0-2*cc, lw=stirrup_lw, ec=stirrup_color, fc='none'))
    for sx in range(w1+20, w1+step_w-20, 120):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d0+level_diff-2*cc, lw=stirrup_lw, ec=stirrup_color, fc='none'))
    for sx in range(w1+step_w+50, w1+w2+step_w-50, 150):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d0-2*cc, lw=stirrup_lw, ec=stirrup_color, fc='none'))

    main_color = '#3498db'
    main_lw = 4
    hook = 150
    
    t1_y = level_diff + d0 - cc - 10
    ax.plot([cc, w1+step_w-cc], [t1_y, t1_y], color=main_color, lw=main_lw)
    ax.plot([cc, cc, cc+100], [t1_y, t1_y-hook, t1_y-hook], color=main_color, lw=main_lw)
    ax.plot([w1+step_w-cc, w1+step_w-cc], [t1_y, level_diff-100], color=main_color, lw=main_lw)
    
    t2_y = d0 - cc - 10
    ax.plot([w1+cc, w1+w2+step_w-cc], [t2_y, t2_y], color=main_color, lw=main_lw)
    ax.plot([w1+w2+step_w-cc, w1+w2+step_w-cc, w1+w2+step_w-cc-100], [t2_y, t2_y-hook, t2_y-hook], color=main_color, lw=main_lw)
    
    b1_y = level_diff + cc + 10
    ax.plot([cc, w1+step_w-cc], [b1_y, b1_y], color=main_color, lw=main_lw)
    ax.plot([cc, cc, cc+100], [b1_y, b1_y+hook, b1_y+hook], color=main_color, lw=main_lw)
    
    b2_y = cc + 10
    ax.plot([w1+step_w+100, w1+w2+step_w-cc], [b2_y, b2_y], color=main_color, lw=main_lw)
    ax.plot([w1+w2+step_w-cc, w1+w2+step_w-cc, w1+w2+step_w-cc-100], [b2_y, b2_y+hook, b2_y+hook], color=main_color, lw=main_lw)
    ax.plot([w1+step_w+100, w1+cc], [b2_y, b2_y], color=main_color, lw=main_lw)
    ax.plot([w1+cc, w1+cc], [b2_y, d0+100], color=main_color, lw=main_lw)

    # L-Bars
    lbar_color = '#2980b9'
    lbar_y_left = level_diff + cc + 40
    lbar_y_right = d0 - cc - 40
    Ld_Lbar = 1000 
    ax.plot([w1 - Ld_Lbar, w1+cc+30], [lbar_y_left, lbar_y_left], color=lbar_color, lw=3.5)
    ax.plot([w1+cc+30, w1+cc+30], [lbar_y_left, lbar_y_right], color=lbar_color, lw=3.5)
    ax.plot([w1+cc+30, w1+step_w + Ld_Lbar], [lbar_y_right, lbar_y_right], color=lbar_color, lw=3.5)
    
    # --- เหล็กทแยงมุมกันร้าว (Diagonal Steel) (เอาของเดิมกลับมา) ---
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
    
    # --- ระบุระยะ L_d สำหรับ Z-Beam ---
    dim_y_top = lbar_y_left + 150
    ax.plot([w1 - Ld_Lbar, w1], [dim_y_top, dim_y_top], color='black', lw=1.5)
    ax.plot([w1 - Ld_Lbar, w1 - Ld_Lbar], [lbar_y_left, dim_y_top+30], color='black', lw=1, linestyle='--')
    ax.plot([w1, w1], [level_diff, dim_y_top+30], color='black', lw=1, linestyle='--')
    ax.annotate("", xy=(w1 - Ld_Lbar, dim_y_top), xytext=(w1, dim_y_top), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(w1 - Ld_Lbar/2, dim_y_top + 40, "$L_d$ (Tension)", ha='center', fontsize=11, fontweight='bold')

    dim_y_bot = lbar_y_right - 150
    ax.plot([w1+step_w, w1+step_w + Ld_Lbar], [dim_y_bot, dim_y_bot], color='black', lw=1.5)
    ax.plot([w1+step_w, w1+step_w], [lbar_y_right, dim_y_bot-30], color='black', lw=1, linestyle='--')
    ax.plot([w1+step_w + Ld_Lbar, w1+step_w + Ld_Lbar], [lbar_y_right, dim_y_bot-30], color='black', lw=1, linestyle='--')
    ax.annotate("", xy=(w1+step_w, dim_y_bot), xytext=(w1+step_w + Ld_Lbar, dim_y_bot), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(w1+step_w + Ld_Lbar/2, dim_y_bot - 80, "$L_d$ (Tension)", ha='center', fontsize=11, fontweight='bold')

    # --- Annotations (เอาของเดิมกลับมา) ---
    bbox_props = dict(boxstyle="square,pad=0.3", fc="white", ec="black", lw=1)
    arrow_props = dict(arrowstyle="->", color="black", lw=1.5)
    
    ax.annotate("Compression Steel", xy=(w1-400, t1_y), xytext=(w1-800, t1_y+150), arrowprops=arrow_props, fontsize=11, ha='center')
    ax.annotate("Main Tension", xy=(w1-600, b1_y), xytext=(w1-800, b1_y-150), arrowprops=arrow_props, fontsize=11, ha='center')
    ax.annotate("Corner L-Bar", xy=(w1+cc+30, (lbar_y_left+lbar_y_right)/2), xytext=(w1+800, (lbar_y_left+lbar_y_right)/2 + 100), arrowprops=arrow_props, fontsize=11, ha='center')
    ax.annotate("Stirrups", xy=(w1+w2+step_w-400, d0-cc), xytext=(w1+w2+step_w-200, d0+100), arrowprops=arrow_props, fontsize=11, ha='center')
    ax.annotate("Diagonal Crack Control Steel\nwith proper $L_d$ anchorage.", xy=(re_entrant_x + 300, re_entrant_y + 300), xytext=(re_entrant_x + 1000, re_entrant_y + 400), arrowprops=arrow_props, bbox=bbox_props, fontsize=11, ha='center')
    ax.annotate("Diagonal Steel with\nstir re-entrant bars.", xy=(re_entrant_x - 300, re_entrant_y - 300), xytext=(re_entrant_x - 700, re_entrant_y - 450), arrowprops=arrow_props, fontsize=11, ha='center')

    ax.set_title("Z-Beam / Re-entrant Corner Detailing (Constructable Standard)", fontsize=16, pad=20, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-200, w1+w2+step_w+200)
    ax.set_ylim(-400, d0+level_diff+400) # ปรับ y-lim ให้ครอบคลุม text
    return fig

# ==========================================
# ส่วน UI ของ Streamlit
# ==========================================
st.set_page_config(layout="wide", page_title="Senior Structural Detailing System")
st.title("🏗️ Senior Structural Detailing System")
st.markdown("เน้นการแสดงผลระยะฝังล้วงยึดเหนี่ยว ($L_d$ / $L_{dh}$) บริเวณจุดวิกฤต ตามมาตรฐาน ACI 318")

with st.expander("📌 Engineering Note: ทำไมการระบุ $L_d$ ให้ชัดเจนถึงสำคัญ?", expanded=True):
    st.markdown("""
    ในฐานะวิศวกรผู้ออกแบบ **การโยนภาระให้ Draftsman กะระยะเหล็กเอาเองบริเวณ D-Region คือความเสี่ยงร้ายแรง**
    *   **$L_d$ (Development Length):** ระยะล้วงเหล็กเส้นตรง ต้องคำนวณตามกำลังอัดคอนกรีต ($f'_c$) และกำลังรับแรงดึงเหล็ก ($f_y$) หากพื้นที่ไม่พอ ต้องเปลี่ยนไปใช้งอขอ ($L_{dh}$) หรือ Mechanical Splice
    *   **จุดเริ่มวัด (Critical Section):** ต้องระบุให้ชัดเจนว่าเริ่มวัดจากขอบหน้าตัด (Face of Support / Face of Step) ไม่ใช่วัดรวมไปตั้งแต่งอฉาก
    *   **ทิศทางของแรง (Load Path):** บริเวณคานหักมุม (Z-Beam) เหล็กเสริมมุม (Corner L-Bar) มีแนวโน้มจะถีบตัวออก (Spalling) ทำให้อาจต้องพิจารณา $L_d$ เผื่อเพิ่มขึ้นจากโซนรับแรงดึงปกติ 
    """)

with st.sidebar:
    st.header("⚙️ เลือกประเภทโครงสร้าง")
    beam_selection = st.radio(
        "โครงสร้างที่ต้องการตรวจสอบ:",
        (
            "1. คานลดระดับด้านล่าง (Stepped-Bottom)",
            "2. คานลดระดับด้านบน (Stepped-Top)",
            "3. คานหักมุมซิกแซก (Stepped / Z-Beam)"
        )
    )

if beam_selection == "1. คานลดระดับด้านล่าง (Stepped-Bottom)":
    st.pyplot(draw_cad_transition_deep_beam())
elif beam_selection == "2. คานลดระดับด้านบน (Stepped-Top)":
    st.pyplot(draw_cad_stepped_top_beam())
else:
    st.pyplot(draw_cad_z_beam())
