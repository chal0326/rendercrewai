import os
from typing import Dict, Any, Optional, List
from crewai import Agent, Task, Crew
from crewai.process import Process
from crewai.utilities.callbacks import CrewAgentCallbacks

class MusicalTheaterCrew:
    """
    Musical Theater Crew Management System
    
    This class manages the creation and organization of agents and tasks
    for a musical theater production crew.
    """
    
    def __init__(self):
        self.agents = {}
        self.tasks = {}
        self.roles = [
            "Composer + Lyricist",
            "Book",
            "Director",
            "Choreographer",
            "Set/Visual",
            "Dramaturg",
            "Market/Producer"
        ]
        
        self.task_templates = {
            "Composer + Lyricist": [
                ("Compose new songs", "Sheet music and lyrics for all songs"),
                ("Develop musical themes", "Musical motifs for characters and scenes"),
                ("Create vocal arrangements", "Detailed vocal arrangements for ensemble")
            ],
            "Book": [
                ("Draft storyline", "Complete first draft of the book"),
                ("Character development", "Detailed character backgrounds and arcs"),
                ("Scene structure", "Scene-by-scene breakdown with transitions")
            ],
            "Director": [
                ("Review creative inputs", "Provide feedback on creative direction"),
                ("Vision development", "Comprehensive production vision document"),
                ("Staging concepts", "Initial staging plans for key scenes")
            ],
            "Choreographer": [
                ("Develop choreography", "Choreography plans for musical numbers"),
                ("Movement patterns", "Character-specific movement guidelines"),
                ("Dance arrangements", "Dance break arrangements for ensemble numbers")
            ],
            "Set/Visual": [
                ("Design set sketches", "Mood boards and initial sketches"),
                ("Technical requirements", "Technical specifications for set pieces"),
                ("Visual continuity", "Scene transition and visual flow plans")
            ],
            "Dramaturg": [
                ("Check continuity", "A list of suggested storyline adjustments"),
                ("Historical research", "Period-specific reference materials"),
                ("Theme analysis", "Analysis of major themes and motifs")
            ],
            "Market/Producer": [
                ("Analyze market trends", "Market analysis report"),
                ("Budget planning", "Initial budget breakdown"),
                ("Marketing strategy", "Marketing and promotion plan")
            ]
        }

def create_agent_for_role(role: str) -> Agent:
    """
    Create an agent for a specific musical theater role.
    
    Args:
        role: The specific role in the musical theater production
        
    Returns:
        A configured Agent object for the role
    """
    role_descriptions = {
        "Composer + Lyricist": {
            "goal": "Create compelling musical numbers and lyrics that advance the story",
            "backstory": "You are an experienced composer and lyricist with a deep understanding of musical theater conventions and the ability to create memorable melodies and meaningful lyrics."
        },
        "Book": {
            "goal": "Develop a coherent and engaging narrative structure",
            "backstory": "You are a skilled playwright with experience in crafting compelling stories and developing rich characters for musical theater."
        },
        "Director": {
            "goal": "Unify the creative vision and guide the overall production",
            "backstory": "You are a seasoned director with expertise in bringing together various theatrical elements into a cohesive whole."
        },
        "Choreographer": {
            "goal": "Create dynamic movement that enhances the storytelling",
            "backstory": "You are an innovative choreographer who specializes in creating movement that serves both the story and the music."
        },
        "Set/Visual": {
            "goal": "Design compelling visual environments that support the narrative",
            "backstory": "You are a creative designer with experience in creating immersive theatrical environments that enhance storytelling."
        },
        "Dramaturg": {
            "goal": "Ensure historical accuracy and narrative consistency",
            "backstory": "You are a meticulous researcher and story expert who helps maintain the integrity of the production."
        },
        "Market/Producer": {
            "goal": "Develop effective marketing strategies and manage production resources",
            "backstory": "You are an experienced producer with a strong understanding of theater marketing and production management."
        }
    }
    
    role_info = role_descriptions.get(role, {
        "goal": "Contribute to the overall success of the production",
        "backstory": "You are a theater professional with expertise in your specific domain."
    })
    
    return Agent(
        role=role,
        goal=role_info["goal"],
        backstory=role_info["backstory"],
        verbose=True,
        allow_delegation=True
    )

def create_task_for_role(agent: Agent, task_desc: tuple) -> Task:
    """
    Create a task for a specific role.
    
    Args:
        agent: The agent to assign the task to
        task_desc: Tuple containing (description, expected_output)
        
    Returns:
        A configured Task object
    """
    description, expected_output = task_desc
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )

def create_musical_theater_crew(production_name: str) -> Crew:
    """
    Create a crew for a musical theater production.
    
    Args:
        production_name: The name of the musical theater production
        
    Returns:
        A configured Crew object with all necessary agents and tasks
    """
    crew_manager = MusicalTheaterCrew()
    agents = []
    tasks = []
    
    # Create agents and tasks for each role
    for role in crew_manager.roles:
        agent = create_agent_for_role(role)
        agents.append(agent)
        
        # Create tasks for this role
        role_tasks = crew_manager.task_templates.get(role, [])
        for task_desc in role_tasks:
            task = create_task_for_role(agent, task_desc)
            tasks.append(task)
    
    # Create the crew with all agents and tasks
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=2,
        process=Process.sequential,
        callbacks=CrewAgentCallbacks()
    )
    
    return crew

# Example usage (uncomment to test locally):
# if __name__ == "__main__":
#     production_name = "New Musical Production"
#     crew = create_musical_theater_crew(production_name)
#     result = crew.kickoff()
#     print(result)