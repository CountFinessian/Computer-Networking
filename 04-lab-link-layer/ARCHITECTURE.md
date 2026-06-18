# BYU Freshman Assistant - Architecture Documentation

## 🏗️ System Architecture

The BYU Freshman Assistant implements an **agentic workflow architecture** where multiple specialized AI agents collaborate to solve complex problems that first-year college students face.

## 🎯 Core Design Philosophy

### Why Agentic Architecture?

Traditional approaches to student support often involve:
- Multiple disconnected resources
- Students not knowing where to find help
- Reactive rather than proactive support
- One-size-fits-all guidance

Our agentic system solves these problems by:
1. **Centralizing knowledge** across all campus resources
2. **Intelligent routing** to the right expert for each question
3. **Personalization** based on major, goals, and situation
4. **Proactive recommendations** before problems become crises

## 🤖 Agent Architecture

### 1. Coordinator Agent (Router)

**Role**: Main entry point that analyzes requests and routes to specialists

```python
class CoordinatorAgent:
    - Receives all student queries
    - Analyzes intent using keyword matching
    - Routes to appropriate specialist agent
    - Can split complex queries into subtasks
    - Aggregates results from multiple agents
```

**Routing Logic:**
- Academic keywords → Academic Agent
- Location/building keywords → Navigation Agent
- Time/schedule keywords → Time Management Agent
- Social/friend keywords → Social Connection Agent
- Resource/help keywords → Resource Finder Agent
- Wellness/stress keywords → Wellness Agent

### 2. Specialized Agents

Each agent inherits from `BaseAgent` and implements specific domain expertise:

#### Academic Planning Agent
```python
Capabilities:
- Course recommendations based on major
- Schedule optimization (credits, balance, timing)
- Prerequisite checking and tracking
- Degree progress monitoring
- Registration guidance

Knowledge Base:
- Course catalog by major
- General education requirements
- Prerequisite chains
- Typical freshman year paths
```

#### Campus Navigation Agent
```python
Capabilities:
- Building location lookup
- Route planning between classes
- Parking recommendations
- Dining options and hours
- Campus map knowledge

Knowledge Base:
- Building coordinates and details
- Parking lot locations
- Dining facilities with menus/hours
- Walking time estimates
```

#### Time Management Agent
```python
Capabilities:
- Study schedule creation
- Deadline prioritization (Eisenhower Matrix)
- Anti-procrastination strategies
- Time blocking techniques
- Productivity coaching

Knowledge Base:
- Pomodoro technique
- 2-hour-per-credit rule
- Eisenhower priority matrix
- Evidence-based study strategies
```

#### Social Connection Agent
```python
Capabilities:
- Study group formation help
- Friend-making strategies
- Roommate conflict resolution
- Club recommendations
- Community building

Knowledge Base:
- BYU clubs by interest/major
- Ward/branch structure
- Social event calendars
- Proven friend-making strategies
```

#### Resource Finder Agent
```python
Capabilities:
- Finding tutoring services
- Mental health resources
- Career services
- Financial aid information
- Health services

Knowledge Base:
- Complete directory of BYU resources
- Contact information
- Hours and locations
- Costs and eligibility
- How to access each service
```

#### Wellness Agent
```python
Capabilities:
- Stress management strategies
- Sleep optimization
- Exercise planning
- Spiritual wellness support
- Work-life balance coaching

Knowledge Base:
- Evidence-based wellness practices
- BYU fitness facilities
- Mental health resources
- Spiritual development strategies
- Crisis intervention protocols
```

## 📊 Data Flow

```
Student Question
      ↓
Coordinator Agent (analyzes intent)
      ↓
Routes to appropriate specialist(s)
      ↓
Specialist Agent processes using:
  - Domain knowledge base
  - Student profile
  - Contextual understanding
      ↓
Returns structured response
      ↓
Coordinator formats and delivers
      ↓
Student receives actionable guidance
```

## 🗂️ Data Structures

### Task
```python
@dataclass
class Task:
    id: str                          # Unique identifier
    description: str                 # What student is asking
    priority: Priority               # LOW, MEDIUM, HIGH, URGENT
    deadline: Optional[datetime]     # If time-sensitive
    assigned_agent: AgentType        # Which specialist handles it
    status: str                      # pending/completed
    result: Any                      # Agent's response
    subtasks: List[Task]             # For complex requests
```

### StudentProfile
```python
@dataclass
class StudentProfile:
    name: str
    major: str
    credits_completed: int
    preferred_study_times: List[str]
    interests: List[str]
    courses_enrolled: List[str]
    goals: List[str]
```

This profile enables **personalization** - agents tailor advice to:
- Major (different courses, clubs, resources)
- Credits (freshman vs sophomore advice)
- Interests (club recommendations, social activities)
- Goals (align recommendations with student objectives)

## 🔄 Workflow Patterns

### 1. Simple Query Pattern
```
Question → Coordinator → Single Agent → Response
Example: "Where is TMCB?" → Navigation Agent
```

### 2. Multi-Agent Pattern
```
Complex Question → Coordinator → Multiple Agents → Aggregated Response
Example: "How do I succeed this semester?"
  → Academic Agent (course strategy)
  → Time Management Agent (schedule)
  → Wellness Agent (balance tips)
```

### 3. Hierarchical Task Decomposition
```
Large Request → Coordinator breaks into subtasks
  → Each subtask to appropriate agent
  → Results combined into comprehensive plan

Example: "I'm struggling in college"
  1. Academic Agent: tutoring resources
  2. Time Management Agent: study schedule
  3. Wellness Agent: stress management
  4. Resource Finder Agent: counseling options
```

