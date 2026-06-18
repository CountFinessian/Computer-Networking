"""
BYU-Specific Data and Knowledge Base
Contains real information about BYU campus, resources, and services
"""

# Complete building database with coordinates (for future navigation features)
BYU_BUILDINGS = {
    # Academic Buildings - North Campus
    "TMCB": {
        "name": "Talmage Math & Computer Science Building",
        "location": "North Campus",
        "coordinates": (40.2518, -111.6493),
        "parking": ["Lot 34", "Lot 26"],
        "departments": ["Computer Science", "Mathematics", "Statistics"],
        "facilities": ["Computer labs", "Study rooms", "Auditoriums"],
        "hours": "6:00 AM - 12:00 AM"
    },
    "ESC": {
        "name": "Eyring Science Center",
        "location": "North Campus",
        "coordinates": (40.2496, -111.6485),
        "parking": ["Lot 34"],
        "departments": ["Chemistry", "Biochemistry", "Physics"],
        "facilities": ["Labs", "Lecture halls"],
        "hours": "7:00 AM - 10:00 PM"
    },
    "CB": {
        "name": "Clyde Building",
        "location": "North Campus",
        "coordinates": (40.2507, -111.6502),
        "parking": ["Lot 34"],
        "departments": ["Engineering", "Technology"],
        "facilities": ["Machine shops", "Labs"],
        "hours": "7:00 AM - 10:00 PM"
    },
    
    # Academic Buildings - Central Campus
    "MARB": {
        "name": "Marriott School of Business",
        "location": "Central Campus",
        "coordinates": (40.2490, -111.6519),
        "parking": ["Lot 45", "Lot 16"],
        "departments": ["Business", "Accounting", "Management"],
        "facilities": ["Study rooms", "Career center", "Auditoriums"],
        "hours": "6:00 AM - 11:00 PM"
    },
    "HBLL": {
        "name": "Harold B. Lee Library",
        "location": "Central Campus",
        "coordinates": (40.2494, -111.6490),
        "parking": ["Lot 16", "Lot 45"],
        "departments": ["Library Services"],
        "facilities": [
            "Study rooms (individual and group)",
            "Computer labs",
            "Tutoring center (2nd floor)",
            "Writing center (3rd floor)",
            "Media center",
            "Special collections"
        ],
        "hours": "24/7 during semester (some floors have restricted hours)"
    },
    "WILK": {
        "name": "Wilkinson Student Center",
        "location": "Central Campus",
        "coordinates": (40.2511, -111.6497),
        "parking": ["Lot 16"],
        "departments": ["Student Life"],
        "facilities": [
            "Cougareat (food court)",
            "Bookstore",
            "Study lounges",
            "Game room",
            "Ballrooms",
            "Meeting rooms"
        ],
        "hours": "6:00 AM - 12:00 AM"
    },
    "JSB": {
        "name": "Joseph Smith Building",
        "location": "Central Campus",
        "coordinates": (40.2523, -111.6513),
        "parking": ["Lot 16"],
        "departments": ["Religion", "Ancient Scripture"],
        "facilities": ["Classrooms", "Auditorium"],
        "hours": "7:00 AM - 10:00 PM"
    },
    
    # Academic Buildings - East Campus
    "LSB": {
        "name": "Life Sciences Building",
        "location": "East Campus",
        "coordinates": (40.2486, -111.6471),
        "parking": ["Lot 22", "Lot 23"],
        "departments": ["Biology", "Microbiology", "Neuroscience"],
        "facilities": ["Labs", "Museum of Paleontology", "Greenhouses"],
        "hours": "7:00 AM - 10:00 PM"
    },
    "BNSN": {
        "name": "Benson Science Building",
        "location": "East Campus",
        "coordinates": (40.2479, -111.6474),
        "parking": ["Lot 22"],
        "departments": ["Geology", "Physics & Astronomy"],
        "facilities": ["Planetarium", "Labs", "Lecture halls"],
        "hours": "7:00 AM - 10:00 PM"
    },
    
    # Other Important Buildings
    "SWKT": {
        "name": "Spencer W. Kimball Tower",
        "location": "South Campus",
        "coordinates": (40.2458, -111.6490),
        "parking": ["Lot 43"],
        "departments": ["Languages", "Linguistics", "Humanities"],
        "facilities": ["Language labs", "Classrooms"],
        "hours": "7:00 AM - 10:00 PM"
    },
    "RB": {
        "name": "Richards Building (Student Fitness Center)",
        "location": "North Campus",
        "coordinates": (40.2535, -111.6503),
        "parking": ["Lot 26"],
        "departments": ["Recreation Services"],
        "facilities": [
            "Weight room",
            "Cardio equipment",
            "Rock climbing wall",
            "Swimming pool",
            "Racquetball courts",
            "Group fitness rooms"
        ],
        "hours": "5:30 AM - 11:00 PM (varies by area)"
    },
    "MC": {
        "name": "Marriott Center",
        "location": "North Campus",
        "coordinates": (40.2533, -111.6519),
        "parking": ["Lot 26", "Lot 41"],
        "departments": ["Athletics", "Events"],
        "facilities": ["Arena", "Sports facilities"],
        "hours": "Event-dependent",
        "notes": "Tuesday devotionals at 11:00 AM"
    }
}

