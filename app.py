import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_deep_beam(level_diff, beam_length=600):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # กำหนดขนาดคานพื้นฐาน
    beam_depth = 100 + level_diff  
    
    # วาดคอนกรีต
    rect = patches.Rectangle((0, 0), beam_length, beam_depth, linewidth=2, edgecolor='#333333', facecolor='#e2e8f0')
    ax.add_patch(rect)
    
    # จำลองการกระจายแรง (Strut and Tie Model)
    # Compression Struts (สีน้ำเงิน)
    ax.plot([50, beam_length/2], [beam_depth, 50], color='#2563eb', linestyle='--', linewidth=3, alpha=0.7, label='Compression Strut (แรงอัด)')
    ax.plot([beam_length-50, beam_length/2], [beam_depth, 50], color='#2563eb', linestyle='--', linewidth=3, alpha=0.7)
    
    # Tension Tie (สีแดง - เหล็กเสริมรับแรงดึงหลัก)
    ax.plot([50, beam_length-50], [50, 50], color='#dc2626', linewidth=4, label='Main Tension Rebar (เหล็กนอน)')
    
    # เหล็กเสริมกันร้าว (Skin Reinforcement) ที่ต้องมีใน Deep Beam
    num_skin_bars = int(beam_depth / 30)
    for i in range(1, num_skin_bars):
        y_pos = i * 30
        if y_pos < beam_depth - 20:
            if i == 1: # ใส่ label แค่เส้นเดียวเพื่อไม่ให้รก Legend
                ax.plot([20, beam_length-20], [y_pos, y_pos], color='#16a34a', linewidth=1.5, linestyle='-.', label='Skin Reinforcement')
            else:
                ax.plot([20, beam_length-20], [y_pos, y_pos], color='#16a34a', linewidth=1.5, linestyle='-.')
            
    # เหล็กปลอก (Stirrups)
    for x in range(50, beam_length-40, 40):
        ax.plot([x, x], [20, beam_depth-20], color='#f59e0b', linewidth=1.5, alpha=0.8)
        
    ax.set_xlim(-50, beam_length + 50)
    ax.set_ylim(-50, beam_depth + 50)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Deep Beam: Strut-and-Tie Model & Skin Reinforcement", fontsize=14, fontweight='bold', pad=15)
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    
    fig.tight_layout()
    return fig, beam_length, beam_depth

def draw_z_beam(level_diff):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # กำหนดพิกัดของคานหักมุม (Stepped Beam)
    x = [0, 300, 300, 600, 600, 260, 260, 0]
    y = [150+level_diff, 150+level_diff, 150, 150, 50, 50, 50+level_diff, 50+level_diff]
    
    # วาดคอนกรีต
    poly = patches.Polygon(xy=list(zip(x, y)), closed=True, edgecolor='#333333', facecolor='#e2e8f0', linewidth=2)
    ax.add_patch(poly)
    
    # เหล็กเสริมหลัก (Main Rebar) - สีเขียว
    ax.plot([20, 280], [130+level_diff, 130+level_diff], color='#16a34a', linewidth=3, label='Main Rebar')
    ax.plot([280, 280], [130+level_diff, 70], color='#16a34a', linewidth=3) # ล้วงลงมาในคานล่าง
    ax.plot([320, 580], [130, 130], color='#16a34a', linewidth=3)
    
    # เหล็กล่าง
    ax.plot([20, 280], [70+level_diff, 70+level_diff], color='#16a34a', linewidth=3)
    ax.plot([320, 580], [70, 70], color='#16a34a', linewidth=3)
    ax.plot([320, 320], [70, 130+level_diff], color='#16a34a', linewidth=3) # ล้วงขึ้นไปในคานบน
    
    # *** ไฮไลท์สำคัญ: เหล็กเสริมทแยงมุม (Diagonal Rebar) กันร้าวที่มุม Re-entrant ***
    # คำนวณพิกัดให้สัมพันธ์กับ level_diff
    corner_y = 150
    ax.plot([240, 340], [corner_y + 40, corner_y - 60], color='#dc2626', linewidth=3, label='Diagonal Crack Control')
    ax.plot([260, 360], [corner_y + 50, corner_y - 50], color='#dc2626', linewidth=3)
    
    # แสดงจุดที่มักเกิดรอยร้าว (Stress Concentration)
    circle = patches.Circle((300, 150), radius=25, color='#ef4444', alpha=0.4, label='Stress Concentration Zone')
    ax.add_patch(circle)

    ax.set_xlim(-50, 650)
    ax.set_ylim(0, 200 + level_diff + 50)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Z-Shaped Beam: Re-entrant Corner Detailing", fontsize=14, fontweight='bold', pad=15)
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    
    fig.tight_layout()
    return fig

