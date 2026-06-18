"""
BYU Freshman Assistant - Agentic Workflow System
A multi-agent system designed to help first-year BYU students navigate common challenges.

Key Features:
- Academic Planning Agent: Course selection, scheduling, prerequisite tracking
- Campus Navigation Agent: Building locations, shortest paths, class timing
- Time Management Agent: Assignment tracking, study scheduling, deadline management
- Social Connection Agent: Study group matching, roommate coordination, activity recommendations
- Resource Finder Agent: Finding tutoring, advising, counseling, and other campus resources
- Wellness Agent: Managing stress, sleep, exercise, and spiritual activities
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json


class AgentType(Enum):
    COORDINATOR = "coordinator"
    ACADEMIC = "academic"
    NAVIGATION = "navigation"
    TIME_MANAGEMENT = "time_management"
    SOCIAL = "social"
    RESOURCE_FINDER = "resource_finder"
    WELLNESS = "wellness"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    """Represents a task in the system"""
    id: str
    description: str
    priority: Priority
    deadline: Optional[datetime] = None
    assigned_agent: Optional[AgentType] = None
    status: str = "pending"
    result: Optional[Any] = None
    subtasks: List['Task'] = field(default_factory=list)


@dataclass
class StudentProfile:
    """Student information and preferences"""
    name: str
    major: str
    credits_completed: int = 0
    preferred_study_times: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    courses_enrolled: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, agent_type: AgentType, name: str):
        self.agent_type = agent_type
        self.name = name
        self.capabilities = []
        self.knowledge_base = {}
    
    def can_handle(self, task: Task) -> bool:
        """Determine if this agent can handle the given task"""
        return task.assigned_agent == self.agent_type
    
    def process(self, task: Task, student: StudentProfile) -> Dict[str, Any]:
        """Process a task and return results"""
        raise NotImplementedError("Subclasses must implement process method")
    
    def log(self, message: str):
        """Log agent activities"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.name}] {message}")


class AcademicPlanningAgent(BaseAgent):
    """Agent specialized in course planning, scheduling, and academic advising"""
    
    def __init__(self):
        super().__init__(AgentType.ACADEMIC, "Academic Planning Agent")
        self.capabilities = [
            "course_recommendations",
            "schedule_optimization",
            "prerequisite_checking",
            "degree_progress_tracking",
            "registration_assistance"
        ]
        self._load_course_catalog()
    
    def _load_course_catalog(self):
        """Load BYU course information"""
        self.knowledge_base = {
            "general_education": {
                "first_year_writing": ["WRTG 150"],
                "american_heritage": ["HIST 202", "POLI 202"],
                "foundations": ["languages", "civilization", "letters"],
            },
            "common_freshman_courses": {
                "CS": ["CS 110", "CS 111", "CS 142", "MATH 112", "MATH 113"],
                "Engineering": ["ENGR 101", "CHEM 105", "MATH 112", "PHSCS 121"],
                "Business": ["ECON 110", "ACC 200", "BUS 110", "MATH 119"],
                "Nursing": ["NURS 104", "CHEM 105", "BIO 100", "NDFS 100"],
            },
            "prerequisite_chains": {
                "CS 142": ["CS 111"],
                "CS 235": ["CS 142"],
                "MATH 113": ["MATH 112"],
                "CHEM 106": ["CHEM 105"],
            }
        }
    
    def process(self, task: Task, student: StudentProfile) -> Dict[str, Any]:
        """Process academic-related tasks"""
        self.log(f"Processing academic task: {task.description}")
        
        description_lower = task.description.lower()
        
        if "schedule" in description_lower or "courses" in description_lower:
            return self._recommend_schedule(student)
        elif "prerequisite" in description_lower:
            return self._check_prerequisites(student)
        elif "progress" in description_lower or "degree" in description_lower:
            return self._track_degree_progress(student)
        else:
            return self._general_academic_advice(student)
    
    def _recommend_schedule(self, student: StudentProfile) -> Dict[str, Any]:
        """Recommend courses for the student"""
        recommendations = []
        
        # Get major-specific courses
        major_courses = self.knowledge_base["common_freshman_courses"].get(
            student.major, []
        )
        
        # Add general education requirements
        if student.credits_completed < 30:
            recommendations.append({
                "course": "WRTG 150",
                "name": "First-Year Writing",
                "credits": 3,
                "reason": "Required general education",
                "priority": "HIGH"
            })
            recommendations.append({
                "course": "American Heritage",
                "name": "Choose HIST 202 or POLI 202",
                "credits": 3,
                "reason": "Required general education",
                "priority": "HIGH"
            })
        
        # Add major courses
        for course in major_courses[:3]:
            recommendations.append({
                "course": course,
                "name": f"{student.major} Core Course",
                "credits": 3,
                "reason": f"Core requirement for {student.major} major",
                "priority": "HIGH"
            })
        
        # Add a religion course
        recommendations.append({
            "course": "Book of Mormon or New Testament",
            "name": "Religion Course",
            "credits": 2,
            "reason": "Religion requirement (need 14 total)",
            "priority": "MEDIUM"
        })
        
        return {
            "success": True,
            "recommendations": recommendations,
            "total_credits": sum(r["credits"] for r in recommendations),
            "advice": "Aim for 14-16 credits your first semester to adjust to college life."
        }
    
    def _check_prerequisites(self, student: StudentProfile) -> Dict[str, Any]:
        """Check if student has prerequisites for courses"""
        results = []
        
        for target_course, prereqs in self.knowledge_base["prerequisite_chains"].items():
            has_prereqs = all(p in student.courses_enrolled for p in prereqs)
            results.append({
                "course": target_course,
                "prerequisites": prereqs,
                "eligible": has_prereqs,
                "missing": [p for p in prereqs if p not in student.courses_enrolled]
            })
        
        return {
            "success": True,
            "prerequisite_check": results
        }
    
    def _track_degree_progress(self, student: StudentProfile) -> Dict[str, Any]:
        """Track progress toward degree completion"""
        total_required = 120
        completed = student.credits_completed
        remaining = total_required - completed
        percent_complete = (completed / total_required) * 100
        
        return {
            "success": True,
            "credits_completed": completed,
            "credits_remaining": remaining,
            "percent_complete": round(percent_complete, 1),
            "on_track": completed >= 15,  # Should have ~15 credits after first semester
            "advice": "You need 120 total credits to graduate. Stay on track with 15 credits per semester."
        }
    
    def _general_academic_advice(self, student: StudentProfile) -> Dict[str, Any]:
        """Provide general academic guidance"""
        return {
            "success": True,
            "advice": [
                "Meet with your academic advisor at least once per semester",
                "Don't overload your first semester - 14-16 credits is ideal",
                "Balance hard and easy classes",
                "Register early - popular classes fill up fast",
                "Use Rate My Professors and BYU reviews to research instructors"
            ]
        }