# Dining options with detailed information
DINING_OPTIONS = {
    "Cougareat": {
        "location": "WILK Ground Floor",
        "type": "Food Court",
        "hours": {
            "Monday-Friday": "7:00 AM - 8:00 PM",
            "Saturday": "11:00 AM - 5:00 PM",
            "Sunday": "Closed"
        },
        "options": [
            "Subway",
            "Chick-fil-A",
            "Pizza",
            "Asian cuisine",
            "Grill items",
            "Salad bar"
        ],
        "payment": ["Dining Plus", "Credit/Debit", "Cash"],
        "price_range": "$5-$10"
    },
    "Legends Grille": {
        "location": "WILK 2nd Floor",
        "type": "Sit-down restaurant",
        "hours": {
            "Monday-Friday": "11:00 AM - 8:00 PM",
            "Saturday": "Closed",
            "Sunday": "Closed"
        },
        "specialty": "Burgers, sandwiches, appetizers",
        "payment": ["Dining Plus", "Credit/Debit"],
        "price_range": "$8-$15"
    },
    "Skyroom": {
        "location": "WILK 6th Floor",
        "type": "Fine dining",
        "hours": {
            "Monday-Friday": "11:00 AM - 2:00 PM",
            "Saturday": "Closed",
            "Sunday": "Closed"
        },
        "specialty": "Buffet with rotating menu",
        "payment": ["Dining Plus", "Credit/Debit"],
        "price_range": "$12-$18",
        "note": "Great city views!"
    },
    "Cannon Commons": {
        "location": "Heritage Halls",
        "type": "Dining Hall",
        "hours": {
            "Monday-Friday": "7:00 AM - 8:00 PM",
            "Saturday": "9:00 AM - 6:00 PM",
            "Sunday": "10:00 AM - 6:00 PM"
        },
        "payment": ["Meal plan", "Dining Plus"],
        "price_range": "$8-$12"
    },
    "On-Campus Quick Options": {
        "BYU Creamery": {"location": "North end of campus", "specialty": "Ice cream, cheese"},
        "Underground Shops": {"location": "HBLL", "specialty": "Snacks, drinks, sandwiches"},
        "Jamba Juice": {"location": "MARB", "specialty": "Smoothies"},
        "Einstein Bros": {"location": "Various", "specialty": "Bagels, coffee"}
    }
}