# --- Streamlit UI ---
st.set_page_config(page_title="Beam Detailing Viewer", page_icon="🏗️", layout="wide")

st.title("🏗️ Beam Reinforcement & Stress Visualization")
st.markdown("โปรแกรมจำลองการจัดเหล็กเสริมและการกระจายแรงในคานหน้าตัดพิเศษ")
st.markdown("---")

# ย้ายส่วนควบคุมไปไว้ที่ Sidebar
with st.sidebar:
    st.header("⚙️ ตั้งค่าพารามิเตอร์")
    beam_type = st.radio(
        "เลือกประเภทโครงสร้าง:",
        ("คานเพิ่มความลึก (Deep Beam)", "คานหักมุม (Z-Shaped Beam)")
    )
    
    st.markdown("---")
    level_diff = st.slider(
        "ระดับความต่างของพื้น / ความลึก (cm):", 
        min_value=20, 
        max_value=200, 
        value=80, 
        step=10,
        help="ปรับเพื่อดูการเปลี่ยนแปลงของรูปทรงคานและการจัดเหล็ก"
    )
    
    st.markdown("---")
    st.subheader("💡 ข้อควรรู้ทางวิศวกรรม")
    if beam_type == "คานเพิ่มความลึก (Deep Beam)":
        st.info("**Deep Beam:** เมื่อคานมีความลึกมาก พฤติกรรมการรับแรงจะเปลี่ยนจาก Bending เป็นแบบ **Strut-and-Tie** สิ่งสำคัญคือต้องมี **เหล็กเสริมด้านข้าง (Skin Reinforcement)** เพื่อป้องกันการแตกร้าวจากอุณหภูมิและการหดตัว")
    else:
        st.warning("**Z-Shaped Beam:** จุดอ่อนที่สุดคือ **มุมหักด้านใน (Re-entrant Corner)** ซึ่งจะเกิดหน่วยแรงดึงสูงมาก จำเป็นต้องเสริม **เหล็กทแยงมุม (Diagonal Bars)** และล้วงเหล็กหลักให้ลึกพอ ไม่เช่นนั้นคานจะร้าวฉีกที่มุมนี้แน่นอน")

# พื้นที่แสดงผลหลัก
col_main, col_metrics = st.columns([3, 1])

with col_main:
    st.subheader("📊 ภาพจำลองโครงสร้าง")
    if beam_type == "คานเพิ่มความลึก (Deep Beam)":
        fig, length, depth = draw_deep_beam(level_diff)
        st.pyplot(fig)
    else:
        fig = draw_z_beam(level_diff)
        st.pyplot(fig)

with col_metrics:
    st.subheader("📐 ข้อมูลทางเรขาคณิต")
    if beam_type == "คานเพิ่มความลึก (Deep Beam)":
        span_depth_ratio = length / depth
        st.metric(label="ความยาวคาน (Span)", value=f"{length} cm")
        st.metric(label="ความลึกคาน (Depth)", value=f"{depth} cm")
        st.metric(label="Span/Depth Ratio", value=f"{span_depth_ratio:.2f}")
        
        if span_depth_ratio <= 4:
            st.success("✅ พฤติกรรมเป็น Deep Beam (Ratio $\le$ 4)")
        else:
            st.error("⚠️ พฤติกรรมเป็นคานปกติ (Ordinary Beam)")
    else:
        st.metric(label="ระยะหักมุมแนวตั้ง", value=f"{level_diff} cm")
        st.metric(label="จุดวิกฤต (Critical Zone)", value="1 จุด")
        st.markdown("*แนะนำให้หลีกเลี่ยงการใช้คานรูปแบบนี้หากโครงสร้างต้องรับแรงสั่นสะเทือนหรือแผ่นดินไหว*")
