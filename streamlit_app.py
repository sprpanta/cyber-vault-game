"""
Cyber Vault: Security+ Matching System
Deployment Ready - Optimized for Speed
Enterprise-Grade Training Platform
"""

import streamlit as st
import random

# Import your question bank
try:
    from data.questions import QUESTION_BANK
except ImportError:
    st.error("Unable to load Security Database. Please check data/questions.py")
    st.stop()

# ============================================
# PAGE CONFIGURATION (Must be first)
# ============================================
st.set_page_config(
    page_title="Cyber Vault - Security+ Training",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="auto"
)

# ============================================
# INITIALIZE SESSION STATE
# ============================================

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'game_active': False,
        'current_card_index': 0,
        'current_term_index': 0,
        'shuffled_indices': [],
        'matches': {},
        'selected_def': None,
        'feedback': None,
        'feedback_type': None,
        'show_results': False,
        'completed_cards': set(),
        'score': 0,
        'total_questions_answered': 0,
        'all_results': [],
        'selected_domain': None,
        'questions_list': [],
        'current_term': None,
        'current_term_idx': None,
        'current_definitions': [],
        'card_complete': False,
        'terms_answered': set(),
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================
# DOMAINS CONFIGURATION
# ============================================
TOTAL_QUESTIONS = len(QUESTION_BANK)
questions_per_domain = TOTAL_QUESTIONS // 5

DOMAINS = {
    "Complete Security Suite": list(range(TOTAL_QUESTIONS)),
    "Domain 1: Core Security Framework": list(range(0, min(35, TOTAL_QUESTIONS))),
    "Domain 2: Threat Intelligence & Attacks": list(range(35, min(70, TOTAL_QUESTIONS))),
    "Domain 3: Security Architecture": list(range(70, min(101, TOTAL_QUESTIONS))),
    "Domain 4: Security Operations": list(range(101, min(134, TOTAL_QUESTIONS))),
    "Domain 5: Security Program Management": list(range(134, TOTAL_QUESTIONS)),
}

# Domain descriptions for better UX
DOMAIN_INFO = {
    "Complete Security Suite": {"icon": "🌐", "desc": "All Security+ domains combined"},
    "Domain 1: Core Security Framework": {"icon": "🔐", "desc": "Basic security concepts, CIA triad, risk management"},
    "Domain 2: Threat Intelligence & Attacks": {"icon": "⚠️", "desc": "Malware, social engineering, network attacks"},
    "Domain 3: Security Architecture": {"icon": "🏗️", "desc": "Network design, cloud security, secure configurations"},
    "Domain 4: Security Operations": {"icon": "🛡️", "desc": "Incident response, monitoring, forensics"},
    "Domain 5: Security Program Management": {"icon": "📋", "desc": "Governance, risk compliance, policies"},
}