class CampusNavigationAgent(BaseAgent):
    """Agent for campus navigation and building locations"""
    
    def __init__(self):
        super().__init__(AgentType.NAVIGATION, "Campus Navigation Agent")
        self.capabilities = [
            "building_locations",
            "route_planning",
            "parking_info",
            "dining_locations",
            "class_timing_analysis"
        ]
        self._load_campus_map()
    
    def _load_campus_map(self):
        """Load campus building information"""
        self.knowledge_base = {
            "buildings": {
                "TMCB": {"name": "Talmage Math/CS Building", "location": "North Campus", "parking": "Lot 34"},
                "ESC": {"name": "Engineering Sciences Center", "location": "North Campus", "parking": "Lot 34"},
                "MARB": {"name": "Marriott School", "location": "Central Campus", "parking": "Lot 45"},
                "JSB": {"name": "Joseph Smith Building", "location": "Central Campus", "parking": "Lot 16"},
                "HBLL": {"name": "Harold B. Lee Library", "location": "Central Campus", "parking": "Lot 16"},
                "WILK": {"name": "Wilkinson Student Center", "location": "Central Campus", "parking": "Lot 16"},
                "LSB": {"name": "Life Sciences Building", "location": "East Campus", "parking": "Lot 22"},
                "SWKT": {"name": "Benson Building", "location": "South Campus", "parking": "Lot 43"},
            },
            "dining": {
                "Cougareat": {"building": "WILK", "hours": "7am-8pm"},
                "Legends Grille": {"building": "WILK", "hours": "11am-8pm"},
                "Skyroom": {"building": "WILK", "hours": "11am-2pm"},
                "Cannon Commons": {"building": "Heritage Halls", "hours": "7am-8pm"},
            }
        }
    
    def process(self, task: Task, student: StudentProfile) -> Dict[str, Any]:
        """Process navigation-related tasks"""
        self.log(f"Processing navigation task: {task.description}")
        
        description_lower = task.description.lower()
        
        if "building" in description_lower or "find" in description_lower:
            return self._find_buildings(task.description)
        elif "route" in description_lower or "walk" in description_lower:
            return self._plan_route(task.description)
        elif "parking" in description_lower:
            return self._find_parking()
        elif "food" in description_lower or "eat" in description_lower:
            return self._find_dining()
        else:
            return self._general_navigation_info()
    
    def _find_buildings(self, description: str) -> Dict[str, Any]:
        """Find building locations"""
        found_buildings = []
        
        for code, info in self.knowledge_base["buildings"].items():
            if code.lower() in description.lower():
                found_buildings.append({
                    "code": code,
                    "name": info["name"],
                    "location": info["location"],
                    "parking": info["parking"]
                })
        
        if not found_buildings:
            return {
                "success": False,
                "message": "Building not found. Try checking maps.byu.edu"
            }
        
        return {
            "success": True,
            "buildings": found_buildings,
            "tip": "Use the BYU Mobile app for real-time navigation"
        }
    
    def _plan_route(self, description: str) -> Dict[str, Any]:
        """Plan route between classes"""
        return {
            "success": True,
            "advice": [
                "Allow 10 minutes between classes in the same area",
                "Allow 15-20 minutes between North and Central campus",
                "Use the campus shuttle for longer distances",
                "Winter: Add 5 minutes for icy conditions",
                "Download the BYU Mobile app for real-time bus tracking"
            ]
        }
    
    def _find_parking(self) -> Dict[str, Any]:
        """Provide parking information"""
        return {
            "success": True,
            "parking_tips": [
                "Freshmen living on campus: Y Lot parking is available",
                "Commuters: Get to campus by 8am for best parking",
                "Best lots: 34 (North), 16 (Central), 43 (South)",
                "Evening parking (after 5pm): Generally abundant",
                "Consider UVX bus from Orem/Provo for free transport"
            ],
            "permit_info": "Purchase parking permits at police.byu.edu"
        }
    
    def _find_dining(self) -> Dict[str, Any]:
        """Find dining options"""
        return {
            "success": True,
            "dining_options": self.knowledge_base["dining"],
            "meal_plan_tip": "Dining Plus works at all locations. Pre-load for 10% bonus!"
        }
    
    def _general_navigation_info(self) -> Dict[str, Any]:
        """Provide general navigation guidance"""
        return {
            "success": True,
            "tips": [
                "Use maps.byu.edu to find any building",
                "Download BYU Mobile app for bus routes",
                "Most classes are in walking distance (10-15 min)",
                "Campus is very walkable - enjoy the scenery!",
                "In winter, use the tunnels between buildings"
            ]
        }