# Comprehensive resource directory
CAMPUS_RESOURCES = {
    "academic_support": {
        "University Tutoring Services": {
            "location": "HBLL 2nd Floor, Room 2160",
            "phone": "801-422-5770",
            "email": "tutoring@byu.edu",
            "website": "tutoring.byu.edu",
            "services": [
                "Free peer tutoring for 100-300 level courses",
                "Individual and group sessions",
                "Walk-in and appointment options",
                "Online tutoring available"
            ],
            "hours": "Monday-Thursday: 9 AM - 9 PM, Friday: 9 AM - 5 PM",
            "cost": "Free"
        },
        "Writing Center": {
            "location": "HBLL 3rd Floor, Room 3340",
            "phone": "801-422-4499",
            "email": "writingcenter@byu.edu",
            "website": "writingcenter.byu.edu",
            "services": [
                "One-on-one tutoring for any writing project",
                "Help at any stage (brainstorming to final edits)",
                "30 or 60-minute appointments",
                "Online and in-person options"
            ],
            "hours": "Monday-Thursday: 9 AM - 9 PM, Friday: 9 AM - 5 PM",
            "cost": "Free"
        },
        "Academic Success Center": {
            "location": "HBLL 2nd Floor",
            "phone": "801-422-3925",
            "website": "academicsuccess.byu.edu",
            "services": [
                "Study skills coaching",
                "Time management strategies",
                "Test-taking strategies",
                "Learning assessments",
                "Workshops on various topics"
            ],
            "cost": "Free"
        },
        "Math Lab": {
            "location": "TMCB 223",
            "website": "math.byu.edu/home/mathlab",
            "services": ["Drop-in tutoring for math courses"],
            "hours": "Monday-Friday: various hours",
            "cost": "Free"
        }
    },
    
    "health_wellness": {
        "Counseling and Psychological Services (CAPS)": {
            "location": "1500 WSC",
            "phone": "801-422-3035",
            "crisis_line": "801-422-5156 (24/7)",
            "website": "caps.byu.edu",
            "services": [
                "Individual counseling (8-10 sessions free)",
                "Group counseling",
                "Crisis services",
                "Psychiatric services",
                "Workshops and outreach programs",
                "Completely confidential"
            ],
            "hours": "Monday-Friday: 8 AM - 5 PM",
            "crisis_support": "24/7 phone support available",
            "cost": "Free for students"
        },
        "Student Health Center": {
            "location": "1853 North Canyon Road (near Heritage Halls)",
            "phone": "801-422-5156",
            "website": "health.byu.edu",
            "services": [
                "Primary care",
                "Urgent care",
                "Immunizations",
                "Lab services",
                "Pharmacy",
                "Physical therapy",
                "Women's health"
            ],
            "hours": "Monday-Friday: 8 AM - 5 PM",
            "urgent_care": "Monday-Friday: 8 AM - 5 PM, Saturday: 9 AM - 1 PM",
            "cost": "Copays range $15-$50 depending on service"
        },
        "Health Promotion": {
            "website": "health.byu.edu/health-promotion",
            "services": [
                "Wellness education",
                "Stress management programs",
                "Sleep improvement programs",
                "Nutrition counseling",
                "Substance abuse prevention"
            ],
            "cost": "Free"
        }
    },
    
    "career_financial": {
        "University Career Services": {
            "location": "2500 WSC",
            "phone": "801-422-3035",
            "email": "careers@byu.edu",
            "website": "careers.byu.edu",
            "services": [
                "Career counseling and exploration",
                "Resume and cover letter review",
                "Mock interviews",
                "Career fairs (Fall and Winter)",
                "Internship database",
                "Job search strategies",
                "LinkedIn profile optimization",
                "Networking workshops"
            ],
            "hours": "Monday-Friday: 8 AM - 5 PM",
            "cost": "Free"
        },
        "Financial Aid Office": {
            "location": "D-159 ASB (Abraham Smoot Building)",
            "phone": "801-422-4104",
            "email": "financialaid@byu.edu",
            "website": "financialaid.byu.edu",
            "services": [
                "FAFSA assistance",
                "Scholarship applications",
                "Grants and loans",
                "Work-study programs",
                "Financial literacy counseling",
                "Emergency funds"
            ],
            "hours": "Monday-Friday: 8 AM - 5 PM",
            "cost": "Free counseling"
        }
    },
    
    "student_life": {
        "Dean of Students": {
            "location": "3200 WSC",
            "phone": "801-422-2731",
            "website": "deanofstudents.byu.edu",
            "services": [
                "Student advocacy",
                "Crisis intervention",
                "Emergency financial assistance",
                "Food pantry (Cougar Cupboard)",
                "Student concerns and complaints"
            ]
        },
        "Housing Office": {
            "location": "1450 WSC",
            "phone": "801-422-1511",
            "website": "housing.byu.edu",
            "services": [
                "On-campus housing",
                "Approved off-campus housing",
                "Roommate conflicts",
                "Housing contracts"
            ]
        }
    },
    
    "spiritual": {
        "University Chaplain": {
            "contact": "Through CAPS (801-422-3035)",
            "services": [
                "Confidential spiritual support",
                "Faith questions and concerns",
                "Interfaith dialogue",
                "Connection to campus ministry"
            ],
            "cost": "Free"
        },
        "Campus Devotionals": {
            "location": "Marriott Center",
            "time": "Tuesday, 11:00 AM",
            "website": "devotional.byu.edu",
            "description": "Weekly devotional addresses by Church leaders, faculty, and guest speakers"
        }
    }
}

