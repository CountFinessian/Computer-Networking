"""
Example scenarios demonstrating the BYU Freshman Assistant
Shows how the agentic system handles various real-world freshman situations
"""

from byu_freshman_assistant import (
    BYUFreshmanAssistant,
    StudentProfile,
    Priority
)
import json


def print_scenario(title, description):
    """Print a scenario header"""
    print("\n" + "="*90)
    print(f"📖 SCENARIO: {title}")
    print("="*90)
    print(f"\n{description}\n")
    print("-"*90)


def print_response(result):
    """Pretty print agent response"""
    print("\n🤖 ASSISTANT RESPONSE:\n")
    print(json.dumps(result, indent=2, default=str))
    print("\n" + "-"*90)


def scenario_1_overwhelmed_freshman():
    """Scenario: Student feeling overwhelmed with first semester"""
    
    print_scenario(
        "The Overwhelmed Freshman",
        """
        Meet Jake: He's 3 weeks into his first semester at BYU. He's enrolled in 17 credits
        including CS 111, MATH 112, CHEM 105, and WRTG 150. He's struggling to keep up with
        assignments, hasn't made many friends yet, and is feeling homesick. He's not sure where
        to start getting help.
        """
    )
    
    jake = StudentProfile(
        name="Jake Thompson",
        major="CS",
        credits_completed=0,
        courses_enrolled=["CS 111", "MATH 112", "CHEM 105", "WRTG 150", "REL 121"],
        interests=["video games", "basketball"],
        goals=["Get good grades", "Make friends", "Don't fail"]
    )
    
    assistant = BYUFreshmanAssistant(jake)
    
    # Problem 1: Academic overwhelm
    print("\n💬 Jake: 'I have so many assignments and I don't know how to manage them all.'")
    result1 = assistant.ask("Help me prioritize my deadlines and create a study schedule", Priority.URGENT)
    print_response(result1)
    
    input("\nPress Enter to continue...")
    
    # Problem 2: Social isolation
    print("\n💬 Jake: 'I feel lonely and haven't really connected with anyone yet.'")
    result2 = assistant.ask("How do I make friends at BYU?", Priority.HIGH)
    print_response(result2)
    
    input("\nPress Enter to continue...")
    
    # Problem 3: Academic support
    print("\n💬 Jake: 'I'm really struggling with chemistry. Where can I get help?'")
    result3 = assistant.ask("I need tutoring for chemistry", Priority.HIGH)
    print_response(result3)
    
    print("\n✅ OUTCOME: Jake now has a clear action plan:")
    print("   • Time management strategies and a weekly schedule")
    print("   • Specific ways to meet people (ward, study groups, clubs)")
    print("   • Free tutoring resources in ESC and HBLL")


def scenario_2_career_exploration():
    """Scenario: Student unsure about major and career path"""
    
    print_scenario(
        "The Undecided Explorer",
        """
        Meet Emily: She's interested in both biology and business, but isn't sure which path
        to pursue. She's worried about making the wrong choice and wants to explore both options
        while still making progress toward a degree.
        """
    )
    
    emily = StudentProfile(
        name="Emily Rodriguez",
        major="Undecided",
        credits_completed=12,
        courses_enrolled=["BIO 100", "ECON 110", "MATH 112"],
        interests=["science", "entrepreneurship", "helping people"],
        goals=["Choose the right major", "Explore careers", "Stay on track to graduate"]
    )
    
    assistant = BYUFreshmanAssistant(emily)
    
    print("\n💬 Emily: 'How can I explore different majors without falling behind?'")
    result1 = assistant.ask("Help me choose between majors and plan my courses", Priority.HIGH)
    print_response(result1)
    
    input("\nPress Enter to continue...")
    
    print("\n💬 Emily: 'I want to learn about career options in these fields.'")
    result2 = assistant.ask("Where can I get career counseling and explore job options?", Priority.MEDIUM)
    print_response(result2)
    
    print("\n✅ OUTCOME: Emily now has:")
    print("   • Course plan that keeps options open")
    print("   • Connection to University Career Services")
    print("   • Strategies for exploring both fields")