class TimeManagementAgent(BaseAgent):
    """Agent for time management and deadline tracking"""
    
    def __init__(self):
        super().__init__(AgentType.TIME_MANAGEMENT, "Time Management Agent")
        self.capabilities = [
            "assignment_tracking",
            "study_scheduling",
            "deadline_prioritization",
            "time_blocking",
            "procrastination_prevention"
        ]
    
    def process(self, task: Task, student: StudentProfile) -> Dict[str, Any]:
        """Process time management tasks"""
        self.log(f"Processing time management task: {task.description}")
        
        description_lower = task.description.lower()
        
        if "schedule" in description_lower or "plan" in description_lower:
            return self._create_study_schedule(student)
        elif "deadline" in description_lower or "assignment" in description_lower:
            return self._prioritize_deadlines()
        elif "procrastination" in description_lower:
            return self._anti_procrastination_advice()
        else:
            return self._general_time_management_advice()
    
    def _create_study_schedule(self, student: StudentProfile) -> Dict[str, Any]:
        """Create a study schedule for the student"""
        schedule = {
            "Monday": [
                {"time": "8:00-9:00", "activity": "Review class notes from previous week"},
                {"time": "10:00-12:00", "activity": "Major coursework block 1"},
                {"time": "14:00-16:00", "activity": "Major coursework block 2"},
                {"time": "19:00-20:00", "activity": "Reading assignments"}
            ],
            "Tuesday": [
                {"time": "9:00-11:00", "activity": "Major coursework block 1"},
                {"time": "14:00-16:00", "activity": "Problem sets/homework"},
                {"time": "19:00-20:00", "activity": "Review and prepare for next day"}
            ],
            "Wednesday": [
                {"time": "8:00-9:00", "activity": "Weekly review session"},
                {"time": "10:00-12:00", "activity": "Major coursework block 1"},
                {"time": "14:00-16:00", "activity": "Major coursework block 2"},
                {"time": "19:00-20:00", "activity": "Reading assignments"}
            ],
            "Thursday": [
                {"time": "9:00-11:00", "activity": "Major coursework block 1"},
                {"time": "14:00-16:00", "activity": "Catch-up and overflow work"},
                {"time": "19:00-20:00", "activity": "Review and prepare for next day"}
            ],
            "Friday": [
                {"time": "10:00-12:00", "activity": "Week-end review and consolidation"},
                {"time": "14:00-16:00", "activity": "Finish outstanding assignments"},
                {"time": "Evening", "activity": "Social/personal time"}
            ],
            "Saturday": [
                {"time": "Morning", "activity": "Personal time / errands"},
                {"time": "14:00-17:00", "activity": "Major project work (optional)"},
                {"time": "Evening", "activity": "Social activities"}
            ],
            "Sunday": [
                {"time": "Morning", "activity": "Church/spiritual activities"},
                {"time": "Afternoon", "activity": "Rest and reflection"},
                {"time": "Evening", "activity": "Plan upcoming week"}
            ]
        }
        
        return {
            "success": True,
            "schedule": schedule,
            "principles": [
                "Study 2-3 hours outside class for every 1 hour in class",
                "Take 10-minute breaks every 50 minutes (Pomodoro technique)",
                "Study hardest subjects when you're most alert",
                "Keep Sundays for rest and spiritual renewal when possible",
                "Build in buffer time for unexpected events"
            ]
        }
    
    def _prioritize_deadlines(self) -> Dict[str, Any]:
        """Help prioritize assignments and deadlines"""
        return {
            "success": True,
            "prioritization_matrix": {
                "Urgent & Important": [
                    "Due within 48 hours",
                    "Exams this week",
                    "Major project deadlines"
                ],
                "Important but Not Urgent": [
                    "Due next week",
                    "Study for future exams",
                    "Reading assignments",
                    "Long-term projects"
                ],
                "Urgent but Not Important": [
                    "Minor quizzes",
                    "Discussion posts",
                    "Administrative tasks"
                ],
                "Neither Urgent nor Important": [
                    "Extra credit (low value)",
                    "Optional readings"
                ]
            },
            "strategy": "Focus on Important tasks first, whether urgent or not. This prevents crisis mode.",
            "tool_recommendation": "Use Learning Suite's calendar + Google Calendar for deadline tracking"
        }
    
    def _anti_procrastination_advice(self) -> Dict[str, Any]:
        """Provide strategies to combat procrastination"""
        return {
            "success": True,
            "strategies": [
                "2-Minute Rule: If it takes less than 2 minutes, do it now",
                "Break large tasks into 15-minute chunks",
                "Start with the easiest part to build momentum",
                "Use the 'Pomodoro Technique': 25 min work, 5 min break",
                "Study with friends for accountability",
                "Remove distractions: phone in another room, website blockers",
                "Reward yourself after completing tasks",
                "Use the library or study rooms (environment matters)"
            ],
            "byu_resources": [
                "Academic Success Center - study skills coaching",
                "University Tutoring Services - free tutoring",
                "Writing Center - help with papers",
                "Study zones in HBLL - quiet, focused environment"
            ]
        }
    
    def _general_time_management_advice(self) -> Dict[str, Any]:
        """General time management tips"""
        return {
            "success": True,
            "advice": [
                "Use a planner or digital calendar consistently",
                "Plan your week every Sunday evening",
                "Block out class times, work, church, and study time",
                "Protect your sleep - aim for 7-8 hours",
                "Say 'no' to overcommitment - focus on priorities",
                "Build in margin for the unexpected",
                "Use 'dead time' wisely (between classes, waiting, etc.)"
            ]
        }