# Common major requirements and typical freshman courses
MAJOR_PATHWAYS = {
    "Computer Science": {
        "department": "Computer Science",
        "college": "Physical and Mathematical Sciences",
        "total_credits": 120,
        "freshman_year": {
            "Fall": [
                {"course": "CS 111", "name": "Introduction to Computer Science", "credits": 3},
                {"course": "MATH 112", "name": "Calculus 1", "credits": 4},
                {"course": "WRTG 150", "name": "Writing & Rhetoric", "credits": 3},
                {"course": "Religion", "name": "Book of Mormon or New Testament", "credits": 2},
                {"course": "GE", "name": "General Education Elective", "credits": 3}
            ],
            "Winter": [
                {"course": "CS 142", "name": "Introduction to Computer Programming", "credits": 3},
                {"course": "MATH 113", "name": "Calculus 2", "credits": 4},
                {"course": "ENGL 316 or GE", "name": "Technical Communication or GE", "credits": 3},
                {"course": "Religion", "name": "Foundations of Restoration", "credits": 2},
                {"course": "GE", "name": "General Education Elective", "credits": 3}
            ]
        },
        "key_prerequisites": {
            "CS 142": ["CS 111"],
            "CS 235": ["CS 142", "MATH 112"],
            "CS 236": ["CS 235"],
        },
        "advice": [
            "Math is critical - stay current with calculus",
            "Start building projects outside of class",
            "Join ACM or other CS clubs",
            "Begin looking for internships after freshman year"
        ]
    },
    
    "Mechanical Engineering": {
        "department": "Mechanical Engineering",
        "college": "Ira A. Fulton College of Engineering",
        "total_credits": 128,
        "freshman_year": {
            "Fall": [
                {"course": "ENGR 101", "name": "Engineering Design", "credits": 2},
                {"course": "CHEM 105", "name": "General Chemistry", "credits": 3},
                {"course": "MATH 112", "name": "Calculus 1", "credits": 4},
                {"course": "WRTG 150", "name": "Writing & Rhetoric", "credits": 3},
                {"course": "Religion", "name": "Book of Mormon", "credits": 2}
            ],
            "Winter": [
                {"course": "CHEM 106", "name": "General Chemistry II", "credits": 3},
                {"course": "MATH 113", "name": "Calculus 2", "credits": 4},
                {"course": "PHSCS 121", "name": "Physics 1", "credits": 3},
                {"course": "GE", "name": "General Education", "credits": 3},
                {"course": "Religion", "name": "New Testament", "credits": 2}
            ]
        },
        "advice": [
            "Engineering is demanding - manage your time well",
            "Form study groups early",
            "Use tutoring services for math and physics",
            "Get involved with engineering clubs and competitions"
        ]
    },
    
    "Business Management": {
        "department": "Management",
        "college": "Marriott School of Business",
        "total_credits": 120,
        "freshman_year": {
            "Fall": [
                {"course": "ECON 110", "name": "Economic Principles and Problems", "credits": 3},
                {"course": "MATH 119", "name": "Calculus for Business", "credits": 3},
                {"course": "WRTG 150", "name": "Writing & Rhetoric", "credits": 3},
                {"course": "Religion", "name": "Book of Mormon", "credits": 2},
                {"course": "GE", "name": "General Education", "credits": 3}
            ],
            "Winter": [
                {"course": "ACC 200", "name": "Financial Accounting", "credits": 3},
                {"course": "MATH 121", "name": "Business Statistics", "credits": 3},
                {"course": "GE", "name": "American Heritage", "credits": 3},
                {"course": "Religion", "name": "New Testament", "credits": 2},
                {"course": "GE", "name": "General Education", "credits": 3}
            ]
        },
        "advice": [
            "Apply to the Marriott School by end of sophomore year",
            "Maintain good GPA - admission is competitive",
            "Get involved in business clubs",
            "Start networking early"
        ]
    },
    
    "Nursing": {
        "department": "Nursing",
        "college": "College of Nursing",
        "total_credits": 120,
        "freshman_year": {
            "Fall": [
                {"course": "CHEM 105", "name": "General Chemistry", "credits": 3},
                {"course": "BIO 100", "name": "Principles of Biology", "credits": 3},
                {"course": "WRTG 150", "name": "Writing & Rhetoric", "credits": 3},
                {"course": "NDFS 100", "name": "Food and Nutrition", "credits": 2},
                {"course": "Religion", "name": "Book of Mormon", "credits": 2}
            ],
            "Winter": [
                {"course": "CHEM 106 or 107", "name": "General/Organic Chemistry", "credits": 3},
                {"course": "NURS 104", "name": "Lifespan Human Development", "credits": 3},
                {"course": "STAT 121", "name": "Statistics", "credits": 3},
                {"course": "Religion", "name": "New Testament", "credits": 2},
                {"course": "GE", "name": "General Education", "credits": 3}
            ]
        },
        "advice": [
            "Nursing program is very competitive",
            "Excel in prerequisite courses",
            "Gain healthcare experience (CNA certification)",
            "Apply to nursing program sophomore year"
        ]
    }
}