def scenario_3_mental_health_crisis():
    """Scenario: Student experiencing mental health challenges"""
    
    print_scenario(
        "The Struggling Student",
        """
        Meet David: He's dealing with severe anxiety and depression. He's missing classes,
        not eating well, and feeling hopeless. He needs immediate support but doesn't know
        where to turn or if he can afford counseling.
        """
    )
    
    david = StudentProfile(
        name="David Chen",
        major="Mechanical Engineering",
        credits_completed=15,
        courses_enrolled=["ENGR 201", "MATH 113", "PHSCS 121"],
        interests=["robotics", "music"],
        goals=["Just survive", "Feel better", "Not drop out"]
    )
    
    assistant = BYUFreshmanAssistant(david)
    
    print("\n💬 David: 'I'm really struggling. I feel overwhelmed and hopeless.'")
    result = assistant.ask("I need help with stress and anxiety. I think I need counseling.", Priority.URGENT)
    print_response(result)
    
    print("\n✅ OUTCOME: David learns that:")
    print("   • CAPS offers FREE counseling (completely confidential)")
    print("   • Crisis line available 24/7: 801-422-5156")
    print("   • Text support: BYU to 741741")
    print("   • He's not alone - 60% of freshmen experience high stress")
    print("   • Seeking help is strength, not weakness")
    
    print("\n⚠️  IMPORTANT: The system recognizes this as URGENT and prioritizes")
    print("     immediate mental health resources over other suggestions.")


def scenario_4_time_management_success():
    """Scenario: Student wanting to optimize their college experience"""
    
    print_scenario(
        "The Proactive Planner",
        """
        Meet Sophia: She's doing well academically but wants to optimize her time to get
        involved in more activities, maintain wellness, and still excel in her studies.
        She wants to make the most of her BYU experience.
        """
    )
    
    sophia = StudentProfile(
        name="Sophia Martinez",
        major="Business Management",
        credits_completed=15,
        courses_enrolled=["ACC 200", "ECON 110", "WRTG 150", "MATH 119"],
        interests=["leadership", "service", "fitness", "music"],
        goals=["4.0 GPA", "Lead a club", "Stay healthy", "Serve others"]
    )
    
    assistant = BYUFreshmanAssistant(sophia)
    
    print("\n💬 Sophia: 'I want to get involved in campus life. What clubs should I join?'")
    result1 = assistant.ask("What clubs and activities should I join for my major?", Priority.MEDIUM)
    print_response(result1)
    
    input("\nPress Enter to continue...")
    
    print("\n💬 Sophia: 'How can I balance academics, activities, and personal wellness?'")
    result2 = assistant.ask("Help me create a balanced schedule with study, activities, and wellness", Priority.HIGH)
    print_response(result2)
    
    input("\nPress Enter to continue...")
    
    print("\n💬 Sophia: 'I want to prepare for internships next year.'")
    result3 = assistant.ask("How do I prepare for business internships?", Priority.MEDIUM)
    print_response(result3)
    
    print("\n✅ OUTCOME: Sophia receives:")
    print("   • Specific business clubs and activities to join")
    print("   • A balanced weekly schedule template")
    print("   • Career preparation roadmap")
    print("   • Wellness strategies to maintain high performance")


def scenario_5_practical_navigation():
    """Scenario: Student needing practical campus navigation help"""
    
    print_scenario(
        "The Lost Freshman",
        """
        Meet Marcus: It's his first week and he keeps getting lost on campus. He has back-to-back
        classes in different buildings and isn't sure if he'll make it between them. He also
        doesn't know where to eat or park.
        """
    )
    
    marcus = StudentProfile(
        name="Marcus Johnson",
        major="CS",
        credits_completed=0,
        courses_enrolled=["CS 111", "MATH 112", "WRTG 150"],
        interests=["programming", "gaming"],
        goals=["Not be late to class", "Find good food", "Figure out campus"]
    )
    
    assistant = BYUFreshmanAssistant(marcus)
    
    print("\n💬 Marcus: 'Where is the TMCB building and how do I get there from the MARB?'")
    result1 = assistant.ask("Where is TMCB building and how long to walk from MARB?", Priority.MEDIUM)
    print_response(result1)
    
    input("\nPress Enter to continue...")
    
    print("\n💬 Marcus: 'Where can I eat on campus?'")
    result2 = assistant.ask("Where can I get food on campus?", Priority.LOW)
    print_response(result2)
    
    input("\nPress Enter to continue...")
    
    print("\n💬 Marcus: 'Where should I park?'")
    result3 = assistant.ask("Where can I park on campus?", Priority.LOW)
    print_response(result3)
    
    print("\n✅ OUTCOME: Marcus now knows:")
    print("   • Building locations and walking times")
    print("   • All dining options with hours and prices")
    print("   • Parking lots and permit information")
    print("   • To download the BYU Mobile app for navigation")