class SocialConnectionAgent(BaseAgent):
    """Agent for social connections and community building"""
    
    def __init__(self):
        super().__init__(AgentType.SOCIAL, "Social Connection Agent")
        self.capabilities = [
            "study_group_matching",
            "roommate_advice",
            "club_recommendations",
            "social_event_suggestions",
            "networking_guidance"
        ]
    
    def process(self, task: Task, student: StudentProfile) -> Dict[str, Any]:
        """Process social connection tasks"""
        self.log(f"Processing social task: {task.description}")
        
        description_lower = task.description.lower()
        
        if "study group" in description_lower:
            return self._find_study_groups(student)
        elif "roommate" in description_lower:
            return self._roommate_advice()
        elif "club" in description_lower or "activity" in description_lower:
            return self._recommend_clubs(student)
        elif "friends" in description_lower or "lonely" in description_lower:
            return self._making_friends_advice()
        else:
            return self._general_social_advice()
    
    def _find_study_groups(self, student: StudentProfile) -> Dict[str, Any]:
        """Help find or form study groups"""
        return {
            "success": True,
            "strategies": [
                "Ask classmates after the first day: 'Want to study together?'",
                "Check Learning Suite - some classes have built-in study groups",
                "Post in class GroupMe/Discord channels",
                "Study in the TMCB/MARB/LSB - find others working on same material",
                "Form groups of 3-5 people for best dynamics"
            ],
            "study_group_tips": [
                "Meet at consistent times/places (e.g., Tu/Th at 2pm in HBLL)",
                "Set clear goals for each session",
                "Teach each other - teaching reinforces learning",
                "Don't just socialize - stay focused",
                "Use video chat (Zoom/Discord) for remote study"
            ],
            "recommended_courses_for_groups": [
                course for course in student.courses_enrolled 
                if any(x in course for x in ["CS", "MATH", "PHSCS", "CHEM"])
            ]
        }
    
    def _roommate_advice(self) -> Dict[str, Any]:
        """Provide roommate relationship guidance"""
        return {
            "success": True,
            "advice": [
                "Have a roommate agreement conversation in first week",
                "Discuss: sleep schedules, cleanliness, guests, noise levels",
                "Be direct but kind when issues arise",
                "Use 'I feel' statements, not accusations",
                "Respect each other's space and property",
                "Plan occasional roommate activities (dinner, games, etc.)",
                "It's okay if you're not best friends - just be respectful"
            ],
            "conflict_resolution": {
                "step_1": "Talk directly to roommate first",
                "step_2": "If unresolved, involve RA or apartment manager",
                "step_3": "If serious issues, contact housing office",
                "resources": "Counseling Center offers roommate mediation"
            }
        }
    
    def _recommend_clubs(self, student: StudentProfile) -> Dict[str, Any]:
        """Recommend clubs and activities"""
        general_clubs = [
            "BYU Creamery on Ninth (tours and ice cream!)",
            "Intramural sports (all skill levels)",
            "Devotionals (Tuesday 11am)",
            "Service clubs (Circle K, Alternative Spring Break)",
            "Cultural clubs (International Student Association, etc.)"
        ]
        
        # Major-specific clubs
        major_clubs = {
            "CS": ["ACM", "Cyber Security Club", "Game Dev Club", "Women in CS"],
            "Engineering": ["ASME", "IEEE", "Society of Women Engineers"],
            "Business": ["Business Society", "Entrepreneurship Club", "Finance Society"],
            "Nursing": ["Nursing Student Association", "Health Professions Club"]
        }
        
        recommended = general_clubs + major_clubs.get(student.major, [])
        
        return {
            "success": True,
            "recommended_clubs": recommended,
            "how_to_find": [
                "Visit clubs.byu.edu for full list",
                "Attend Club Fest at start of semester",
                "Check social media for club accounts",
                "Ask professors about major-related clubs"
            ],
            "advice": "Join 2-3 clubs max in your first year. Quality over quantity!"
        }
    
    def _making_friends_advice(self) -> Dict[str, Any]:
        """Advice for making friends"""
        return {
            "success": True,
            "strategies": [
                "Attend ward/branch activities regularly",
                "Say yes to invitations, even if uncomfortable at first",
                "Sit with different people in the Cougareat each week",
                "Join study groups in your classes",
                "Attend campus devotionals and forums",
                "Strike up conversations in line, bus, library",
                "Invite others to activities YOU enjoy",
                "Be patient - meaningful friendships take time"
            ],
            "places_to_meet_people": [
                "Your ward/branch (church community)",
                "Classes and study groups",
                "Club meetings and activities",
                "Intramural sports teams",
                "Service projects",
                "Campus employment",
                "Residence halls and apartments"
            ],
            "reminder": "Everyone is looking for friends. Be brave and reach out!"
        }
    
    def _general_social_advice(self) -> Dict[str, Any]:
        """General social guidance"""
        return {
            "success": True,
            "advice": [
                "Balance social life with academics - both are important",
                "Quality relationships matter more than quantity",
                "Stay connected with family - call home regularly",
                "Be yourself - authentic friendships are best",
                "Look for friends who share your values",
                "Don't compare your social life to others' social media",
                "Get involved on campus - don't isolate in your apartment"
            ]
        }


