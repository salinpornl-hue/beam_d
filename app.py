import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_cad_deep_beam(base_length=6000, depth=1200):
    """
    วาด Deep Beam สไตล์ CAD Detailing (หน่วยเป็น mm)
    """
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # 1. วาดคอนกรีต (เส้นประสีเทาเข้ม)
    rect = patches.Rectangle((0, 0), base_length, depth, linewidth=2, edgecolor='#333333', facecolor='none', linestyle='--')
    ax.add_patch(rect)
    
    # 2. ระยะหุ้ม (Clear Cover)
    cc = 40 # 40 mm clear cover
    
    # 3. วาดเหล็กปลอก (Closed Stirrups) - สีน้ำเงิน
    spacing = 250
    stirrup_x = range(cc + 50, base_length - cc, spacing)
    for x in stirrup_x:
        # วาดรูปสี่เหลี่ยมแทนเหล็กปลอก
        stirrup = patches.Rectangle((x, cc), 20, depth - 2*cc, linewidth=1.5, edgecolor='#2980b9', facecolor='none')
        ax.add_patch(stirrup)
        
    # 4. วาดเหล็กเสริมหลัก (Main Bottom Rebar) พร้อมขอเกี่ยว 90 องศา - สีแดง
    rebar_y = cc + 10 # ขยับขึ้นจากเหล็กปลอกนิดหน่อย
    hook_length = 250
    
    # เส้นนอน
    ax.plot([cc, base_length - cc], [rebar_y, rebar_y], color='#c0392b', linewidth=4, label='Main Bottom Rebar (with hooks)')
    # ขอเกี่ยวซ้าย (งอขึ้น)
    ax.plot([cc, cc], [rebar_y, rebar_y + hook_length], color='#c0392b', linewidth=4)
    # ขอเกี่ยวขวา (งอขึ้น)
    ax.plot([base_length - cc, base_length - cc], [rebar_y, rebar_y + hook_length], color='#c0392b', linewidth=4)
    
    # วาดเหล็กเสริมหลักด้านบน (Top Rebar) 
    top_y = depth - cc - 10
    ax.plot([cc, base_length - cc], [top_y, top_y], color='#c0392b', linewidth=3)
    ax.plot([cc, cc], [top_y, top_y - hook_length], color='#c0392b', linewidth=3)
    ax.plot([base_length - cc, base_length - cc], [top_y, top_y - hook_length], color='#c0392b', linewidth=3)
    
    # 5. วาดเหล็กด้านข้าง (Skin Reinforcement) - สีเขียว
    # ต้องผูกติดกับเหล็กปลอกด้านใน
    num_skin_bars = int(depth / 300) # ระยะห่างประมาณ 300mm
    for i in range(1, num_skin_bars):
        y_pos = i * 300
        # ลากเส้นยาวตลอดแนว
        ax.plot([cc, base_length - cc], [y_pos, y_pos], color='#27ae60', linewidth=2)
        # วาดจุด (หน้าตัดเหล็ก) ตรงตำแหน่งที่ตัดกับเหล็กปลอก
        for x in stirrup_x:
            ax.plot(x, y_pos, marker='o', markersize=4, color='#27ae60')

    ax.set_title("Deep Beam Reinforcement Detailing (CAD Style)", fontsize=14, pad=15)
    ax.set_xlim(-200, base_length + 200)
    ax.set_ylim(-100, depth + 100)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # เพิ่ม Grid หรือเส้นบอกขนาด (Dimension lines) แบบคร่าวๆ
    ax.plot([0, base_length], [-60, -60], color='black', linewidth=1)
    ax.plot([0, 0], [-50, -70], color='black', linewidth=1)
    ax.plot([base_length, base_length], [-50, -70], color='black', linewidth=1)
    ax.text(base_length/2, -120, f"Span = {base_length} mm", ha='center', fontsize=10)
    
    return fig

def draw_cad_z_beam(level_diff=800):
    """
    วาด Z-Beam เน้นจุดวิกฤต Re-entrant Corner (หน่วยเป็น mm)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    base_length = 4000
    d0 = 500 # ความลึกคานมาตรฐาน
    cc = 40  # Clear cover
    
    # พิกัดคอนกรีต
    x = [0, 2000, 2000, base_length, base_length, 1500, 1500, 0]
    y = [d0+level_diff, d0+level_diff, d0, d0, 0, 0, level_diff, level_diff]
    
    poly = patches.Polygon(xy=list(zip(x, y)), closed=True, edgecolor='#333333', facecolor='#f8f9fa', linewidth=2)
    ax.add_patch(poly)
    
    # --- การใส่เหล็กหลัก (Main Rebar) ---
    # เหล็กบน (ยื่นจากซ้ายมาขวา แล้วหักงอลงเพื่อล้วงในคานล่าง)
    top_y1 = d0 + level_diff - cc
    ax.plot([cc, 1900], [top_y1, top_y1], color='#2980b9', linewidth=3)
    # งอลงมาล้วงระยะ Ld
    ax.plot([1900, 1900], [top_y1, d0/2], color='#2980b9', linewidth=3) 
    
    # เหล็กล่าง (ยื่นจากขวามาซ้าย แล้วหักงอขึ้นเพื่อล้วงในคานบน)
    bot_y2 = cc
    ax.plot([base_length-cc, 1600], [bot_y2, bot_y2], color='#2980b9', linewidth=3)
    # งอขึ้นไปล้วงระยะ Ld
    ax.plot([1600, 1600], [bot_y2, level_diff + d0/2], color='#2980b9', linewidth=3)
    
    # --- เหล็กกันร้าวมุม (Diagonal Re-entrant Bars) ---
    # จุดวิกฤตคือพิกัด (1500, level_diff) มุมหักด้านใน
    corner_x, corner_y = 1500, level_diff
    
    # วาดแนวรอยร้าวสมมติ (Crack Plane) 45 องศา
    ax.plot([corner_x-300, corner_x+300], [corner_y+300, corner_y-300], color='gray', linestyle='--', alpha=0.5)
    
    # วาดเหล็กทแยง (ตั้งฉากกับรอยร้าว) ให้ล้วงผ่านรอยร้าวไปฝั่งละ Ld (สมมติ 600mm)
    Ld_diag = 600
    for offset in [-50, 0, 50]: # ใส่เหล็กทแยง 3 เส้น
        start_x = corner_x - Ld_diag + offset
        start_y = corner_y - Ld_diag - offset
        end_x = corner_x + Ld_diag + offset
        end_y = corner_y + Ld_diag - offset
        
        ax.plot([start_x, end_x], [start_y, end_y], color='#c0392b', linewidth=3)
        # ใส่ขอเกี่ยวปลายเหล็กทแยง (Hook)
        ax.plot([start_x, start_x+40], [start_y, start_y-40], color='#c0392b', linewidth=3)
        ax.plot([end_x, end_x-40], [end_y, end_y+40], color='#c0392b', linewidth=3)

    ax.text(corner_x, corner_y + 400, "Diagonal Bars with proper $L_d$ anchorage", color='#c0392b', ha='center', fontsize=11)
    
    ax.set_title("Stepped Beam / Re-entrant Corner Detailing", fontsize=14, pad=15)
    ax.set_aspect('equal')
    ax.axis('off')
    
    return fig

# --- ส่วน UI ของ Streamlit ---
st.set_page_config(layout="wide")
st.title("CAD-Style Beam Reinforcement Detailing")

col1, col2 = st.columns([1, 1])
with col1:
    st.pyplot(draw_cad_deep_beam())
with col2:
    st.pyplot(draw_cad_z_beam())
