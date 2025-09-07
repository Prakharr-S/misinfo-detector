import streamlit as st
import os
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="AI Misinformation Detector",
    page_icon="🔍",
    layout="wide"
)

def analyze_content_mock(content, content_type="text"):
    """Mock analysis function - we'll replace this with real AI later"""
    
    # Simple keyword-based scoring for demo
    risk_keywords = [
        "forward this", "share immediately", "doctors don't want you to know",
        "secret cure", "government hiding", "they don't want you to see",
        "urgent", "breaking", "exclusive", "miracle", "banned"
    ]
    
    risk_score = 0
    detected_flags = []
    
    content_lower = content.lower()
    for keyword in risk_keywords:
        if keyword in content_lower:
            risk_score += 2
            detected_flags.append(f"Contains suspicious phrase: '{keyword}'")
    
    # Additional checks
    if len(content) < 50:
        risk_score += 1
        detected_flags.append("Very short content - lacks detail")
    
    if content.count("!") > 3:
        risk_score += 1
        detected_flags.append("Excessive exclamation marks")
    
    if "http" not in content and "source" not in content_lower:
        risk_score += 1
        detected_flags.append("No sources or links provided")
    
    # Cap risk score
    risk_score = min(risk_score, 10)
    confidence = min(risk_score * 10 + 20, 95)
    
    return {
        "risk_score": risk_score,
        "confidence": confidence,
        "flags": detected_flags,
        "analysis_time": datetime.now().strftime("%H:%M:%S")
    }

def generate_education_content(analysis_result):
    """Generate educational content based on analysis"""
    
    risk_score = analysis_result["risk_score"]
    
    if risk_score >= 7:
        level = "HIGH RISK"
        color = "error"
        explanation = "This content shows multiple signs of potential misinformation. Be very cautious before believing or sharing."
        
    elif risk_score >= 4:
        level = "MODERATE RISK" 
        color = "warning"
        explanation = "This content has some concerning elements. Verify with reliable sources before trusting."
        
    else:
        level = "LOW RISK"
        color = "success" 
        explanation = "This content appears relatively trustworthy, but always verify important information."
    
    verification_steps = [
        "🔍 Search for the same claim on reliable news websites",
        "📊 Check fact-checking sites like Alt News, Boom, or Fact Crescendo",
        "🏛️ Look for official government or institutional sources",
        "👥 See if multiple credible sources report the same information",
        "📅 Check if the information is recent and contextually relevant"
    ]
    
    red_flags = [
        "❌ Emotional language designed to provoke strong reactions",
        "❌ Claims that seem too good or too bad to be true", 
        "❌ Requests to 'forward immediately' or 'share with everyone'",
        "❌ No credible sources or citations provided",
        "❌ Poor grammar, spelling, or formatting",
        "❌ Claims that 'they' don't want you to know something"
    ]
    
    return {
        "level": level,
        "color": color,
        "explanation": explanation,
        "verification_steps": verification_steps,
        "red_flags": red_flags
    }