class ResourceFinderAgent(BaseAgent):
    """Agent for finding campus resources and services"""
    
    def __init__(self):
        super().__init__(AgentType.RESOURCE_FINDER, "Resource Finder Agent")
        self.capabilities = [
            "tutoring_services",
            "counseling_services",
            "career_services",
            "health_services",
            "financial_aid"
        ]
        self._load_resources()
    
    def _load_resources(self):
        """Load campus resource information"""
        self.knowledge_base = {
            "academic_resources": {
                "University Tutoring": {
                    "location": "HBLL 2nd floor",
                    "services": "Free tutoring for most courses",
                    "website": "tutoring.byu.edu",
                    "cost": "Free"
                },
                "Writing Center": {
                    "location": "HBLL 3rd floor",
                    "services": "Help with papers and writing",
                    "website": "writingcenter.byu.edu",
                    "cost": "Free"
                },
                "Academic Success Center": {
                    "location": "HBLL 2nd floor",
                    "services": "Study skills, time management coaching",
                    "website": "academicsuccess.byu.edu",
                    "cost": "Free"
                }
            },
            "health_wellness": {
                "Student Health Center": {
                    "location": "Heritage Halls",
                    "services": "Medical care, immunizations",
                    "phone": "801-422-5156",
                    "cost": "Copays apply"
                },
                "Counseling Center": {
                    "location": "1500 WSC",
                    "services": "Mental health counseling",
                    "website": "caps.byu.edu",
                    "cost": "Free for students"
                },
                "Health Promotion": {
                    "location": "Student Health Center",
                    "services": "Wellness education, stress management",
                    "website": "health.byu.edu",
                    "cost": "Free"
                }
            },
            "career_financial": {
                "Career Services": {
                    "location": "2500 WSC",
                    "services": "Internships, resumes, career counseling",
                    "website": "careers.byu.edu",
                    "cost": "Free"
                },
                "Financial Aid": {
                    "location": "D-159 ASB",
                    "services": "Scholarships, grants, loans, work-study",
                    "website": "financialaid.byu.edu",
                    "cost": "Free counseling"
                }
            },
            "spiritual": {
                "Campus Ministry": {
                    "services": "Spiritual support, devotionals",
                    "website": "religion.byu.edu"
                },
                "Chaplain Services": {
                    "services": "Confidential spiritual guidance",
                    "location": "Contact through Counseling Center"
                }
            }
        }
    
    def process(self, task: Task, student: StudentProfile) -> Dict[str, Any]:
        """Process resource-finding tasks"""
        self.log(f"Processing resource finding task: {task.description}")
        
        description_lower = task.description.lower()
        
        if any(word in description_lower for word in ["tutor", "help", "academic"]):
            return self._academic_resources()
        elif any(word in description_lower for word in ["counseling", "mental", "stress", "anxiety"]):
            return self._mental_health_resources()
        elif any(word in description_lower for word in ["career", "job", "internship", "resume"]):
            return self._career_resources()
        elif any(word in description_lower for word in ["money", "financial", "scholarship"]):
            return self._financial_resources()
        elif any(word in description_lower for word in ["health", "sick", "doctor"]):
            return self._health_resources()
        else:
            return self._all_resources()
    
    def _academic_resources(self) -> Dict[str, Any]:
        """Return academic support resources"""
        return {
            "success": True,
            "resources": self.knowledge_base["academic_resources"],
            "pro_tip": "Book tutoring appointments early - spots fill up before exams!"
        }
    
    def _mental_health_resources(self) -> Dict[str, Any]:
        """Return mental health resources"""
        return {
            "success": True,
            "resources": self.knowledge_base["health_wellness"],
            "important": [
                "Counseling Center is FREE for all students",
                "All sessions are completely confidential",
                "No judgment - everyone needs support sometimes",
                "Crisis line available 24/7: 801-422-5156",
                "You can also text 'BYU' to 741741 for crisis support"
            ],
            "common_issues": [
                "Homesickness and adjustment",
                "Academic stress and anxiety",
                "Depression",
                "Relationship concerns",
                "Family issues",
                "Identity and purpose questions"
            ]
        }
    
    def _career_resources(self) -> Dict[str, Any]:
        """Return career development resources"""
        return {
            "success": True,
            "resources": self.knowledge_base["career_financial"],
            "first_year_priorities": [
                "Create a LinkedIn profile",
                "Build a resume (even with limited experience)",
                "Explore different career paths in your major",
                "Attend career fairs (fall and winter semester)",
                "Consider an on-campus job for experience",
                "Start thinking about internships for next summer"
            ]
        }
    
    def _financial_resources(self) -> Dict[str, Any]:
        """Return financial aid resources"""
        return {
            "success": True,
            "resources": self.knowledge_base["career_financial"],
            "financial_tips": [
                "File FAFSA every year by priority deadline",
                "Apply for BYU scholarships through AIM",
                "Look for major-specific scholarships",
                "Consider on-campus employment (work-study)",
                "Budget carefully - use YNAB or Mint apps",
                "Avoid credit card debt",
                "Take advantage of free campus food events"
            ],
            "emergency_funds": "Contact Dean of Students for emergency financial assistance"
        }
    
    def _health_resources(self) -> Dict[str, Any]:
        """Return health services"""
        return {
            "success": True,
            "resources": self.knowledge_base["health_wellness"],
            "health_tips": [
                "Student Health Center is open Mon-Fri",
                "Most visits have small copays ($15-30)",
                "Get flu shots for free in fall semester",
                "Pharmacy on site with student discounts",
                "Urgent care for after-hours issues"
            ]
        }
    
    def _all_resources(self) -> Dict[str, Any]:
        """Return all resources"""
        return {
            "success": True,
            "all_resources": self.knowledge_base,
            "reminder": "All these resources are included in your tuition - use them!"
        }


