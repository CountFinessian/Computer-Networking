# Quick Start Guide - BYU Freshman Assistant

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Choose Your Experience

#### Option A: Watch the Demo (Recommended First)
See all capabilities demonstrated with example scenarios:
```bash
python byu_freshman_assistant.py
```

This shows:
- ✅ All 6 specialized agents in action
- ✅ Sample student profile
- ✅ Common freshman questions answered
- ✅ Personalized summary generation

#### Option B: Interactive Assistant
Have a conversation with the assistant:
```bash
python interactive_assistant.py
```

Follow the prompts to:
1. Create your student profile
2. Ask questions across 6 categories
3. Get personalized recommendations

#### Option C: Detailed Scenarios
See real-world use cases:
```bash
python example_scenarios.py
```

This walks through:
- The Overwhelmed Freshman (academic stress)
- The Undecided Explorer (choosing majors)
- The Struggling Student (mental health)
- The Proactive Planner (optimization)
- The Lost Freshman (campus navigation)
- Comprehensive check-in summary

### Step 3: Explore the Code

#### Main Files:
- `byu_freshman_assistant.py` - Core agentic framework (800+ lines)
- `byu_data.py` - BYU knowledge base (450+ data points)
- `interactive_assistant.py` - CLI interface
- `example_scenarios.py` - Real-world demonstrations

#### Documentation:
- `README.md` - Overview and features
- `ARCHITECTURE.md` - Technical deep-dive
- `QUICKSTART.md` - This file!

## 💡 Example Usage

### Programmatic Usage

```python
from byu_freshman_assistant import BYUFreshmanAssistant, StudentProfile, Priority

# Create your profile
you = StudentProfile(
    name="Your Name",
    major="Your Major",
    courses_enrolled=["CS 111", "MATH 112"],
    interests=["coding", "sports"],
    goals=["Excel academically", "Make friends"]
)

# Create assistant
assistant = BYUFreshmanAssistant(you)

# Ask questions
result = assistant.ask("What courses should I take?", Priority.HIGH)
print(result)

# Get comprehensive summary
summary = assistant.get_summary()
```

### Common Questions to Try

**Academic:**
- "What courses should I take next semester?"
- "How do I check my degree progress?"
- "What are the prerequisites for CS 235?"

**Navigation:**
- "Where is the TMCB building?"
- "Where can I park on campus?"
- "Where can I eat lunch?"

**Time Management:**
- "Help me create a study schedule"
- "I'm procrastinating on assignments"
- "How do I prioritize my deadlines?"

**Social:**
- "How do I make friends at BYU?"
- "Where can I find study groups?"
- "What clubs should I join?"

**Resources:**
- "I need tutoring help"
- "Where is the counseling center?"
- "How do I find career services?"

**Wellness:**
- "I'm feeling stressed"
- "Help me sleep better"
- "Where can I exercise on campus?"

## 🎯 What Makes This Agentic?

Unlike a simple FAQ bot, this system:

1. **Multiple Specialized Agents**
   - Each agent is an expert in one domain
   - Coordinator routes questions to the right specialist
   - Agents can collaborate on complex requests

2. **Personalized Responses**
   - Uses your major, interests, and goals
   - Recommendations adapt to your situation
   - Different advice for CS vs Nursing vs Business

3. **Priority-Based Processing**
   - Mental health crises get immediate resources
   - Urgent vs. normal vs. low priority routing
   - Time-sensitive advice (registration deadlines, etc.)

4. **Comprehensive Knowledge Base**
   - 450+ BYU-specific data points
   - Building locations, resources, courses
   - Real contact info and hours

5. **Holistic Support**
   - Academic AND social AND wellness
   - Proactive recommendations
   - Prevents problems before they become crises

## 📊 System Architecture

```
Your Question
     ↓
Coordinator Agent (analyzes & routes)
     ↓
┌────────────┬──────────┬─────────┬─────────┬──────────┬──────────┐
│  Academic  │ Navigate │  Time   │ Social  │ Resource │ Wellness │
│   Agent    │  Agent   │  Agent  │ Agent   │  Agent   │  Agent   │
└────────────┴──────────┴─────────┴─────────┴──────────┴──────────┘
     ↓
Personalized Response Based On:
- Your major
- Your courses
- Your interests
- Your goals
- BYU knowledge base
```

## 🔧 Customization

### Add Your Own Data

Edit `byu_data.py` to add:
- More buildings
- Updated dining hours
- Your favorite study spots
- Major-specific resources

### Create New Agents

```python
class MyNewAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.NEW, "My Agent")
        self.capabilities = ["feature1", "feature2"]
    
    def process(self, task, student):
        # Your logic here
        return {"success": True, "data": "..."}

# Register it
coordinator.agents[AgentType.NEW] = MyNewAgent()
```

## 🎓 Learning Objectives

By exploring this code, you'll learn:

1. **Agentic Architecture Patterns**
   - Multi-agent coordination
   - Task routing and delegation
   - Specialized domain expertise

2. **Software Design Principles**
   - Separation of concerns
   - Modularity and extensibility
   - Strategy pattern
   - Factory pattern

3. **Real-World Problem Solving**
   - Addressing user needs holistically
   - Personalization strategies
   - Priority-based systems
   - Knowledge base design

## 📈 Next Steps

### Try These Challenges:

1. **Add a New Agent**
   - Create a "Study Abroad Agent" for international programs
   - Create a "Campus Safety Agent" for security resources

2. **Enhance Routing**
   - Replace keyword matching with semantic similarity
   - Use an LLM for intent classification

3. **Add Persistence**
   - Save student profiles to JSON/database
   - Track conversation history
   - Remember preferences

4. **Build an Interface**
   - Web app with Flask/FastAPI
   - Discord bot
   - SMS integration with Twilio

5. **Add Real Data**
   - Connect to BYU APIs
   - Scrape current course catalog
   - Integrate with Learning Suite

## 🐛 Troubleshooting

**Issue**: Module not found
```bash
# Make sure you're in the right directory
cd 04-lab-link-layer
pip install -r requirements.txt
```

**Issue**: Wrong agent responds
- This is expected with keyword-based routing
- Try rephrasing your question
- Or specify category in interactive mode

**Issue**: Want different recommendations
- Modify your student profile
- Change major, interests, or goals
- Agents personalize based on profile

## 💬 Get Help

The interactive assistant has:
- Guided menus (no need to remember commands)
- Examples for each category
- Help text throughout

Start with:
```bash
python interactive_assistant.py
```

## 🎉 Have Fun!

This is a powerful demonstration of agentic AI systems solving real-world problems. Explore, modify, and make it your own!

**Go Cougars!** 🏈

---

Questions? Check out:
- `README.md` for overview
- `ARCHITECTURE.md` for technical details
- The code itself - it's well-commented!