### 4. Priority Escalation
```
URGENT request → Immediate routing to crisis resources
Normal request → Standard processing

Example: "I'm having thoughts of self-harm"
  → URGENT priority
  → Wellness Agent provides immediate crisis resources
  → Skips non-essential recommendations
```

## 🧠 Intelligence & Personalization

### How Agents "Know" What to Recommend

1. **Student Profile Matching**
   - Major → major-specific courses, clubs, resources
   - Credits → appropriate difficulty level advice
   - Interests → relevant clubs and activities

2. **Contextual Understanding**
   - Time of year → registration deadlines, finals prep
   - Course load → balance recommendations
   - Expressed stress level → wellness resource urgency

3. **Knowledge Base Queries**
   ```python
   if student.major == "CS":
       recommend_courses = CS_freshman_courses
       recommend_clubs = ["ACM", "Cyber Security Club"]
   ```

4. **Evidence-Based Strategies**
   - Study techniques backed by research
   - Proven time management methods
   - Clinical mental health guidelines

## 🔐 Safety & Ethics

### Mental Health Safeguards

1. **Crisis Detection**
   - Keywords trigger URGENT priority
   - Immediate resource provision
   - Clear escalation pathways

2. **Resource Limitations**
   - Agents acknowledge they're not counselors
   - Always refer serious issues to professionals
   - Provide 24/7 crisis line information

3. **Confidentiality**
   - System emphasizes CAPS is confidential
   - No judgment messaging
   - Normalizes seeking help

### Academic Integrity

- Never provides answers to assignments
- Teaches HOW to study, not what to memorize
- Directs to tutoring for subject matter help

## 📈 Scalability Considerations

### Current Implementation (Prototype)
- Rule-based routing
- Static knowledge base
- Synchronous processing

### Production-Ready Enhancements

1. **LLM Integration**
   ```python
   # Replace keyword matching with semantic understanding
   intent = openai.ChatCompletion.create(
       model="gpt-4",
       messages=[{"role": "user", "content": query}]
   )
   ```

2. **Dynamic Knowledge Base**
   - Connect to BYU APIs for live data
   - Course catalog updates
   - Real-time building hours
   - Event calendars

3. **Persistent Storage**
   ```python
   # Track student interactions over time
   database.store_interaction(student_id, query, response, outcome)
   
   # Learn from patterns
   if student repeatedly asks time management questions:
       proactively suggest Academic Success Center workshop
   ```

4. **Asynchronous Processing**
   ```python
   # For complex multi-agent queries
   async def process_complex_query(query):
       tasks = await asyncio.gather(
           academic_agent.process(),
           time_agent.process(),
           wellness_agent.process()
       )
       return aggregate_results(tasks)
   ```

## 🔧 Extensibility

### Adding New Agents

```python
class NewSpecializedAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.NEW_TYPE, "New Agent Name")
        self.capabilities = ["capability1", "capability2"]
        self._load_knowledge()
    
    def process(self, task, student):
        # Implement domain-specific logic
        return result

# Register with coordinator
coordinator.agents[AgentType.NEW_TYPE] = NewSpecializedAgent()
```

### Expanding Knowledge Bases

```python
# byu_data.py is modular - add new data structures
NEW_RESOURCE_CATEGORY = {
    "resource_name": {
        "location": "...",
        "services": [...],
        "hours": "...",
        "cost": "..."
    }
}
```

## 🎓 Educational Value

This architecture demonstrates:

1. **Separation of Concerns**: Each agent has single responsibility
2. **Modularity**: Easy to add/remove/modify agents
3. **Abstraction**: BaseAgent provides common interface
4. **Composition**: Complex behaviors from simple agents
5. **Strategy Pattern**: Different agents for different strategies
6. **Factory Pattern**: Coordinator creates/routes to agents

## 📊 Performance Metrics

For production deployment, track:

```python
metrics = {
    "response_time": "Time from query to answer",
    "accuracy": "Was the right agent chosen?",
    "user_satisfaction": "Did answer help?",
    "resource_usage": "Most requested services",
    "problem_areas": "Common struggles",
    "intervention_success": "Did proactive help prevent crisis?"
}
```

## 🔮 Future Architecture Evolution

### Phase 1: Enhanced Intelligence
- Add LLM for natural language understanding
- Semantic search over knowledge base
- Multi-turn conversations with context

### Phase 2: Predictive Capabilities
- ML model to predict student struggles
- Proactive outreach before crisis
- Personalized intervention timing

### Phase 3: Multi-Modal Support
- Voice interface (Alexa skill)
- SMS/text integration
- Mobile app with push notifications
- Discord/Slack bot

### Phase 4: Ecosystem Integration
- Learning Suite API connection
- Google Calendar sync
- BYU authentication
- Academic record access (with permission)

## 🏁 Conclusion

The agentic architecture provides:
- **Scalability**: Easy to add new capabilities
- **Maintainability**: Each agent is independent
- **Flexibility**: Can reconfigure agent relationships
- **Personalization**: Student profile drives recommendations
- **Holistic Support**: Addresses all aspects of student life

This design pattern is applicable beyond BYU to any complex domain requiring specialized expertise coordinated toward helping users navigate challenging situations.

---

**Architecture Version**: 1.0  
**Last Updated**: October 2025  
**Status**: Prototype/Educational Demonstration