class WellnessAgent(BaseAgent):
    """Agent for wellness, stress management, and work-life balance"""
    
    def __init__(self):
        super().__init__(AgentType.WELLNESS, "Wellness Agent")
        self.capabilities = [
            "stress_management",
            "sleep_optimization",
            "exercise_planning",
            "spiritual_wellness",
            "work_life_balance"
        ]
    
    def process(self, task: Task, student: StudentProfile) -> Dict[str, Any]:
        """Process wellness-related tasks"""
        self.log(f"Processing wellness task: {task.description}")
        
        description_lower = task.description.lower()
        
        if "stress" in description_lower or "overwhelmed" in description_lower:
            return self._stress_management()
        elif "sleep" in description_lower or "tired" in description_lower:
            return self._sleep_advice()
        elif "exercise" in description_lower or "fitness" in description_lower:
            return self._exercise_guidance()
        elif "spiritual" in description_lower or "faith" in description_lower:
            return self._spiritual_wellness()
        else:
            return self._holistic_wellness_plan()
    
    def _stress_management(self) -> Dict[str, Any]:
        """Provide stress management strategies"""
        return {
            "success": True,
            "immediate_relief": [
                "Take 10 deep breaths (4 seconds in, 6 seconds out)",
                "Go for a 15-minute walk outside",
                "Talk to a friend or family member",
                "Do something you enjoy for 30 minutes",
                "Physical exercise - even 10 minutes helps"
            ],
            "long_term_strategies": [
                "Regular sleep schedule (7-8 hours)",
                "Daily exercise (even just walking)",
                "Healthy eating (protein, fruits, vegetables)",
                "Social connection - don't isolate",
                "Spiritual practices (prayer, scripture study, meditation)",
                "Time management - prevent crisis mode",
                "Say 'no' to overcommitment"
            ],
            "when_to_seek_help": [
                "Stress interfering with daily life",
                "Feeling hopeless or depressed",
                "Can't sleep or eating problems",
                "Thoughts of self-harm",
                "Constant anxiety or panic attacks"
            ],
            "byu_resources": "Counseling Center (caps.byu.edu) - Free and confidential"
        }
    
    def _sleep_advice(self) -> Dict[str, Any]:
        """Provide sleep optimization guidance"""
        return {
            "success": True,
            "sleep_schedule": {
                "target": "7-8 hours per night",
                "bedtime": "Consistent time, even weekends",
                "wake_time": "Consistent wake time (use alarm)"
            },
            "sleep_hygiene": [
                "No screens 1 hour before bed (blue light disrupts sleep)",
                "Keep bedroom cool (65-68°F ideal)",
                "Use bedroom only for sleep (not studying)",
                "Avoid caffeine after 2pm",
                "No heavy meals 3 hours before bed",
                "Wind-down routine: reading, journaling, prayer",
                "Use blackout curtains or sleep mask",
                "White noise or earplugs if needed"
            ],
            "myths": {
                "I can catch up on weekends": "False - consistent schedule is key",
                "I'll sleep when I'm dead": "False - sleep is essential for learning and health",
                "All-nighters help me study": "False - sleep consolidates memory"
            },
            "real_talk": "You'll perform better on tests well-rested than sleep-deprived. Prioritize sleep!"
        }
    
    def _exercise_guidance(self) -> Dict[str, Any]:
        """Provide exercise recommendations"""
        return {
            "success": True,
            "minimum_target": "150 minutes moderate exercise per week (30 min x 5 days)",
            "easy_options": [
                "Walk/bike to campus instead of driving",
                "Use the stairs instead of elevators",
                "Walk between classes (don't just sit)",
                "Study walk with friends",
                "Lunchtime walks around campus"
            ],
            "byu_facilities": {
                "Student Fitness Center": {
                    "location": "Richards Building",
                    "cost": "Free with student ID",
                    "offerings": "Weights, cardio, climbing wall, classes"
                },
                "Intramural Sports": {
                    "offerings": "Basketball, soccer, volleyball, flag football, etc.",
                    "cost": "Small team fee",
                    "benefit": "Exercise + social connection"
                },
                "Group Fitness Classes": {
                    "offerings": "Yoga, spin, HIIT, dance, etc.",
                    "cost": "Free or low cost",
                    "schedule": "Check recsports.byu.edu"
                }
            },
            "benefits": [
                "Reduces stress and anxiety",
                "Improves focus and memory",
                "Better sleep quality",
                "More energy throughout day",
                "Social connections",
                "Better mood"
            ],
            "tip": "Find something you ENJOY - you'll actually stick with it!"
        }
    
    def _spiritual_wellness(self) -> Dict[str, Any]:
        """Provide spiritual wellness guidance"""
        return {
            "success": True,
            "spiritual_practices": [
                "Personal scripture study (even 10 minutes daily)",
                "Personal prayer (morning and evening)",
                "Attend ward/branch meetings",
                "Temple attendance (weekly or monthly)",
                "Devotionals (Tuesday 11am in Marriott Center)",
                "Religion classes (count toward graduation!)",
                "Spiritual reflection and journaling"
            ],
            "spiritual_balance": {
                "tip": "Spiritual foundations help with academic pressure",
                "reality": "It's okay if spiritual life isn't perfect - keep trying",
                "community": "Your ward/branch is your support system"
            },
            "byu_opportunities": [
                "Tuesday Devotionals - inspiring speakers",
                "Campus firesides and special events",
                "Service opportunities through various organizations",
                "Religion classes with excellent professors",
                "Temple near campus (Provo City Center)"
            ],
            "struggles": "If you're having a faith crisis or questions, that's normal. Talk to trusted mentors, bishops, or chaplain services."
        }
    
    def _holistic_wellness_plan(self) -> Dict[str, Any]:
        """Comprehensive wellness guidance"""
        return {
            "success": True,
            "wellness_dimensions": {
                "Physical": "Sleep, exercise, nutrition, avoiding harmful substances",
                "Emotional": "Managing stress, expressing feelings, seeking help when needed",
                "Social": "Meaningful relationships, community involvement, communication skills",
                "Intellectual": "Continuous learning, curiosity, critical thinking, creativity",
                "Spiritual": "Purpose, values, faith practices, service to others",
                "Occupational": "Work-life balance, career development, time management"
            },
            "freshman_year_goals": [
                "Establish healthy sleep routine",
                "Build friend network",
                "Find balance between academics and social life",
                "Develop time management skills",
                "Stay physically active",
                "Maintain spiritual practices",
                "Ask for help when struggling"
            ],
            "remember": "College is about growth in ALL areas, not just academics. Take care of yourself!"
        }


