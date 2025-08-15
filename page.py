import streamlit as st
import pandas as pd
import json
from datetime import datetime
import base64
from PIL import Image
import io

# Configure the page
st.set_page_config(
    page_title="PyVision Studio - Products",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for PyVision Studio branding
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a202c 100%);
    }

    /* Header styling with logo */
    .main-header {
        background: linear-gradient(90deg, #2d3748, #4a5568);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #4a5568;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .logo-container {
        flex-shrink: 0;
    }

    .logo-container img {
        width: 80px;
        height: 80px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .header-content h1 {
        color: #00d9ff;
        font-family: 'Monaco', 'Menlo', monospace;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
        margin: 0;
        font-size: 2.8rem;
    }

    .header-content p {
        color: #a0aec0;
        font-family: 'Monaco', 'Menlo', monospace;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }

    /* Product card styling */
    .product-card {
        background: linear-gradient(145deg, #2d3748, #1a202c);
        border: 1px solid #4a5568;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }

    .product-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(0,217,255,0.25);
        border-color: #00d9ff;
    }

    .product-title {
        color: #00d9ff;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-family: 'Monaco', 'Menlo', monospace;
    }

    .product-technology {
        background: linear-gradient(90deg, #f39c12, #e67e22);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 1rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }

    .product-platform {
        background: linear-gradient(90deg, #9b59b6, #8e44ad);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 1rem;
        font-weight: bold;
    }

    .product-description {
        color: #cbd5e0;
        line-height: 1.8;
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
    }

    .product-status {
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin-right: 1rem;
    }

    .status-available {
        background: #27ae60;
        color: white;
    }

    .status-beta {
        background: #f39c12;
        color: white;
    }

    .status-development {
        background: #e74c3c;
        color: white;
    }

    /* Feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }

    .feature-item {
        background: rgba(0, 217, 255, 0.1);
        border: 1px solid rgba(0, 217, 255, 0.3);
        border-radius: 8px;
        padding: 1rem;
        color: #e2e8f0;
    }

    .feature-item strong {
        color: #00d9ff;
    }

    /* Purchase section */
    .purchase-section {
        background: linear-gradient(90deg, #e74c3c, #c0392b);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: white;
        text-align: center;
    }

    .purchase-button {
        background: white;
        color: #e74c3c;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
        font-size: 1.1rem;
    }

    .purchase-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }

    .download-section {
        background: linear-gradient(90deg, #27ae60, #2ecc71);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: white;
        text-align: center;
    }

    .download-button {
        background: white;
        color: #27ae60;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }

    .download-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    /* Media gallery */
    .media-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }

    .media-item {
        border: 2px solid #4a5568;
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s ease;
        background: #2d3748;
    }

    .media-item:hover {
        border-color: #00d9ff;
        box-shadow: 0 8px 25px rgba(0,217,255,0.3);
    }

    .media-item img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }

    .media-placeholder {
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #a0aec0;
        font-size: 1.2rem;
        background: #1a202c;
    }

    /* Social video container */
    .social-video-container {
        border: 2px solid #4a5568;
        border-radius: 15px;
        padding: 1.5rem;
        background: #1a202c;
        margin: 1.5rem 0;
        text-align: center;
    }

    .social-platform {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem;
    }

    .linkedin-badge {
        background: #0077b5;
        color: white;
    }

    .facebook-badge {
        background: #1877f2;
        color: white;
    }

    .youtube-badge {
        background: #ff0000;
        color: white;
    }

    /* System requirements */
    .requirements-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    .requirement-item {
        background: #2d3748;
        border: 1px solid #4a5568;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }

    .requirement-item strong {
        color: #00d9ff;
        display: block;
        margin-bottom: 0.5rem;
    }

    /* Upload section styling */
    .upload-section {
        background: rgba(45, 55, 72, 0.5);
        border: 2px dashed #4a5568;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
    }

    /* Sidebar styling */
    .sidebar .element-container {
        background: rgba(45, 55, 72, 0.7);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #4a5568;
    }

    /* Metrics styling */
    .metric-card {
        background: linear-gradient(145deg, #2d3748, #1a202c);
        border: 1px solid #4a5568;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        color: #00d9ff;
        font-family: 'Monaco', 'Menlo', monospace;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    /* Form styling */
    .stTextInput, .stTextArea, .stSelectbox {
        background: #2d3748 !important;
        border: 1px solid #4a5568 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #00d9ff, #0099cc);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
        padding: 0.7rem 1.5rem;
    }

    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(0, 217, 255, 0.6);
        transform: translateY(-3px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for PyVision Studio products
if 'products' not in st.session_state:
    st.session_state.products = [
        {
            "id": 1,
            "name": "Document Analysis and Organizer",
            "technology": "Tkinter",
            "platform": "Desktop",
            "description": "A lightweight, no-setup desktop app that securely extracts and processes text from documents with a clean, minimalist interface.",
            "status": "Available",
            "version": "2.1.0",
            "price": 29.99,
            "created_date": "2024-01-15",
            "features": [
                "Real-time Image Processing",
                "Advanced OCR",
                "Batch Processing Support",
                "Export to Multiple Formats",
                "User-friendly Tkinter Interface",
                "OpenAi API",


            ],
            "system_requirements": {
                "OS": "Windows 7/10/11",
                "Python": "3.8 or higher",
                "RAM": "4GB minimum, 8GB recommended",
                "Storage": "500MB free space",

            },
            "purchase_links": {
                "Gumroad": "https://freelanceibrahim.gumroad.com/l/uisef"

            },
            "demo_videos": {
                "LinkedIn": "https://www.linkedin.com/feed/update/urn:li:activity:7361790447947599873?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEXwExYBpJkYnn9C3CGeh_jGEeIHkPz2LyM",
                "Facebook": "https://www.facebook.com/61573393474390/videos/1520702859296383/",

            },
            "documentation": "https://docs.pyvisionstudio.com/desktop-pro",
            "uploaded_images": [],
            "uploaded_videos": []
        },
        {
            "id": 2,
            "name": "Fast Ledger Tallying Tool",
            "technology": "PyQt",
            "platform": "Desktop",
            "description": "AI-Powered Ledger Matcher: Automate financial reconciliation with smart, customizable matching for seamless accounting workflows.",
            "status": "Beta",
            "version": "1.5.0-beta",
            "price": 29.99,
            "created_date": "2024-02-20",
            "features": [
                "Advanced Data Analytics",
                "PyQT Integration",
                "Interactive Visualizations",
                "Custom Dashboard Creation",
                "Professional PyQt Interface",
                "Multi-format Data Import",
                "Statistical Analysis Tools",
                "Export to Excel"
            ],
            "system_requirements": {
                "OS": "Windows 7/10/11",
                "Python": "3.9 or higher",
                "RAM": "4GB minimum, 6GB recommended",
                "Storage": "500MB free space",

            },
            "purchase_links": {
                "Gumroad": "https://gumroad.com/l/pyvision-analytics-suite",
                "Itch.io": "https://pyvisionstudio.itch.io/analytics-suite"
            },
            "demo_videos": {
                "LinkedIn": "https://www.linkedin.com/posts/your-profile_analytics-demo",
                "Facebook": "https://www.facebook.com/watch/?v=your-analytics-video",
                "YouTube": "https://www.youtube.com/watch?v=your-analytics-video"
            },
            "documentation": "https://docs.pyvisionstudio.com/analytics-suite",
            "uploaded_images": [],
            "uploaded_videos": []
        }
    ]


def render_header():
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #1e3a8a, #3b82f6); 
                        border-radius: 10px; display: flex; align-items: center; justify-content: center; 
                        font-size: 2rem; color: white;">👁️</div>
        </div>
        <div class="header-content">
            <h1>PyVision Studio</h1>
            <p>Professional Python Vision & Analytics Solutions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_social_videos(demo_videos):
    st.markdown("## 🎥 Demo Videos")

    video_html = '<div class="social-video-container">'
    video_html += '<h3 style="margin-top: 0;">Watch Our Product Demos</h3>'

    for platform, link in demo_videos.items():
        if link and link != "#":
            platform_class = platform.lower() + "-badge"
            video_html += f'''
            <div style="margin: 1rem 0;">
                <span class="social-platform {platform_class}">{platform}</span><br>
                <a href="{link}" target="_blank" style="color: #00d9ff; text-decoration: none;">
                    🎬 Watch on {platform}
                </a>
            </div>
            '''

    video_html += '</div>'
    st.markdown(video_html, unsafe_allow_html=True)


def render_uploaded_media(product):
    st.markdown("## 📸 Product Media")

    # Show uploaded images
    if product.get('uploaded_images'):
        st.markdown("### Product Screenshots")
        cols = st.columns(3)
        for i, img_data in enumerate(product['uploaded_images']):
            with cols[i % 3]:
                img = Image.open(io.BytesIO(img_data))
                st.image(img, use_container_width=True, caption=f"Screenshot {i + 1}")

    # Show uploaded videos
    if product.get('uploaded_videos'):
        st.markdown("### Product Videos")
        for i, video_data in enumerate(product['uploaded_videos']):
            st.video(video_data, format='video/mp4')

    # Show placeholders if no media
    if not product.get('uploaded_images') and not product.get('uploaded_videos'):
        st.markdown("""
        <div class="media-gallery">
            <div class="media-item">
                <div class="media-placeholder">📷 Product Screenshots<br><small>Upload images in the Add Product section</small></div>
            </div>
            <div class="media-item">
                <div class="media-placeholder">🎬 Demo Videos<br><small>Upload videos or use social media links</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_product_showcase(product):
    price_text = f"${product.get('price', 0):.2f}" if product.get('price') else "Free"

    st.markdown(f"""
    <div class="product-card">
        <div class="product-title">{product['name']}</div>
        <span class="product-technology">{product['technology']}</span>
        <span class="product-platform">{product['platform']}</span>
        <div class="product-description">{product['description']}</div>
        <div>
            <span class="product-status status-{product['status'].lower()}">{product['status']}</span>
            <strong style="color: #48bb78; margin-left: 1rem;">💰 {price_text}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_product_details(product):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"# 🚀 {product['name']}")
        st.markdown(
            f"**Technology:** {product['technology']} • **Platform:** {product['platform']} • **Version:** {product['version']}")

        # Status and price
        status_class = f"status-{product['status'].lower()}"
        price_text = f"${product.get('price', 0):.2f}" if product.get('price') else "Free"
        st.markdown(
            f'<span class="product-status {status_class}">{product["status"]}</span> <strong style="color: #48bb78;">💰 {price_text}</strong>',
            unsafe_allow_html=True)

        st.markdown("---")

        # Description
        st.markdown("## 📋 Overview")
        st.write(product['description'])

        # Social media videos
        if product.get('demo_videos'):
            render_social_videos(product['demo_videos'])

        # Uploaded media
        render_uploaded_media(product)

        # Key Features
        st.markdown("## ⭐ Key Features")
        features_html = '<div class="feature-grid">'
        for feature in product['features']:
            features_html += f'<div class="feature-item"><strong>✓</strong> {feature}</div>'
        features_html += '</div>'
        st.markdown(features_html, unsafe_allow_html=True)

    with col2:
        # Purchase Section
        if product.get('purchase_links'):
            st.markdown("## 💳 Purchase")
            purchase_html = f"""
            <div class="purchase-section">
                <h3 style="margin-top: 0;">Get {product['name']}</h3>
                <p>Version {product['version']} • {f"${product.get('price', 0):.2f}" if product.get('price') else "Free"}</p>
            """

            for platform, link in product['purchase_links'].items():
                if link and link != "#":
                    purchase_html += f'<a href="{link}" target="_blank" class="purchase-button">🛒 Buy on {platform}</a>'

            purchase_html += '</div>'
            st.markdown(purchase_html, unsafe_allow_html=True)

        # Free download section (if no purchase links)
        if not product.get('purchase_links') or not any(product['purchase_links'].values()):
            st.markdown("## ⬇️ Download")
            st.markdown(f"""
            <div class="download-section">
                <h3 style="margin-top: 0;">Download {product['name']}</h3>
                <p>Version {product['version']} • Free</p>
                <a href="#" class="download-button">📦 Download Now</a>
            </div>
            """, unsafe_allow_html=True)

        # Documentation
        if product.get('documentation'):
            st.markdown(
                f'<div class="download-section"><a href="{product["documentation"]}" target="_blank" class="download-button">📚 Documentation</a></div>',
                unsafe_allow_html=True)

        # System Requirements
        st.markdown("## 💻 System Requirements")
        req_html = '<div class="requirements-grid">'
        for req, value in product['system_requirements'].items():
            req_html += f'<div class="requirement-item"><strong>{req}</strong>{value}</div>'
        req_html += '</div>'
        st.markdown(req_html, unsafe_allow_html=True)

        # Additional Info
        st.markdown("### 📊 Product Info")
        st.markdown(f"**Release Date:** {product['created_date']}")
        st.markdown(f"**Product ID:** PVS-{product['id']:03d}")
        st.markdown(f"**Category:** {product['technology']} Application")


def add_product_form():
    st.markdown("### ➕ Add New PyVision Product")

    with st.form("add_product_form"):
        # Basic Info
        st.markdown("#### 📝 Basic Information")
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Product Name*")
            technology = st.selectbox("Technology Stack",
                                      ["Tkinter", "PyQt", "PyQt6", "Kivy", "Flask", "Django", "FastAPI"])
            platform = st.selectbox("Platform", ["Desktop", "Web", "Mobile", "CLI"])
            status = st.selectbox("Status", ["Available", "Beta", "Development", "Discontinued"])

        with col2:
            version = st.text_input("Version (e.g., 1.0.0)")
            price = st.number_input("Price ($)", min_value=0.0, step=0.01, help="Set to 0 for free products")
            description = st.text_area("Description*", height=100)

        # Features
        st.markdown("#### ⭐ Features")
        features = st.text_area("Features (one per line)")

        # Media Upload Section
        st.markdown("#### 📸 Media Upload")
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)

        media_col1, media_col2 = st.columns(2)

        with media_col1:
            st.markdown("**📷 Product Images**")
            uploaded_images = st.file_uploader(
                "Upload Screenshots/Images",
                type=['png', 'jpg', 'jpeg'],
                accept_multiple_files=True,
                help="Upload screenshots of your product interface"
            )

        with media_col2:
            st.markdown("**🎬 Product Videos**")
            uploaded_videos = st.file_uploader(
                "Upload Demo Videos",
                type=['mp4', 'avi', 'mov'],
                accept_multiple_files=True,
                help="Upload demo videos of your product"
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # Social Media Links
        st.markdown("#### 🌐 Social Media Demo Links")
        social_col1, social_col2, social_col3 = st.columns(3)

        with social_col1:
            linkedin_video = st.text_input("LinkedIn Video Link")
        with social_col2:
            facebook_video = st.text_input("Facebook Video Link")
        with social_col3:
            youtube_video = st.text_input("YouTube Video Link")

        # Purchase Links
        st.markdown("#### 💳 Purchase/Download Links")
        purchase_col1, purchase_col2 = st.columns(2)

        with purchase_col1:
            gumroad_link = st.text_input("Gumroad Link")
            itch_link = st.text_input("Itch.io Link")

        with purchase_col2:
            documentation_link = st.text_input("Documentation URL")
            github_link = st.text_input("GitHub/Source Link")

        # System Requirements
        st.markdown("#### 💻 System Requirements")
        req_cols = st.columns(2)
        with req_cols[0]:
            req_keys = st.text_area("Requirement Types",
                                    value="OS\nPython\nRAM\nStorage\nDependencies")
        with req_cols[1]:
            req_values = st.text_area("Requirement Values",
                                      value="Windows 10/11, macOS, Linux\n3.8+\n4GB\n500MB\nOpenCV, NumPy")

        submitted = st.form_submit_button("🚀 Add PyVision Product", use_container_width=True)

        if submitted and name and description:
            # Process uploaded images
            processed_images = []
            if uploaded_images:
                for img_file in uploaded_images:
                    processed_images.append(img_file.read())

            # Process uploaded videos
            processed_videos = []
            if uploaded_videos:
                for video_file in uploaded_videos:
                    processed_videos.append(video_file.read())

            # Process requirements
            reqs = {}
            if req_keys and req_values:
                keys = [k.strip() for k in req_keys.split('\n') if k.strip()]
                values = [v.strip() for v in req_values.split('\n') if v.strip()]
                reqs = dict(zip(keys, values))

            # Process features
            feature_list = [f.strip() for f in features.split('\n') if f.strip()] if features else []

            # Process purchase links
            purchase_links = {}
            if gumroad_link: purchase_links["Gumroad"] = gumroad_link
            if itch_link: purchase_links["Itch.io"] = itch_link
            if github_link: purchase_links["GitHub"] = github_link

            # Process social media links
            demo_videos = {}
            if linkedin_video: demo_videos["LinkedIn"] = linkedin_video
            if facebook_video: demo_videos["Facebook"] = facebook_video
            if youtube_video: demo_videos["YouTube"] = youtube_video

            new_product = {
                "id": max([p['id'] for p in st.session_state.products], default=0) + 1,
                "name": name,
                "technology": technology,
                "platform": platform,
                "description": description,
                "status": status,
                "version": version or "1.0.0",
                "price": price,
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "features": feature_list,
                "system_requirements": reqs,
                "purchase_links": purchase_links,
                "demo_videos": demo_videos,
                "documentation": documentation_link or "#",
                "uploaded_images": processed_images,
                "uploaded_videos": processed_videos
            }

            st.session_state.products.append(new_product)
            st.success(f"✅ Product '{name}' added to PyVision Studio catalog!")
            st.rerun()


# Main app
def main():
    render_header()

    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ PyVision Control Panel")

        page = st.radio("Navigate", ["🏠 Showcase", "📦 Products", "➕ Add Product", "📊 Analytics", "ℹ️ About"])

        st.markdown("---")
        st.markdown("### 🔧 Filters")

        # Technology filter
        technologies = ["All"] + list(set(p['technology'] for p in st.session_state.products))
        tech_filter = st.selectbox("Technology", technologies)

        # Status filter
        statuses = ["All"] + list(set(p['status'] for p in st.session_state.products))
        status_filter = st.selectbox("Status", statuses)

        # Search
        search_term = st.text_input("🔎 Search Products")

        st.markdown("---")
        st.markdown("### 🌐 PyVision Studio")
        st.markdown("**Founded:** 2023")
        st.markdown("**Focus:** Computer Vision & Analytics")
        st.markdown("**Technologies:** Python, OpenCV, Qt")

    # Apply filters
    filtered_products = st.session_state.products

    if tech_filter != "All":
        filtered_products = [p for p in filtered_products if p['technology'] == tech_filter]

    if status_filter != "All":
        filtered_products = [p for p in filtered_products if p['status'] == status_filter]

    if search_term:
        filtered_products = [p for p in filtered_products
                             if search_term.lower() in p['name'].lower()
                             or search_term.lower() in p['description'].lower()]

    # Main content
    if page == "🏠 Showcase":
        st.markdown("## 🚀 PyVision Studio Product Showcase")
        st.markdown("*Professional Python applications for computer vision and data analytics*")

        # Company metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Products", len(st.session_state.products))
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            active_count = len([p for p in st.session_state.products if p['status'] in ['Available', 'Beta']])
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Active Products", active_count)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            tech_count = len(set(p['technology'] for p in st.session_state.products))
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Technologies", tech_count)
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            total_revenue = sum(p.get('price', 0) for p in st.session_state.products)
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Portfolio Value", f"${total_revenue:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Featured products
        for product in st.session_state.products:
            render_product_showcase(product)

    elif page == "📦 Products":
        st.markdown("## 📦 PyVision Products Catalog")
        st.markdown(f"*Showing {len(filtered_products)} of {len(st.session_state.products)} products*")

        if not filtered_products:
            st.warning("No products match your current filters.")
        else:
            # Product selection
            product_names = [f"{p['name']} v{p['version']}" for p in filtered_products]
            selected_product_name = st.selectbox("Select Product for Detailed View", ["🏷️ Overview"] + product_names)

            if selected_product_name == "🏷️ Overview":
                # Show all products as cards
                for product in filtered_products:
                    render_product_showcase(product)
            else:
                # Show detailed product page
                selected_product = next(
                    p for p in filtered_products if f"{p['name']} v{p['version']}" == selected_product_name)
                render_product_details(selected_product)

    elif page == "➕ Add Product":
        add_product_form()

    elif page == "📊 Analytics":
        st.markdown("## 📊 PyVision Studio Analytics")

        # Technology distribution
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Technology Stack Distribution")
            tech_data = {}
            for product in st.session_state.products:
                tech = product['technology']
                tech_data[tech] = tech_data.get(tech, 0) + 1

            if tech_data:
                df_tech = pd.DataFrame(list(tech_data.items()), columns=['Technology', 'Count'])
                st.bar_chart(df_tech.set_index('Technology'))

        with col2:
            st.markdown("### Product Status Overview")
            status_data = {}
            for product in st.session_state.products:
                status = product['status']
                status_data[status] = status_data.get(status, 0) + 1

            if status_data:
                df_status = pd.DataFrame(list(status_data.items()), columns=['Status', 'Count'])
                st.bar_chart(df_status.set_index('Status'))

        # Revenue analysis
        st.markdown("### 💰 Revenue Analysis")
        if st.session_state.products:
            prices = [p.get('price', 0) for p in st.session_state.products]
            paid_products = [p for p in prices if p > 0]

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                avg_price = sum(paid_products) / len(paid_products) if paid_products else 0
                st.metric("Average Price", f"${avg_price:.2f}")
            with col2:
                max_price = max(prices) if prices else 0
                st.metric("Highest Price", f"${max_price:.2f}")
            with col3:
                free_count = len([p for p in prices if p == 0])
                st.metric("Free Products", free_count)
            with col4:
                paid_count = len(paid_products)
                st.metric("Paid Products", paid_count)

        # Platform analysis
        st.markdown("### 🖥️ Platform Distribution")
        if st.session_state.products:
            platform_data = {}
            for product in st.session_state.products:
                platform = product['platform']
                platform_data[platform] = platform_data.get(platform, 0) + 1

            if platform_data:
                df_platform = pd.DataFrame(list(platform_data.items()), columns=['Platform', 'Count'])
                st.bar_chart(df_platform.set_index('Platform'))

    elif page == "ℹ️ About":
        st.markdown("## ℹ️ About PyVision Studio")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            ### 👁️ Our Vision
            PyVision Studio specializes in creating professional-grade Python applications 
            for computer vision, data analytics, and desktop automation. We combine cutting-edge 
            technology with intuitive user interfaces to deliver powerful tools for researchers, 
            developers, and businesses.

            ### 🛠️ Our Technology Stack
            - **Desktop Applications**: Tkinter, PyQt, PyQt6
            - **Computer Vision**: OpenCV, PIL, NumPy
            - **Data Analytics**: Pandas, Matplotlib, Scikit-learn
            - **Deployment**: Cross-platform compatibility

            ### 🎯 Our Focus Areas
            - Real-time image processing and analysis
            - Advanced data visualization and analytics
            - User-friendly desktop applications
            - Cross-platform compatibility
            - Professional-grade software solutions

            ### 🌟 Why Choose PyVision Studio?
            - **Professional Quality**: Enterprise-grade applications
            - **User-Friendly**: Intuitive interfaces for all skill levels
            - **Regular Updates**: Continuous improvement and feature additions
            - **Great Support**: Comprehensive documentation and community support
            """)

        with col2:
            st.markdown("### 📞 Contact Information")
            st.markdown("""
            **Email**: ibrahim.aiagents1012@gmail.com   
            **LinkedIn**: www.linkedin.com/in/ibrahim-rehan-732b58288 
            **Facebook**: https://www.facebook.com/profile.php?id=61573393474390

            ### 🛒 Where to Buy Our Products
            - **Gumroad**: Primary marketplace
            - **Direct**: Through our website
            

            ### 📋 Quick Stats
            - **Founded**: 2023
            - **Products**: 2+ Desktop Applications
            - **Technologies**: Tkinter, PyQt
            - **Focus**: Computer Vision & Analytics
            - **Platforms**: Windows, macOS, Linux

            ### 🏆 Our Achievements
            - Cross-platform desktop applications
            - Professional UI/UX design
            - Advanced computer vision integration
            - Growing community of users
            - Positive customer feedback
            """)


if __name__ == "__main__":
    main()


    #         streamlit run page.py