# General Education Requirements
GE_REQUIREMENTS = {
    "first_year_writing": {
        "required": ["WRTG 150"],
        "credits": 3,
        "description": "First-Year Writing"
    },
    "advanced_writing": {
        "options": ["WRTG 316", "ENGL 316", "TMA 316"],
        "credits": 3,
        "description": "Advanced Writing"
    },
    "american_heritage": {
        "options": ["HIST 202", "POLI 202"],
        "credits": 3,
        "description": "American Heritage"
    },
    "civilization": {
        "options": ["Various CIV courses", "Area studies"],
        "credits": 3-4,
        "description": "Civilization courses"
    },
    "languages": {
        "credits": 8,
        "description": "8 credits of a single language (or demonstrate proficiency)"
    },
    "letters": {
        "credits": 3,
        "description": "Literature, philosophy, or comparative arts"
    },
    "religion": {
        "credits": 14,
        "description": "Religion courses (typically 2 credits each)"
    }
}

# Important dates and deadlines (academic year template)
ACADEMIC_CALENDAR_TEMPLATE = {
    "Fall_Semester": {
        "registration": "March (priority by credits)",
        "first_day": "Early September",
        "add_drop": "First 2 weeks",
        "midterms": "Mid-October",
        "withdrawal_deadline": "Mid-November",
        "finals": "Mid-December",
        "breaks": ["Labor Day", "Fall Break (1 day mid-October)", "Thanksgiving (week)"]
    },
    "Winter_Semester": {
        "registration": "October (priority by credits)",
        "first_day": "Early January",
        "add_drop": "First 2 weeks",
        "midterms": "Mid-February",
        "withdrawal_deadline": "Early April",
        "finals": "Mid-April",
        "breaks": ["MLK Day", "Presidents' Day"]
    },
    "Spring_Term": {
        "note": "Optional half-semester",
        "duration": "May - June",
        "benefits": "Catch up or get ahead"
    },
    "Summer_Term": {
        "note": "Optional half-semester",
        "duration": "July - August",
        "benefits": "Lighter course load"
    }
}