class CoordinatorAgent(BaseAgent):
    """Main coordinator that routes tasks to appropriate agents"""
    
    def __init__(self):
        super().__init__(AgentType.COORDINATOR, "Coordinator Agent")
        self.agents = {
            AgentType.ACADEMIC: AcademicPlanningAgent(),
            AgentType.NAVIGATION: CampusNavigationAgent(),
            AgentType.TIME_MANAGEMENT: TimeManagementAgent(),
            AgentType.SOCIAL: SocialConnectionAgent(),
            AgentType.RESOURCE_FINDER: ResourceFinderAgent(),
            AgentType.WELLNESS: WellnessAgent(),
        }
    
    def route_task(self, task: Task) -> AgentType:
        """Determine which agent should handle the task"""
        description_lower = task.description.lower()
        
        # Academic keywords
        if any(word in description_lower for word in 
               ["course", "class", "schedule", "prerequisite", "major", "degree", "register", "credits"]):
            return AgentType.ACADEMIC
        
        # Navigation keywords
        elif any(word in description_lower for word in 
                 ["building", "find", "location", "parking", "navigate", "walk", "food", "eat"]):
            return AgentType.NAVIGATION
        
        # Time management keywords
        elif any(word in description_lower for word in 
                 ["time", "deadline", "assignment", "study schedule", "procrastination", "plan"]):
            return AgentType.TIME_MANAGEMENT
        
        # Social keywords
        elif any(word in description_lower for word in 
                 ["study group", "friends", "roommate", "club", "activity", "social", "lonely"]):
            return AgentType.SOCIAL
        
        # Resource keywords
        elif any(word in description_lower for word in 
                 ["tutor", "counseling", "career", "job", "health", "financial", "resource", "help"]):
            return AgentType.RESOURCE_FINDER
        
        # Wellness keywords
        elif any(word in description_lower for word in 
                 ["stress", "sleep", "exercise", "wellness", "spiritual", "overwhelmed", "balance"]):
            return AgentType.WELLNESS
        
        # Default to resource finder for general help
        else:
            return AgentType.RESOURCE_FINDER
    
    def process(self, task: Task, student: StudentProfile) -> Dict[str, Any]:
        """Route task to appropriate agent and process"""
        self.log(f"Routing task: {task.description}")
        
        # Determine which agent should handle this
        agent_type = self.route_task(task)
        task.assigned_agent = agent_type
        
        # Get the appropriate agent
        agent = self.agents[agent_type]
        
        # Process the task
        self.log(f"Assigned to {agent.name}")
        result = agent.process(task, student)
        
        task.status = "completed"
        task.result = result
        
        return result


