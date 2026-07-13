import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_deep_beam(level_diff):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # กำหนดขนาดคานพื้นฐาน
    beam_length = 600
    beam_depth = 100 + level_diff  # ความลึกคานแปรผันตามระดับที่เพิ่ม
    
    # วาดคอนกรีต
    rect = patches.Rectangle((0, 0), beam_length, beam_depth, linewidth=2, edgecolor='black', facecolor='#e0e0e0')
    ax.add_patch(rect)
    
    # จำลองการกระจายแรง (Strut and Tie Model)
    # Compression Struts (สีน้ำเงิน)
    ax.plot([50, 300], [beam_depth, 50], color='blue', linestyle='--', linewidth=3, alpha=0.5, label='Compression Strut (แรงอัด)')
    ax.plot([550, 300], [beam_depth, 50], color='blue', linestyle='--', linewidth=3, alpha=0.5)
    
    # Tension Tie (สีแดง - เหล็กเสริมรับแรงดึงหลัก)
    ax.plot([50, 550], [50, 50], color='red', linewidth=4, label='Main Tension Rebar (เหล็กนอน)')
    
    # เหล็กเสริมกันร้าว (Skin Reinforcement) ที่ต้องมีใน Deep Beam
    num_skin_bars = int(beam_depth / 30)
    for i in range(1, num_skin_bars):
        y_pos = i * 30
        if y_pos < beam_depth - 20:
            ax.plot([20, 580], [y_pos, y_pos], color='green', linewidth=1, linestyle='-.')
            
    # เหล็กปลอก (Stirrups)
    for x in range(50, 560, 40):
        ax.plot([x, x], [20, beam_depth-20], color='orange', linewidth=1.5)
        
    ax.set_xlim(-50, beam_length + 50)
    ax.set_ylim(-50, beam_depth + 50)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Deep Beam (คานลึก): Strut-and-Tie Model & Skin Reinforcement", fontsize=14)
    ax.legend(loc='upper right')
    
    return fig

def draw_z_beam(level_diff):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # กำหนดพิกัดของคานหักมุม (Stepped Beam)
    x = [0, 300, 300, 600, 600, 260, 260, 0]
    y = [150+level_diff, 150+level_diff, 150, 150, 50, 50, 50+level_diff, 50+level_diff]
    
    # วาดคอนกรีต
    poly = patches.Polygon(xy=list(zip(x, y)), closed=True, edgecolor='black', facecolor='#e0e0e0', linewidth=2)
    ax.add_patch(poly)
    
    # เหล็กเสริมหลัก (Main Rebar)
    # เหล็กบน
    ax.plot([20, 280], [130+level_diff, 130+level_diff], color='green', linewidth=3, label='Main Rebar')
    ax.plot([280, 280], [130+level_diff, 70], color='green', linewidth=3) # ล้วงลงมาในคานล่าง
    ax.plot([320, 580], [130, 130], color='green', linewidth=3)
    
    # เหล็กล่าง
    ax.plot([20, 280], [70+level_diff, 70+level_diff], color='green', linewidth=3)
    ax.plot([320, 580], [70, 70], color='green', linewidth=3)
    ax.plot([320, 320], [70, 130+level_diff], color='green', linewidth=3) # ล้วงขึ้นไปในคานบน
    
    # *** ไฮไลท์สำคัญ: เหล็กเสริมทแยงมุม (Diagonal Rebar) กันร้าวที่มุม Re-entrant ***
    ax.plot([230, 330], [80+level_diff, 20+level_diff], color='red', linewidth=3, label='Diagonal Crack Control (กันร้าวมุม)')
    ax.plot([250, 350], [90+level_diff, 30+level_diff], color='red', linewidth=3)
    
    # แสดงจุดที่มักเกิดรอยร้าว (Stress Concentration)
    circle = patches.Circle((300, 50+level_diff), radius=20, color='red', alpha=0.3, label='Stress Concentration Zone')
    ax.add_patch(circle)

    ax.set_xlim(-50, 650)
    ax.set_ylim(0, 200 + level_diff + 50)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Z-Shaped Beam (คานหักมุม): Re-entrant Corner Detailing", fontsize=14)
    ax.legend(loc='upper right')
    
    return fig

# --- Streamlit UI ---
st.set_page_config(page_title="Beam Detailing Viewer", layout="wide")

st.title("🏗️ Beam Reinforcement & Stress Visualization")
st.markdown("โปรแกรมจำลองการจัดเหล็กเสริมและการกระจายแรงในคานต่างระดับ")

# แบ่งหน้าจอเป็น 2 ฝั่ง (Controls และ Visualization)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ ตั้งค่าคาน (Parameters)")
    beam_type = st.radio(
        "เลือกประเภทโครงสร้าง:",
        ("คานเพิ่มความลึก (Deep Beam)", "คานหักมุม (Z-Shaped Beam)")
    )
    
    level_diff = st.slider(
        "ระดับความต่างของพื้น (cm):", 
        min_value=20, 
        max_value=150, 
        value=50, 
        step=10,
        help="ปรับเพื่อดูการเปลี่ยนแปลงของรูปทรงคานและการจัดเหล็ก"
    )
    
    st.markdown("---")
    st.subheader("💡 ข้อควรรู้ทางวิศวกรรม")
    if beam_type == "คานเพิ่มความลึก (Deep Beam)":
        st.info("**Deep Beam:** เมื่อคานมีความลึกมาก พฤติกรรมการรับแรงจะเปลี่ยนจาก Bending เป็นแบบ **Strut-and-Tie** สิ่งสำคัญคือต้องมี **เหล็กเสริมด้านข้าง (Skin Reinforcement)** เพื่อป้องกันการแตกร้าวจากอุณหภูมิและการหดตัว")
    else:
        st.warning("**Z-Shaped Beam:** จุดอ่อนที่สุดคือ **มุมหักด้านใน (Re-entrant Corner)** ซึ่งจะเกิดหน่วยแรงดึงสูงมาก จำเป็นต้องเสริม **เหล็กทแยงมุม (Diagonal Bars)** และล้วงเหล็กหลักให้ลึกพอ ไม่เช่นนั้นคานจะร้าวฉีกที่มุมนี้แน่นอน")

with col2:
    st.subheader("📊 ภาพจำลองโครงสร้าง")
    if beam_type == "คานเพิ่มความลึก (Deep Beam)":
        fig = draw_deep_beam(level_diff)
    else:
        fig = draw_z_beam(level_diff)
        
    st.pyplot(fig)