# Transportation options
TRANSPORTATION = {
    "UVX": {
        "name": "Utah Valley Express",
        "cost": "Free with student ID",
        "route": "Orem to Provo, stops at BYU",
        "frequency": "Every 10-15 minutes during peak times",
        "hours": "Early morning to late evening",
        "website": "rideuta.com"
    },
    "Campus_Shuttle": {
        "name": "BYU Campus Shuttle",
        "cost": "Free",
        "routes": ["North Campus Loop", "South Campus Loop", "Apartment complexes"],
        "hours": "7 AM - 11 PM (varies by route)",
        "tracking": "BYU Mobile App"
    },
    "Parking": {
        "Y_Lot": {"type": "Commuter", "cost": "$110/year", "location": "North end of campus"},
        "A_Permit": {"type": "Reserved", "cost": "$300+/year", "location": "Designated lots"},
        "Evening": {"type": "Free", "time": "After 5 PM", "location": "Most lots"},
        "Visitor": {"type": "Paid", "cost": "$2/hour", "location": "Visitor lots"}
    },
    "Biking": {
        "bike_share": "None currently active",
        "parking": "Bike racks throughout campus",
        "note": "Campus is very bike-friendly"
    }
}

# Tips and strategies for success
SUCCESS_STRATEGIES = {
    "academic": [
        "Attend class - most important factor in success",
        "Read syllabus carefully and note all deadlines",
        "Sit near the front - better focus and engagement",
        "Take handwritten notes - improves retention",
        "Review notes within 24 hours of class",
        "Form study groups early in semester",
        "Start assignments early - don't procrastinate",
        "Use office hours - professors want to help",
        "Learn from returned assignments and exams",
        "Balance hard and easy courses each semester"
    ],
    "time_management": [
        "Use a planner or digital calendar religiously",
        "Block study time like you block class time",
        "Study 2-3 hours outside class per 1 hour in class",
        "Use time between classes productively",
        "Establish a consistent sleep schedule",
        "Learn to say no to overcommitment",
        "Build in buffer time for unexpected events",
        "Take real breaks - rest is productive"
    ],
    "social": [
        "Go to ward activities - automatic social network",
        "Join 2-3 clubs that match your interests",
        "Say yes to social invitations (within reason)",
        "Initiate plans - don't always wait for others",
        "Balance social life with academics",
        "Find your community - it takes time",
        "Stay in touch with family and home friends",
        "Be yourself - authentic relationships last"
    ],
    "spiritual": [
        "Make Sunday a day of rest and renewal",
        "Consistent daily scripture study (even 10 min)",
        "Attend ward regularly - builds community",
        "Go to the temple regularly",
        "Attend Tuesday devotionals when possible",
        "Take religion classes - count toward degree",
        "Serve others - gets you out of your head",
        "Be patient with spiritual growth"
    ],
    "wellness": [
        "Sleep 7-8 hours consistently",
        "Exercise regularly - even 30 min helps",
        "Eat balanced meals - avoid only ramen",
        "Limit social media and screen time",
        "Get outside - Utah has amazing nature",
        "Ask for help when struggling",
        "Practice stress management techniques",
        "Maintain hobbies and fun activities"
    ],
    "financial": [
        "Create and stick to a budget",
        "Apply for scholarships every year",
        "Consider on-campus employment",
        "Avoid unnecessary debt",
        "Cook meals instead of eating out",
        "Take advantage of free campus resources",
        "File FAFSA annually by priority deadline",
        "Plan for study abroad or internship costs"
    ]
}