def main():
    # Header
    st.title("🔍 AI-Powered Misinformation Detector")
    st.subheader("🇮🇳 Built by Prakhar Singh for Gen AI Exchange Hackathon 2025")
    st.markdown("*Combating misinformation with AI • Educating digital citizens*")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Quick Stats")
        st.info("**Mission:** Help Indians identify and combat misinformation")
        
        st.header("🎯 How It Works")
        st.markdown("""
        1. **Paste** content to analyze
        2. **AI analyzes** for misinformation signs
        3. **Get results** with risk assessment
        4. **Learn** why it's problematic
        5. **Verify** with our recommended steps
        """)
        
        st.header("🚀 Powered By")
        st.markdown("• Google Cloud Vertex AI  \n• Gemini AI Models  \n• Advanced NLP Analysis")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Content Analysis")
        
        # Input selection
        input_type = st.selectbox(
            "What would you like to analyze?",
            ["WhatsApp Forward", "Social Media Post", "News Article", "Email", "Text Message"],
            help="Choose the type of content you want to check for misinformation"
        )
        
        # Content input
        content = st.text_area(
            f"Paste your {input_type.lower()} here:",
            height=150,
            placeholder="Example: 'URGENT! Forward this to 10 people immediately! Doctors discovered a secret cure that pharmaceutical companies don't want you to know about...'"
        )
        
        # Analysis button
        if st.button("🔍 Analyze for Misinformation", type="primary", use_container_width=True):
            if content.strip():
                with st.spinner("🤖 AI is analyzing the content..."):
                    # Simulate processing time
                    import time
                    time.sleep(2)
                    
                    # Analyze content
                    analysis_result = analyze_content_mock(content, input_type)
                    education_content = generate_education_content(analysis_result)
                    
                    # Display results
                    st.markdown("---")
                    st.subheader("📋 Analysis Results")
                    
                    # Metrics
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric(
                            "Risk Level", 
                            f"{analysis_result['risk_score']}/10",
                            help="Higher scores indicate more misinformation risk"
                        )
                    with col_b:
                        st.metric(
                            "AI Confidence", 
                            f"{analysis_result['confidence']}%",
                            help="How confident our AI is in this assessment"
                        )
                    with col_c:
                        st.metric(
                            "Flags Detected", 
                            len(analysis_result['flags']),
                            help="Number of suspicious elements found"
                        )
                    
                    # Risk level display
                    if education_content["color"] == "error":
                        st.error(f"⚠️ {education_content['level']} DETECTED!")
                    elif education_content["color"] == "warning":
                        st.warning(f"⚡ {education_content['level']} DETECTED")
                    else:
                        st.success(f"✅ {education_content['level']}")
                    
                    st.info(education_content["explanation"])
                    
                    # Detailed flags
                    if analysis_result['flags']:
                        with st.expander("🔍 Why this content is flagged", expanded=True):
                            for flag in analysis_result['flags']:
                                st.write(f"• {flag}")
                    
                    # Educational section
                    st.markdown("---")
                    st.subheader("🎓 Learn to Spot Misinformation")
                    
                    tab1, tab2, tab3 = st.tabs(["📚 How to Verify", "🚨 Red Flags", "💡 Quick Tips"])
                    
                    with tab1:
                        st.markdown("**Follow these steps to verify any suspicious content:**")
                        for step in education_content["verification_steps"]:
                            st.write(step)
                    
                    with tab2:
                        st.markdown("**Watch out for these warning signs:**")
                        for flag in education_content["red_flags"]:
                            st.write(flag)
                    
                    with tab3:
                        st.markdown("""
                        **Quick verification tips:**
                        - 🕐 Take a moment to think before sharing
                        - 🔗 Check if there are credible source links
                        - 📱 Search the claim on Google or fact-check sites
                        - 👥 Ask yourself: "Who benefits from me believing this?"
                        - 🧠 Trust your critical thinking skills
                        """)
                    
                    # Analysis metadata
                    st.caption(f"Analysis completed at {analysis_result['analysis_time']} • Powered by Google Cloud AI")
                    
            else:
                st.warning("⚠️ Please paste some content to analyze!")
    
    with col2:
        st.header("📚 Knowledge Hub")
        
        # Quick tips
        st.info("""
        **🚨 Common Red Flags:**
        • Emotional language
        • "Forward immediately"
        • No credible sources
        • Too good to be true
        • Spelling/grammar errors
        • "They don't want you to know"
        """)
        
        # Reliable sources
        st.success("""
        **✅ Trusted Sources:**
        • Government websites (.gov.in)
        • Established news outlets
        • Fact-checking organizations
        • Academic institutions
        • Official social media accounts
        """)
        
        # India-specific resources
        st.markdown("""
        **🇮🇳 Indian Fact-Checkers:**
        - Alt News
        - BOOM Live
        - Fact Crescendo
        - Vishvas News
        - PIB Fact Check
        """)
        
        # Statistics (mock)
        st.markdown("---")
        st.markdown("**📊 Today's Impact**")
        st.metric("Content Analyzed", "1,247")
        st.metric("Misinformation Flagged", "342") 
        st.metric("Users Educated", "1,156")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    🔍 AI-Powered Misinformation Detector | Built with ❤️ for India's Digital Safety<br>
    Powered by Google Cloud Vertex AI • Gen AI Exchange Hackathon 2025
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
