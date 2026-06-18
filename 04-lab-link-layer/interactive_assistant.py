"""
Interactive BYU Freshman Assistant
Command-line interface for interacting with the agentic assistant system
"""

import sys
from byu_freshman_assistant import (
    BYUFreshmanAssistant,
    StudentProfile,
    Priority
)
import json


class InteractiveAssistant:
    """Interactive command-line interface for the assistant"""
    
    def __init__(self):
        self.assistant = None
        self.student = None
        
    def clear_screen(self):
        """Clear the terminal screen"""
        print("\n" * 50)  # Simple cross-platform approach
    
    def print_header(self):
        """Print a nice header"""
        print("\n" + "="*80)
        print(" "*25 + "BYU FRESHMAN ASSISTANT")
        print(" "*20 + "Your Personal College Success Guide")
        print("="*80 + "\n")
    
    def create_student_profile(self):
        """Interactive student profile creation"""
        print("\n📝 Let's create your student profile!\n")
        
        name = input("What's your name? ").strip()
        
        print("\nWhat's your major? Choose or type your own:")
        print("  1. Computer Science (CS)")
        print("  2. Mechanical Engineering")
        print("  3. Business Management")
        print("  4. Nursing")
        print("  5. Other")
        
        major_choice = input("\nEnter number or major name: ").strip()
        major_map = {
            "1": "CS",
            "2": "Mechanical Engineering",
            "3": "Business Management",
            "4": "Nursing"
        }
        major = major_map.get(major_choice, major_choice if major_choice != "5" else input("Enter your major: "))
        
        courses = []
        print("\n📚 What courses are you enrolled in? (Enter one per line, empty line when done)")
        while True:
            course = input("  Course: ").strip()
            if not course:
                break
            courses.append(course)
        
        interests = []
        print("\n🎨 What are your interests/hobbies? (Enter one per line, empty line when done)")
        while True:
            interest = input("  Interest: ").strip()
            if not interest:
                break
            interests.append(interest)
        
        goals = []
        print("\n🎯 What are your goals for this year? (Enter one per line, empty line when done)")
        while True:
            goal = input("  Goal: ").strip()
            if not goal:
                break
            goals.append(goal)
        
        self.student = StudentProfile(
            name=name,
            major=major,
            credits_completed=0,
            preferred_study_times=["morning", "afternoon"],
            interests=interests if interests else ["learning"],
            courses_enrolled=courses if courses else [],
            goals=goals if goals else ["succeed in college"]
        )
        
        self.assistant = BYUFreshmanAssistant(self.student)
        
        print(f"\n✅ Profile created! Welcome to BYU, {name}! 🎉\n")
    
    def print_menu(self):
        """Print the main menu"""
        print("\n" + "-"*80)
        print("MAIN MENU")
        print("-"*80)
        print("\n📋 What can I help you with today?\n")
        print("  1. 📚 Academic Planning (courses, schedules, degree progress)")
        print("  2. 🗺️  Campus Navigation (find buildings, parking, dining)")
        print("  3. ⏰ Time Management (schedules, deadlines, productivity)")
        print("  4. 👥 Social Connections (study groups, friends, clubs)")
        print("  5. 🏥 Campus Resources (tutoring, counseling, career services)")
        print("  6. 💪 Wellness & Balance (stress, sleep, exercise, spiritual)")
        print("  7. 💬 Ask a Custom Question")
        print("  8. 📊 Get Personalized Summary")
        print("  9. 👤 View/Edit Student Profile")
        print("  0. 🚪 Exit")
        print()
    
    def handle_academic(self):
        """Handle academic planning queries"""
        print("\n📚 ACADEMIC PLANNING")
        print("-"*60)
        print("What would you like to know?")
        print("  1. What courses should I take?")
        print("  2. Help me plan my schedule")
        print("  3. Check my degree progress")
        print("  4. Learn about prerequisites")
        print("  5. General academic advice")
        print("  6. Custom question")
        
        choice = input("\nChoice: ").strip()
        
        questions = {
            "1": "What courses should I take next semester?",
            "2": "Help me plan my course schedule",
            "3": "What is my degree progress?",
            "4": "What prerequisites do I need?",
            "5": "Give me general academic advice"
        }
        
        question = questions.get(choice, input("Your question: "))
        result = self.assistant.ask(question, Priority.HIGH)
        self.print_result(result)
    
    def handle_navigation(self):
        """Handle campus navigation queries"""
        print("\n🗺️  CAMPUS NAVIGATION")
        print("-"*60)
        print("What do you need help with?")
        print("  1. Find a building")
        print("  2. Parking information")
        print("  3. Where to eat on campus")
        print("  4. Plan route between classes")
        print("  5. Custom question")
        
        choice = input("\nChoice: ").strip()
        
        questions = {
            "1": "Where is " + input("Building code (e.g., TMCB): "),
            "2": "Where can I park on campus?",
            "3": "Where can I eat on campus?",
            "4": "How do I plan routes between my classes?",
        }
        
        question = questions.get(choice, input("Your question: "))
        result = self.assistant.ask(question, Priority.MEDIUM)
        self.print_result(result)
    
    def handle_time_management(self):
        """Handle time management queries"""
        print("\n⏰ TIME MANAGEMENT")
        print("-"*60)
        print("What would you like help with?")
        print("  1. Create a study schedule")
        print("  2. Help with assignment deadlines")
        print("  3. Stop procrastinating")
        print("  4. General time management tips")
        print("  5. Custom question")
        
        choice = input("\nChoice: ").strip()
        
        questions = {
            "1": "Help me create a study schedule",
            "2": "Help me prioritize my deadlines",
            "3": "How do I stop procrastinating?",
            "4": "Give me time management advice"
        }
        
        question = questions.get(choice, input("Your question: "))
        result = self.assistant.ask(question, Priority.HIGH)
        self.print_result(result)
    
    def handle_social(self):
        """Handle social connection queries"""
        print("\n👥 SOCIAL CONNECTIONS")
        print("-"*60)
        print("What do you need help with?")
        print("  1. Find/form study groups")
        print("  2. Make friends")
        print("  3. Roommate advice")
        print("  4. Find clubs and activities")
        print("  5. Custom question")
        
        choice = input("\nChoice: ").strip()
        
        questions = {
            "1": "How do I find study groups?",
            "2": "How do I make friends at BYU?",
            "3": "I'm having roommate issues",
            "4": "What clubs should I join?"
        }
        
        question = questions.get(choice, input("Your question: "))
        result = self.assistant.ask(question, Priority.MEDIUM)
        self.print_result(result)
    
    def handle_resources(self):
        """Handle campus resources queries"""
        print("\n🏥 CAMPUS RESOURCES")
        print("-"*60)
        print("What resources do you need?")
        print("  1. Tutoring and academic help")
        print("  2. Mental health/counseling")
        print("  3. Career services")
        print("  4. Financial aid")
        print("  5. Health services")
        print("  6. All available resources")
        print("  7. Custom question")
        
        choice = input("\nChoice: ").strip()
        
        questions = {
            "1": "Where can I get tutoring help?",
            "2": "I need counseling support",
            "3": "Help me with career planning",
            "4": "I need financial aid information",
            "5": "Where is the health center?",
            "6": "Show me all campus resources"
        }
        
        question = questions.get(choice, input("Your question: "))
        result = self.assistant.ask(question, Priority.HIGH)
        self.print_result(result)
    
    def handle_wellness(self):
        """Handle wellness queries"""
        print("\n💪 WELLNESS & BALANCE")
        print("-"*60)
        print("What do you need help with?")
        print("  1. I'm feeling stressed")
        print("  2. Sleep problems")
        print("  3. Exercise and fitness")
        print("  4. Spiritual wellness")
        print("  5. Overall wellness plan")
        print("  6. Custom question")
        
        choice = input("\nChoice: ").strip()
        
        questions = {
            "1": "I'm feeling stressed and overwhelmed",
            "2": "Help me sleep better",
            "3": "How do I exercise at BYU?",
            "4": "Help with spiritual wellness",
            "5": "Create a wellness plan for me"
        }
        
        question = questions.get(choice, input("Your question: "))
        result = self.assistant.ask(question, Priority.URGENT if choice == "1" else Priority.HIGH)
        self.print_result(result)
    
    def handle_custom_question(self):
        """Handle custom user questions"""
        print("\n💬 ASK A CUSTOM QUESTION")
        print("-"*60)
        question = input("What's your question? ").strip()
        
        if not question:
            print("No question entered.")
            return
        
        print("\nHow urgent is this?")
        print("  1. Low priority")
        print("  2. Medium priority")
        print("  3. High priority")
        print("  4. Urgent")
        
        priority_choice = input("Priority (default: Medium): ").strip()
        priority_map = {
            "1": Priority.LOW,
            "2": Priority.MEDIUM,
            "3": Priority.HIGH,
            "4": Priority.URGENT
        }
        priority = priority_map.get(priority_choice, Priority.MEDIUM)
        
        result = self.assistant.ask(question, priority)
        self.print_result(result)
    
    def handle_summary(self):
        """Generate and display personalized summary"""
        print("\n📊 GENERATING PERSONALIZED SUMMARY...")
        print("-"*60)
        
        summary = self.assistant.get_summary()
        
        print(f"\n👤 Student: {summary['student']['name']}")
        print(f"📚 Major: {summary['student']['major']}")
        print(f"📖 Credits: {summary['student']['credits']}")
        if summary['student']['courses']:
            print(f"📝 Current Courses: {', '.join(summary['student']['courses'])}")
        
        print(f"\n{'='*80}")
        print("TOP RECOMMENDATIONS FOR YOUR SUCCESS")
        print(f"{'='*80}")
        
        for rec in summary['top_recommendations']:
            print(f"\n🎯 {rec['category'].upper()}")
            print("-" * 60)
            for i, advice in enumerate(rec['advice'], 1):
                print(f"  {i}. {advice}")
    
    def handle_profile(self):
        """View and edit student profile"""
        print("\n👤 STUDENT PROFILE")
        print("-"*60)
        print(f"Name: {self.student.name}")
        print(f"Major: {self.student.major}")
        print(f"Credits: {self.student.credits_completed}")
        print(f"Courses: {', '.join(self.student.courses_enrolled) if self.student.courses_enrolled else 'None'}")
        print(f"Interests: {', '.join(self.student.interests) if self.student.interests else 'None'}")
        print(f"Goals: {', '.join(self.student.goals) if self.student.goals else 'None'}")
        
        print("\nWould you like to update any information? (y/n)")
        if input().strip().lower() == 'y':
            print("\nWhat would you like to update?")
            print("  1. Major")
            print("  2. Add courses")
            print("  3. Update goals")
            print("  4. Nothing")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "1":
                new_major = input("New major: ").strip()
                if new_major:
                    self.student.major = new_major
                    print("✅ Major updated!")
            
            elif choice == "2":
                print("Enter courses (one per line, empty line when done):")
                while True:
                    course = input("  Course: ").strip()
                    if not course:
                        break
                    if course not in self.student.courses_enrolled:
                        self.student.courses_enrolled.append(course)
                print("✅ Courses updated!")
            
            elif choice == "3":
                print("Enter new goals (one per line, empty line when done):")
                new_goals = []
                while True:
                    goal = input("  Goal: ").strip()
                    if not goal:
                        break
                    new_goals.append(goal)
                if new_goals:
                    self.student.goals = new_goals
                    print("✅ Goals updated!")
    
    def print_result(self, result: dict):
        """Pretty print a result"""
        print("\n" + "="*80)
        print("RESPONSE")
        print("="*80 + "\n")
        
        # Format JSON nicely
        formatted = json.dumps(result, indent=2, default=str)
        
        # Make it more readable
        formatted = formatted.replace('"success": true', '✅ Success')
        formatted = formatted.replace('"success": false', '❌ Not Found')
        
        print(formatted)
        
        print("\n" + "="*80)
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main run loop"""
        self.clear_screen()
        self.print_header()
        
        print("Welcome! Let's get you set up with your personalized assistant.\n")
        self.create_student_profile()
        
        while True:
            self.print_menu()
            choice = input("Enter your choice (0-9): ").strip()
            
            if choice == "0":
                print("\n✨ Thanks for using BYU Freshman Assistant!")
                print("Good luck with your college journey! Go Cougars! 🏈\n")
                break
            
            elif choice == "1":
                self.handle_academic()
            
            elif choice == "2":
                self.handle_navigation()
            
            elif choice == "3":
                self.handle_time_management()
            
            elif choice == "4":
                self.handle_social()
            
            elif choice == "5":
                self.handle_resources()
            
            elif choice == "6":
                self.handle_wellness()
            
            elif choice == "7":
                self.handle_custom_question()
            
            elif choice == "8":
                self.handle_summary()
                input("\nPress Enter to continue...")
            
            elif choice == "9":
                self.handle_profile()
                input("\nPress Enter to continue...")
            
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")


def main():
    """Entry point for interactive assistant"""
    try:
        assistant = InteractiveAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n✨ Thanks for using BYU Freshman Assistant!")
        print("Good luck with your college journey! 🏈\n")
        sys.exit(0)


if __name__ == "__main__":
    main()