def scenario_6_comprehensive_summary():
    """Demonstrate the personalized summary feature"""
    
    print_scenario(
        "Comprehensive Check-In",
        """
        At the end of the first month, a student can get a comprehensive summary of
        recommendations across all areas of college life. This helps ensure they're
        not missing important resources or strategies.
        """
    )
    
    student = StudentProfile(
        name="Alex Rivera",
        major="CS",
        credits_completed=14,
        courses_enrolled=["CS 142", "MATH 113", "PHSCS 121", "REL 122"],
        interests=["coding", "soccer", "music"],
        goals=["Excel academically", "Make lasting friendships", "Stay healthy"]
    )
    
    assistant = BYUFreshmanAssistant(student)
    
    print("\n💬 Alex: 'Can you give me a comprehensive check-in on how I'm doing?'")
    print("\n🤖 Generating comprehensive summary...\n")
    
    summary = assistant.get_summary()
    
    print(f"{'='*90}")
    print(f"COMPREHENSIVE SUMMARY FOR {summary['student']['name']}")
    print(f"{'='*90}\n")
    
    print(f"📚 Major: {summary['student']['major']}")
    print(f"📖 Credits: {summary['student']['credits']}")
    print(f"📝 Courses: {', '.join(summary['student']['courses'])}")
    
    for rec in summary['top_recommendations']:
        print(f"\n🎯 {rec['category'].upper()}")
        print("-" * 70)
        for i, advice in enumerate(rec['advice'], 1):
            print(f"  {i}. {advice}")
    
    print("\n✅ OUTCOME: Alex receives personalized guidance across all six areas")
    print("   of college life, ensuring holistic support and success.")


def main():
    """Run all example scenarios"""
    
    print("\n" + "="*90)
    print(" "*25 + "BYU FRESHMAN ASSISTANT")
    print(" "*20 + "EXAMPLE SCENARIOS & USE CASES")
    print("="*90)
    
    print("\n📚 This demo shows how the agentic system handles real freshman situations.")
    print("   Each scenario demonstrates different agents working together to help.")
    
    input("\nPress Enter to start...")
    
    # Run scenarios
    scenario_1_overwhelmed_freshman()
    input("\n\nPress Enter for next scenario...")
    
    scenario_2_career_exploration()
    input("\n\nPress Enter for next scenario...")
    
    scenario_3_mental_health_crisis()
    input("\n\nPress Enter for next scenario...")
    
    scenario_4_time_management_success()
    input("\n\nPress Enter for next scenario...")
    
    scenario_5_practical_navigation()
    input("\n\nPress Enter for next scenario...")
    
    scenario_6_comprehensive_summary()
    
    # Final summary
    print("\n\n" + "="*90)
    print("DEMO COMPLETE - KEY TAKEAWAYS")
    print("="*90)
    
    print("\n✨ The BYU Freshman Assistant demonstrates:")
    print("   1. Multi-agent architecture with specialized expertise")
    print("   2. Priority-based task routing (urgent mental health → immediate resources)")
    print("   3. Personalized recommendations based on major, interests, goals")
    print("   4. Comprehensive BYU knowledge base (buildings, resources, services)")
    print("   5. Holistic support (academic, social, wellness, spiritual)")
    print("   6. Proactive guidance (preventing problems before they occur)")
    
    print("\n🎯 Real-World Impact:")
    print("   • Reduces time spent finding resources (agents know where everything is)")
    print("   • Improves mental health outcomes (quick access to support)")
    print("   • Increases academic success (tutoring, time management, study strategies)")
    print("   • Enhances social integration (clubs, study groups, friend-making)")
    print("   • Promotes holistic wellness (sleep, exercise, spiritual balance)")
    
    print("\n🚀 Future Enhancements Could Include:")
    print("   • Integration with Learning Suite for real deadline tracking")
    print("   • SMS/Discord bot for quick questions and reminders")
    print("   • AI-powered study group matching")
    print("   • Predictive analytics to identify at-risk students")
    print("   • Connection to actual BYU APIs for live data")
    
    print("\n💡 This is more than a chatbot - it's a comprehensive support system")
    print("   that helps BYU freshmen thrive in every aspect of college life.")
    
    print("\n" + "="*90)
    print("Thanks for exploring the BYU Freshman Assistant!")
    print("Go Cougars! 🏈")
    print("="*90 + "\n")


if __name__ == "__main__":
    main()