# ============================================
# OPTIMIZED CSS (Removed animations for speed)
# ============================================
st.markdown("""
<style>
    /* Base styles - optimized for performance */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0a0a1a 100%);
    }
    
    .cyber-header {
        background: linear-gradient(135deg, #00ffff20 0%, #ff00ff20 100%);
        border-bottom: 2px solid #00ffff;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .glitch-text {
        font-family: 'Courier New', monospace;
        font-size: 2em;
        font-weight: bold;
        color: #00ffff;
        text-shadow: 2px 2px #ff00ff;
    }
    
    .subtitle {
        color: #00ffff;
        font-size: 0.8em;
        margin-top: 5px;
    }
    
    .premium-card {
        background: #0a0a1a;
        border: 1px solid #00ffff33;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .card-title {
        font-size: 1.3em;
        font-weight: bold;
        color: #00ffff;
        text-align: center;
    }
    
    .question-area {
        background: #0a0a1a;
        border: 1px solid #00ffff33;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        text-align: center;
    }
    
    .question-term {
        font-size: 1.5em;
        font-weight: bold;
        color: #00ffff;
        padding: 15px;
    }
    
    .question-label {
        color: #ff00ff;
        font-size: 0.8em;
        margin-bottom: 10px;
    }
    
    .option-btn {
        width: 100%;
        padding: 10px;
        margin: 5px 0;
        background: #1a1a3a;
        border: 1px solid #00ffff33;
        border-radius: 8px;
        color: white;
        text-align: left;
        cursor: pointer;
    }
    
    .option-btn:hover {
        background: #2a2a4a;
        border-color: #00ffff;
    }
    
    .feedback-correct {
        background: #00ff8810;
        border-left: 3px solid #00ff88;
        padding: 10px;
        margin: 10px 0;
        color: #00ff88;
    }
    
    .feedback-wrong {
        background: #ff444410;
        border-left: 3px solid #ff4444;
        padding: 10px;
        margin: 10px 0;
        color: #ff8888;
    }
    
    .score-dashboard {
        background: #0a0a1a;
        border: 1px solid #00ffff33;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    
    .score-number {
        font-size: 2em;
        font-weight: bold;
        color: #00ffff;
    }
    
    .domain-card {
        background: #0a0a1a;
        border: 1px solid #00ffff33;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
        transition: 0.2s;
    }
    
    .domain-card:hover {
        border-color: #00ffff;
        transform: translateY(-2px);
    }
    
    .domain-icon {
        font-size: 2em;
        margin-bottom: 10px;
    }
    
    .domain-name {
        font-weight: bold;
        color: #00ffff;
        margin-bottom: 5px;
    }
    
    .domain-count {
        color: #ff00ff;
        font-size: 0.8em;
    }
    
    .result-card {
        background: #0a0a1a;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border-left: 3px solid;
    }
    
    .result-correct {
        border-left-color: #00ff88;
    }
    
    .result-wrong {
        border-left-color: #ff4444;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        width: 100%;
        transition: 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 10px #00ffff40;
    }
    
    /* Progress bar */
    .progress-bar {
        height: 4px;
        background: #00ffff20;
        border-radius: 2px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ffff, #ff00ff);
        transition: width 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# OPTIMIZED FUNCTIONS
# ============================================

@st.cache_data
def get_filtered_questions(domain_name):
    """Cache filtered questions for better performance"""
    if domain_name is None:
        return QUESTION_BANK
    indices = DOMAINS.get(domain_name, DOMAINS["Complete Security Suite"])
    valid_indices = [i for i in indices if i < len(QUESTION_BANK)]
    return [QUESTION_BANK[i] for i in valid_indices]

def get_current_card():
    """Get current question card"""
    questions = st.session_state.questions_list
    if not questions:
        return None
    if st.session_state.current_card_index >= len(questions):
        return None
    return questions[st.session_state.current_card_index]

def get_current_term_info():
    """Get current term to answer"""
    card = get_current_card()
    if not card:
        return None, None
    
    for idx, term in enumerate(card['terms']):
        if idx not in st.session_state.terms_answered:
            return idx, term
    return None, None

@st.cache_data
def generate_options(_card_title, term_idx, _questions_list):
    """Cache options generation for speed"""
    # Find the card by title
    card = None
    for q in _questions_list:
        if q['title'] == _card_title:
            card = q
            break
    
    if not card:
        return [], None
    
    correct_answer = card['definitions'][term_idx]
    
    # Get distractors from same card
    distractors = []
    for idx, definition in enumerate(card['definitions']):
        if idx != term_idx and definition not in distractors:
            distractors.append(definition)
    
    # Add more distractors if needed
    if len(distractors) < 3:
        for q in _questions_list:
            for definition in q['definitions']:
                if definition not in distractors and definition != correct_answer:
                    distractors.append(definition)
                    if len(distractors) >= 3:
                        break
            if len(distractors) >= 3:
                break
    
    options = [correct_answer] + distractors[:3]
    random.shuffle(options)
    
    return options, correct_answer

def submit_answer(selected_definition):
    """Handle answer submission"""
    card = get_current_card()
    term_idx = st.session_state.current_term_idx
    
    if not card or term_idx is None:
        return
    
    correct_answer = card['definitions'][term_idx]
    is_correct = (selected_definition == correct_answer)
    
    # Record result
    st.session_state.all_results.append({
        'card_title': card['title'],
        'term': card['terms'][term_idx],
        'user_answer': selected_definition,
        'correct_answer': correct_answer,
        'is_correct': is_correct
    })
    
    if is_correct:
        st.session_state.score += 1
        st.session_state.feedback = f"✓ CORRECT! '{card['terms'][term_idx]}' matched successfully."
        st.session_state.feedback_type = "correct"
    else:
        st.session_state.feedback = f"✗ INCORRECT. The correct definition is: {correct_answer}"
        st.session_state.feedback_type = "wrong"
    
    st.session_state.terms_answered.add(term_idx)
    st.session_state.total_questions_answered += 1
    
    # Check if card complete
    if len(st.session_state.terms_answered) == 5:
        st.session_state.card_complete = True
        st.session_state.completed_cards.add(st.session_state.current_card_index)
    else:
        # Move to next term
        st.session_state.current_term_idx, st.session_state.current_term = get_current_term_info()
    
    st.rerun()

def next_card():
    """Move to next card"""
    total = len(st.session_state.questions_list)
    
    if st.session_state.current_card_index < len(st.session_state.shuffled_indices) - 1:
        st.session_state.current_card_index += 1
    else:
        remaining = [i for i in range(total) if i not in st.session_state.completed_cards]
        if not remaining:
            st.session_state.game_active = False
            st.session_state.show_results = True
            return
        random.shuffle(remaining)
        st.session_state.shuffled_indices = remaining
        st.session_state.current_card_index = 0
    
    # Reset card state
    st.session_state.terms_answered = set()
    st.session_state.card_complete = False
    st.session_state.feedback = None
    st.session_state.current_term_idx, st.session_state.current_term = get_current_term_info()
    st.rerun()

def start_game(domain):
    """Start the game with selected domain"""
    st.session_state.selected_domain = domain
    st.session_state.questions_list = get_filtered_questions(domain)
    st.session_state.shuffled_indices = list(range(len(st.session_state.questions_list)))
    random.shuffle(st.session_state.shuffled_indices)
    
    st.session_state.game_active = True
    st.session_state.show_results = False
    st.session_state.current_card_index = 0
    st.session_state.terms_answered = set()
    st.session_state.completed_cards = set()
    st.session_state.score = 0
    st.session_state.total_questions_answered = 0
    st.session_state.all_results = []
    st.session_state.feedback = None
    st.session_state.card_complete = False
    
    st.session_state.current_term_idx, st.session_state.current_term = get_current_term_info()
    st.rerun()

def reset_game():
    """Reset to domain selection"""
    st.session_state.game_active = False
    st.session_state.show_results = False
    st.session_state.selected_domain = None
    st.rerun()

# ============================================
# MAIN UI
# ============================================

# Header
st.markdown("""
<div class="cyber-header">
    <div class="glitch-text">🔒 CYBER VAULT</div>
    <div class="subtitle">SECURITY+ CERTIFICATION TRAINING</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# DOMAIN SELECTION SCREEN
# ============================================
if not st.session_state.game_active and not st.session_state.show_results:
    st.markdown("### Select Your Training Domain")
    
    # Create 2 columns for domain cards
    col1, col2 = st.columns(2)
    
    domain_items = list(DOMAINS.items())
    half = len(domain_items) // 2 + len(domain_items) % 2
    
    with col1:
        for domain_name, indices in domain_items[:half]:
            count = len(indices)
            info = DOMAIN_INFO.get(domain_name, {"icon": "📚", "desc": "Security concepts"})
            
            with st.container():
                st.markdown(f"""
                <div class="domain-card">
                    <div class="domain-icon">{info['icon']}</div>
                    <div class="domain-name">{domain_name}</div>
                    <div class="domain-count">{count} Questions</div>
                    <div style="font-size: 0.7em; color: #888; margin-top: 5px;">{info['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Start {domain_name}", key=f"domain_{domain_name[:20]}", use_container_width=True):
                    start_game(domain_name)
    
    with col2:
        for domain_name, indices in domain_items[half:]:
            count = len(indices)
            info = DOMAIN_INFO.get(domain_name, {"icon": "📚", "desc": "Security concepts"})
            
            with st.container():
                st.markdown(f"""
                <div class="domain-card">
                    <div class="domain-icon">{info['icon']}</div>
                    <div class="domain-name">{domain_name}</div>
                    <div class="domain-count">{count} Questions</div>
                    <div style="font-size: 0.7em; color: #888; margin-top: 5px;">{info['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Start {domain_name}", key=f"domain_{domain_name[:20]}_2", use_container_width=True):
                    start_game(domain_name)
    
    st.markdown("---")
    st.info("💡 **How it works:** Each module contains 5 terms to match with definitions. Answer each question to build your Security+ knowledge!")

# ============================================
# RESULTS SCREEN
# ============================================
elif st.session_state.show_results:
    total = len(st.session_state.all_results)
    correct = st.session_state.score
    percentage = (correct / total * 100) if total > 0 else 0
    
    # Grade calculation
    if percentage >= 90:
        grade = "S+"
        grade_color = "#00ff88"
        message = "Outstanding! You're ready for the Security+ exam!"
    elif percentage >= 80:
        grade = "S"
        grade_color = "#00ffff"
        message = "Excellent! Strong understanding of Security+ concepts!"
    elif percentage >= 70:
        grade = "A"
        grade_color = "#ffd700"
        message = "Good job! Review missed questions to improve."
    elif percentage >= 60:
        grade = "B"
        grade_color = "#ff8800"
        message = "Satisfactory. Keep practicing to strengthen weak areas."
    else:
        grade = "C"
        grade_color = "#ff4444"
        message = "Review all correct answers below and try again."
    
    # Results display
    st.markdown(f"""
    <div class="premium-card">
        <div style="text-align: center;">
            <h2 style="color: #00ffff;">📊 Final Grade Report</h2>
            <div style="font-size: 3em; font-weight: bold; color: {grade_color}; margin: 20px 0;">
                {percentage:.0f}%
            </div>
            <div style="font-size: 1.5em; color: #00ffff;">Grade {grade}</div>
            <div style="font-size: 1.2em; margin: 10px 0;">{correct}/{total} Correct</div>
            <div style="color: #00ff88;">{message}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed results
    st.markdown("### 📝 Detailed Answer Review")
    
    for i, result in enumerate(st.session_state.all_results, 1):
        with st.expander(f"{'✓' if result['is_correct'] else '✗'} {i}. {result['term']}"):
            st.markdown(f"""
            **Your Answer:** {result['user_answer']}  
            **Correct Answer:** `{result['correct_answer']}`  
            **Status:** {'✅ CORRECT' if result['is_correct'] else '❌ INCORRECT'}
            """)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Session", use_container_width=True):
            reset_game()
    with col2:
        if st.button("🏠 Change Domain", use_container_width=True):
            reset_game()

# ============================================
# GAME ACTIVE SCREEN
# ============================================
elif st.session_state.game_active:
    current_card = get_current_card()
    
    if current_card is None:
        st.warning("No questions available.")
        st.stop()
    
    # Sidebar - Progress Dashboard
    with st.sidebar:
        st.markdown("### 📊 Progress Dashboard")
        
        # Score display
        st.markdown(f"""
        <div class="score-dashboard">
            <div class="score-number">{st.session_state.score}</div>
            <div>Correct Answers</div>
            <div style="font-size: 0.8em;">Out of {st.session_state.total_questions_answered}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Accuracy
        if st.session_state.total_questions_answered > 0:
            accuracy = (st.session_state.score / st.session_state.total_questions_answered) * 100
            st.markdown(f"""
            <div class="score-dashboard">
                <div style="font-size: 1.5em; color: #ff00ff;">{accuracy:.1f}%</div>
                <div>Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Module progress
        cards_completed = len(st.session_state.completed_cards)
        total_cards = len(st.session_state.questions_list)
        st.markdown(f"""
        <div class="score-dashboard">
            <div style="font-size: 1.2em;">Modules: {cards_completed}/{total_cards}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {(cards_completed/total_cards*100) if total_cards>0 else 0}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Current module progress
        terms_done = len(st.session_state.terms_answered)
        st.markdown(f"""
        <div class="score-dashboard">
            <div>Current Module: {terms_done}/5 Terms</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {terms_done/5*100}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🚪 End Session", use_container_width=True):
            st.session_state.game_active = False
            st.session_state.show_results = True
            st.rerun()
    
    # Main Game Area
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">{current_card['title']}</div>
        <div style="text-align: center; color: #666; margin-top: 5px;">Module {st.session_state.current_card_index + 1} of {len(st.session_state.questions_list)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Card Complete - Show Next Button
    if st.session_state.card_complete:
        st.markdown("""
        <div style="text-align: center; padding: 30px; background: #00ff8810; border-radius: 10px; margin: 20px 0;">
            <h2 style="color: #00ff88;">✓ Module Complete!</h2>
            <p>All 5 terms have been answered.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➡️ Next Module", use_container_width=True):
            next_card()
    
    # Show current question
    elif st.session_state.current_term is not None:
        st.markdown(f"""
        <div class="question-area">
            <div class="question-label">Define this term:</div>
            <div class="question-term">{st.session_state.current_term}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate options
        options, correct_answer = generate_options(
            current_card['title'], 
            st.session_state.current_term_idx,
            st.session_state.questions_list
        )
        
        # Display options as buttons
        for idx, option in enumerate(options):
            if st.button(f"▸ {option}", key=f"opt_{idx}_{option[:30]}", use_container_width=True):
                submit_answer(option)
        
        # Show feedback after answering
        if st.session_state.feedback:
            feedback_class = "feedback-correct" if st.session_state.feedback_type == "correct" else "feedback-wrong"
            st.markdown(f"""
            <div class="{feedback_class}">
                {st.session_state.feedback}
            </div>
            """, unsafe_allow_html=True)
    
    # Show completed terms for this module
    if len(st.session_state.terms_answered) > 0:
        st.markdown("---")
        st.markdown("### ✅ Completed Terms")
        for term_idx in st.session_state.terms_answered:
            st.success(f"**{current_card['terms'][term_idx]}** → {current_card['definitions'][term_idx]}")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#666; font-size:0.75em;'>Cyber Vault | Security+ Certification Training Platform</p>", unsafe_allow_html=True)
