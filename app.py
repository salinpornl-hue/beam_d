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
    
    # Concrete outline
    x_conc = [0, base_length, base_length, L1, L1, 0]
    y_conc = [d2, d2, 0, 0, d2-d1, d2-d1]
    poly = patches.Polygon(xy=list(zip(x_conc, y_conc)), closed=True, edgecolor='#111111', facecolor='#f8f9fa', lw=2)
    ax.add_patch(poly)
    
    cc = 40
    stirrup_color = '#95a5a6'
    main_color = '#3498db'
    diag_color = '#c0392b'
    
    # Stirrups
    for sx in range(cc+50, L1-50, 150):
        ax.add_patch(patches.Rectangle((sx, d2-d1+cc), 30, d1-2*cc, lw=2, ec=stirrup_color, fc='none'))
    for sx in range(L1+50, base_length-cc-50, 200):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d2-2*cc, lw=2, ec=stirrup_color, fc='none'))
        
    hook = 150
    # Top main bars
    ty = d2 - cc - 15
    ax.plot([cc, base_length-cc], [ty, ty], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [ty, ty-hook, ty-hook], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [ty, ty-hook, ty-hook], color=main_color, lw=4)
    
    # Bottom main bars (Normal beam into Deep beam)
    by1 = d2 - d1 + cc + 15
    Ld_bottom = 1200 
    ax.plot([cc, L1 + Ld_bottom], [by1, by1], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [by1, by1+hook, by1+hook], color=main_color, lw=4)
    ax.plot([L1 + Ld_bottom, L1 + Ld_bottom, L1 + Ld_bottom - 50], [by1, by1-hook, by1-hook], color=main_color, lw=4)
    
    # Bottom main bars (Deep beam)
    by2 = cc + 15
    ax.plot([L1+cc, base_length-cc], [by2, by2], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [by2, by2+hook, by2+hook], color=main_color, lw=4)
    ax.plot([L1+cc, L1+cc], [by2, by1-50], color=main_color, lw=4)
    
    # Skin reinforcement
    ax.plot([cc, base_length-cc], [900, 900], color='#2980b9', lw=2.5) 
    ax.plot([L1+cc, base_length-cc], [300, 300], color='#2980b9', lw=2.5) 
    
    # Diagonal bars
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
    
    # --- ระบุระยะ L_d ชัดเจน ---
    dim_y = by1 + 180
    ax.plot([L1, L1 + Ld_bottom], [dim_y, dim_y], color='black', lw=1.5) # เส้นบอกระยะ
    ax.plot([L1, L1], [by1, dim_y+30], color='black', lw=1, linestyle='--') # เส้นอ้างอิงจุดเริ่ม
    ax.plot([L1 + Ld_bottom, L1 + Ld_bottom], [by1, dim_y+30], color='black', lw=1, linestyle='--') # เส้นอ้างอิงจุดจบ
    ax.annotate("", xy=(L1, dim_y), xytext=(L1 + Ld_bottom, dim_y), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(L1 + Ld_bottom/2, dim_y + 40, "Tension Dev. Length ($L_d$)", ha='center', fontsize=12, fontweight='bold', color='#2c3e50')
    
    ax.text(L1/2, d2 - d1/2, "Normal Beam", ha='center', va='center', fontsize=12, alpha=0.5)
    ax.text(L1 + (base_length-L1)/2, d2/2, "Deep Beam Segment", ha='center', va='center', fontsize=12, alpha=0.5)

    ax.set_title("Stepped-Bottom Beam: Transition Details", fontsize=16, pad=20, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-200, base_length+200)
    ax.set_ylim(-100, d2+300)
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
    
    # Stirrups
    for sx in range(cc+50, L1-50, 180):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d1-2*cc, lw=2, ec=stirrup_color, fc='none'))
    for sx in range(L1+20, L1+450, 80):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d2-2*cc, lw=2.5, ec='#e67e22', fc='none', linestyle='--')) 
    for sx in range(L1+450, base_length-cc-50, 150):
        ax.add_patch(patches.Rectangle((sx, cc), 30, d2-2*cc, lw=2, ec=stirrup_color, fc='none'))
        
    hook = 150
    # Bottom Rebar
    by = cc + 15
    ax.plot([cc, base_length-cc], [by, by], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [by, by+hook, by+hook], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [by, by+hook, by+hook], color=main_color, lw=4)
    
    # Top Rebar Transition (Normal beam into Deep beam)
    ty2 = d2 - cc - 15
    Ld_top = 1500 # สมมติระยะล้วงยึดเหนี่ยวที่ต้องการ
    ax.plot([L1 - Ld_top, base_length-cc], [ty2, ty2], color=main_color, lw=4)
    ax.plot([base_length-cc, base_length-cc, base_length-cc-50], [ty2, ty2-hook, ty2-hook], color=main_color, lw=4)
    ax.plot([L1 - Ld_top, L1 - Ld_top, L1 - Ld_top + 50], [ty2, ty2+hook, ty2+hook], color=main_color, lw=4) 
    
    # Top Rebar (Deep beam)
    ty1 = d1 - cc - 15
    ax.plot([cc, L1-cc], [ty1, ty1], color=main_color, lw=4)
    ax.plot([cc, cc, cc+50], [ty1, ty1-hook, ty1-hook], color=main_color, lw=4)
    ax.plot([L1-cc, L1-cc], [ty1, ty2-50], color=main_color, lw=4) 
    
    # Skin Rebar
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
        
    # --- ระบุระยะ L_dh และ L_d ชัดเจน ---
    dim_y_top = ty2 + 250
    ax.plot([L1 - Ld_top, L1], [dim_y_top, dim_y_top], color='black', lw=1.5)
    ax.plot([L1 - Ld_top, L1 - Ld_top], [ty2, dim_y_top+30], color='black', lw=1, linestyle='--')
    ax.plot([L1, L1], [ty2, dim_y_top+30], color='black', lw=1, linestyle='--')
    ax.annotate("", xy=(L1 - Ld_top, dim_y_top), xytext=(L1, dim_y_top), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(L1 - Ld_top/2, dim_y_top + 40, "Hooked Dev. Length ($L_{dh}$)\nCritical section at face of step", ha='center', fontsize=11, fontweight='bold', color='#2c3e50')

    # Column markers
    ax.plot([col_w*1.5, col_w*1.5], [-800, d1+200], color='red', linestyle='-.', lw=1)
    ax.plot([base_length - col_w*1.5, base_length - col_w*1.5], [-800, d2+200], color='red', linestyle='-.', lw=1)

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
    ax.plot([w1+step_w-cc, w1+step_w-cc], [t1_y, level_diff-100], color=main_color, lw=main_lw)
    
    t2_y = d0 - cc - 10
    ax.plot([w1+cc, w1+w2+step_w-cc], [t2_y, t2_y], color=main_color, lw=main_lw)
    
    b1_y = level_diff + cc + 10
    ax.plot([cc, w1+step_w-cc], [b1_y, b1_y], color=main_color, lw=main_lw)
    
    b2_y = cc + 10
    ax.plot([w1+step_w+100, w1+w2+step_w-cc], [b2_y, b2_y], color=main_color, lw=main_lw)
    ax.plot([w1+step_w+100, w1+cc], [b2_y, b2_y], color=main_color, lw=main_lw)
    ax.plot([w1+cc, w1+cc], [b2_y, d0+100], color=main_color, lw=main_lw)

    # Corner L-Bars (Tension continuity)
    lbar_color = '#2980b9'
    lbar_y_left = level_diff + cc + 40
    lbar_y_right = d0 - cc - 40
    
    Ld_Lbar = 1000 # ระยะล้วงเหล็กฉาก
    ax.plot([w1 - Ld_Lbar, w1+cc+30], [lbar_y_left, lbar_y_left], color=lbar_color, lw=3.5)
    ax.plot([w1+cc+30, w1+cc+30], [lbar_y_left, lbar_y_right], color=lbar_color, lw=3.5)
    ax.plot([w1+cc+30, w1+step_w + Ld_Lbar], [lbar_y_right, lbar_y_right], color=lbar_color, lw=3.5)
    
    # --- ระบุระยะ L_d สำหรับ Z-Beam (2 แกน X, Y) ---
    # 1. L_d แกน X ด้านซ้าย (Top segment tension)
    dim_y_top = lbar_y_left + 150
    ax.plot([w1 - Ld_Lbar, w1], [dim_y_top, dim_y_top], color='black', lw=1.5)
    ax.plot([w1 - Ld_Lbar, w1 - Ld_Lbar], [lbar_y_left, dim_y_top+30], color='black', lw=1, linestyle='--')
    ax.plot([w1, w1], [level_diff, dim_y_top+30], color='black', lw=1, linestyle='--')
    ax.annotate("", xy=(w1 - Ld_Lbar, dim_y_top), xytext=(w1, dim_y_top), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(w1 - Ld_Lbar/2, dim_y_top + 40, "$L_d$ (Tension)", ha='center', fontsize=11, fontweight='bold')

    # 2. L_d แกน X ด้านขวา (Bottom segment tension)
    dim_y_bot = lbar_y_right - 150
    ax.plot([w1+step_w, w1+step_w + Ld_Lbar], [dim_y_bot, dim_y_bot], color='black', lw=1.5)
    ax.plot([w1+step_w, w1+step_w], [lbar_y_right, dim_y_bot-30], color='black', lw=1, linestyle='--')
    ax.plot([w1+step_w + Ld_Lbar, w1+step_w + Ld_Lbar], [lbar_y_right, dim_y_bot-30], color='black', lw=1, linestyle='--')
    ax.annotate("", xy=(w1+step_w, dim_y_bot), xytext=(w1+step_w + Ld_Lbar, dim_y_bot), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(w1+step_w + Ld_Lbar/2, dim_y_bot - 80, "$L_d$ (Tension)", ha='center', fontsize=11, fontweight='bold')

    ax.set_title("Z-Beam / Re-entrant Corner Detailing (Constructable Standard)", fontsize=16, pad=20, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-200, w1+w2+step_w+200)
    ax.set_ylim(-300, d0+level_diff+400)
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