class BYUFreshmanAssistant:
    """Main assistant system that coordinates all agents"""
    
    def __init__(self, student: StudentProfile):
        self.student = student
        self.coordinator = CoordinatorAgent()
        self.task_queue = []
        self.completed_tasks = []
    
    def add_task(self, description: str, priority: Priority = Priority.MEDIUM) -> Task:
        """Add a new task to the system"""
        task = Task(
            id=f"task_{len(self.task_queue) + len(self.completed_tasks) + 1}",
            description=description,
            priority=priority
        )
        self.task_queue.append(task)
        return task
    
    def process_next_task(self) -> Optional[Dict[str, Any]]:
        """Process the next task in the queue"""
        if not self.task_queue:
            return None
        
        # Sort by priority
        self.task_queue.sort(key=lambda t: t.priority.value, reverse=True)
        
        # Get highest priority task
        task = self.task_queue.pop(0)
        
        # Process it
        result = self.coordinator.process(task, self.student)
        
        # Move to completed
        self.completed_tasks.append(task)
        
        return result
    
    def process_all_tasks(self) -> List[Dict[str, Any]]:
        """Process all tasks in the queue"""
        results = []
        while self.task_queue:
            result = self.process_next_task()
            if result:
                results.append(result)
        return results
    
    def ask(self, question: str, priority: Priority = Priority.MEDIUM) -> Dict[str, Any]:
        """Ask the assistant a question (convenience method)"""
        task = self.add_task(question, priority)
        return self.process_next_task()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the student's situation and recommendations"""
        print(f"\n{'='*60}")
        print(f"BYU FRESHMAN ASSISTANT - Summary for {self.student.name}")
        print(f"{'='*60}\n")
        
        summary = {
            "student": {
                "name": self.student.name,
                "major": self.student.major,
                "credits": self.student.credits_completed,
                "courses": self.student.courses_enrolled
            },
            "top_recommendations": []
        }
        
        # Get recommendations from each agent
        print("Generating personalized recommendations...\n")
        
        # Academic
        academic_task = Task(
            id="summary_academic",
            description="general academic advice",
            priority=Priority.HIGH,
            assigned_agent=AgentType.ACADEMIC
        )
        academic_result = self.coordinator.agents[AgentType.ACADEMIC].process(academic_task, self.student)
        summary["top_recommendations"].append({
            "category": "Academic",
            "advice": academic_result.get("advice", [])[:3]
        })
        
        # Time Management
        time_task = Task(
            id="summary_time",
            description="general time management advice",
            priority=Priority.HIGH,
            assigned_agent=AgentType.TIME_MANAGEMENT
        )
        time_result = self.coordinator.agents[AgentType.TIME_MANAGEMENT].process(time_task, self.student)
        summary["top_recommendations"].append({
            "category": "Time Management",
            "advice": time_result.get("advice", [])[:3]
        })
        
        # Wellness
        wellness_task = Task(
            id="summary_wellness",
            description="holistic wellness",
            priority=Priority.HIGH,
            assigned_agent=AgentType.WELLNESS
        )
        wellness_result = self.coordinator.agents[AgentType.WELLNESS].process(wellness_task, self.student)
        summary["top_recommendations"].append({
            "category": "Wellness",
            "advice": [
                "Get 7-8 hours of sleep consistently",
                "Exercise 30 minutes, 5 days per week",
                "Maintain spiritual practices daily"
            ]
        })
        
        # Social
        social_task = Task(
            id="summary_social",
            description="general social advice",
            priority=Priority.HIGH,
            assigned_agent=AgentType.SOCIAL
        )
        social_result = self.coordinator.agents[AgentType.SOCIAL].process(social_task, self.student)
        summary["top_recommendations"].append({
            "category": "Social",
            "advice": social_result.get("advice", [])[:3]
        })
        
        return summary


def print_result(result: Dict[str, Any], title: str = "Result"):
    """Pretty print a result"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")
    print(json.dumps(result, indent=2, default=str))
    print()


def main():
    """Demo the BYU Freshman Assistant"""
    
    print("\n" + "="*80)
    print(" "*20 + "BYU FRESHMAN ASSISTANT")
    print(" "*15 + "Agentic Workflow System Demo")
    print("="*80 + "\n")
    
    # Create a sample student profile
    student = StudentProfile(
        name="Sarah Johnson",
        major="CS",
        credits_completed=0,
        preferred_study_times=["morning", "afternoon"],
        interests=["programming", "music", "hiking"],
        courses_enrolled=["CS 111", "MATH 112", "WRTG 150"],
        goals=["Get good grades", "Make friends", "Stay healthy"]
    )
    
    print(f"Student Profile:")
    print(f"  Name: {student.name}")
    print(f"  Major: {student.major}")
    print(f"  Enrolled Courses: {', '.join(student.courses_enrolled)}")
    print(f"  Goals: {', '.join(student.goals)}\n")
    
    # Create the assistant
    assistant = BYUFreshmanAssistant(student)
    
    # Demo various use cases
    print("\n" + "-"*80)
    print("DEMO: Common Freshman Questions")
    print("-"*80 + "\n")
    
    questions = [
        ("What courses should I take next semester?", Priority.HIGH),
        ("How do I find my classes on campus?", Priority.MEDIUM),
        ("I'm feeling overwhelmed with assignments", Priority.URGENT),
        ("How can I find a study group?", Priority.MEDIUM),
        ("Where can I get help with my math homework?", Priority.HIGH),
        ("I'm having trouble sleeping", Priority.MEDIUM),
    ]
    
    for question, priority in questions:
        print(f"\n📝 QUESTION: {question}")
        print(f"   Priority: {priority.name}\n")
        result = assistant.ask(question, priority)
        print(json.dumps(result, indent=2, default=str))
        print("\n" + "-"*80)
    
    # Generate comprehensive summary
    print("\n\n" + "="*80)
    print("GENERATING PERSONALIZED SUMMARY AND RECOMMENDATIONS")
    print("="*80)
    
    summary = assistant.get_summary()
    
    print("\n📊 TOP RECOMMENDATIONS FOR SUCCESS:\n")
    for rec in summary["top_recommendations"]:
        print(f"\n{rec['category'].upper()}:")
        for i, advice in enumerate(rec['advice'], 1):
            print(f"  {i}. {advice}")
    
    print("\n\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print("\nThe BYU Freshman Assistant uses multiple specialized agents to help")
    print("first-year students navigate academic, social, and personal challenges.")
    print("\nEach agent has domain expertise and works together through the")
    print("coordinator to provide comprehensive, personalized support.")
    print("\n")


if __name__ == "__main__":
    main()