# Common freshman challenges and solutions
COMMON_CHALLENGES = {
    "homesickness": {
        "description": "Missing home, family, and friends from before college",
        "solutions": [
            "Stay connected - call/video chat regularly",
            "Create new routines and traditions",
            "Get involved on campus - builds new connections",
            "Give it time - usually improves after first month",
            "Visit home occasionally but not every weekend",
            "Bring familiar items to make room feel like home"
        ],
        "when_to_seek_help": "If it persists beyond first 2 months or interferes with daily life"
    },
    
    "academic_adjustment": {
        "description": "College courses are harder and faster-paced than high school",
        "solutions": [
            "Start with appropriate course load (14-15 credits)",
            "Use tutoring and academic support services",
            "Study differently - can't just memorize",
            "Form study groups",
            "Go to office hours",
            "Learn time management and study skills"
        ],
        "resources": ["University Tutoring", "Academic Success Center", "Writing Center"]
    },
    
    "time_management": {
        "description": "Overwhelmed by balancing classes, work, social life, church",
        "solutions": [
            "Use calendar/planner consistently",
            "Set priorities - can't do everything",
            "Learn to say no",
            "Build study time into schedule",
            "Avoid overcommitment first semester",
            "Take advantage of time management workshops"
        ],
        "resources": ["Academic Success Center workshops"]
    },
    
    "roommate_conflicts": {
        "description": "Disagreements or tension with roommates",
        "solutions": [
            "Communicate directly and kindly",
            "Set clear expectations early",
            "Use 'I feel' statements, not accusations",
            "Compromise when possible",
            "Involve RA if direct communication doesn't work",
            "Remember: you don't have to be best friends"
        ],
        "resources": ["RA", "Housing Office", "Counseling Center for mediation"]
    },
    
    "making_friends": {
        "description": "Difficulty finding friends or social connections",
        "solutions": [
            "Attend ward activities regularly",
            "Join clubs related to your interests",
            "Form study groups in classes",
            "Say yes to invitations",
            "Initiate plans yourself",
            "Be patient - meaningful friendships take time",
            "Put yourself out there - everyone feels awkward"
        ],
        "reminder": "Everyone is in the same boat freshman year"
    },
    
    "choosing_major": {
        "description": "Uncertainty about major or career path",
        "solutions": [
            "Explore through GE requirements",
            "Talk to professors and advisors",
            "Visit University Career Services",
            "Try different intro classes",
            "Don't rush - it's okay to be undecided",
            "Consider internships or job shadowing",
            "Most students change majors - that's normal"
        ],
        "resources": ["University Career Services", "Academic Advisors", "Career assessments"]
    },
    
    "financial_stress": {
        "description": "Worried about paying for school or living expenses",
        "solutions": [
            "Meet with Financial Aid Office",
            "Apply for scholarships through AIM",
            "Consider on-campus employment",
            "Create and follow a budget",
            "Look for free food events on campus",
            "Apply for emergency funds if needed",
            "File FAFSA every year"
        ],
        "resources": ["Financial Aid Office", "Dean of Students (emergency funds)"]
    },
    
    "mental_health": {
        "description": "Feeling depressed, anxious, or overwhelmed",
        "solutions": [
            "Reach out to Counseling Center - it's free",
            "Talk to trusted friends, family, or bishop",
            "Maintain healthy routines (sleep, exercise, eating)",
            "Reduce course load if needed",
            "Text crisis line: BYU to 741741",
            "Remember: seeking help is strength, not weakness"
        ],
        "resources": ["CAPS (caps.byu.edu)", "Crisis line: 801-422-5156 (24/7)"],
        "when_to_seek_help_immediately": [
            "Thoughts of self-harm or suicide",
            "Unable to function in daily life",
            "Severe panic attacks",
            "Substance abuse"
        ]
    }
}


def get_building_info(building_code: str) -> dict:
    """Get information about a specific building"""
    return BYU_BUILDINGS.get(building_code.upper(), {})


def get_dining_options(meal_type: str = None) -> dict:
    """Get dining options, optionally filtered by meal type"""
    return DINING_OPTIONS


def get_resources_by_category(category: str) -> dict:
    """Get resources in a specific category"""
    return CAMPUS_RESOURCES.get(category, {})


def get_major_info(major: str) -> dict:
    """Get information about a specific major"""
    for major_name, info in MAJOR_PATHWAYS.items():
        if major.lower() in major_name.lower():
            return info
    return {}

