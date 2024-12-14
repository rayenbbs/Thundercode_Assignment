from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


from src.qa_review.tools.page_accessibility_tool import PageAccessibilityTool
from src.qa_review.tools.page_performance_tool import PagePerformanceTool
from src.qa_review.tools.page_best_practices_tool import PageBestPracticesTool
from src.qa_review.tools.page_seo_tool import PageSEOTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class QaReview():
	"""QaReview crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def pagePerformance_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['pagePerformance_analyzer'],
   			tools=[PagePerformanceTool()],
			verbose=True
		)

	@agent
	def pageAccessibility_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['pageAccessibility_analyzer'],
   			tools=[PageAccessibilityTool()],
			verbose=True
		)
	
	@agent
	def pageBestPractices_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['pageBestPractices_analyzer'],
   			tools=[PageBestPracticesTool()],
			verbose=True
		)
  
	@agent
	def pageSEO_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['pageSEO_analyzer'],
   			tools=[PageSEOTool()],
			verbose=True
		)
  
	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def analyze_web_performance_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_web_performance_task'],
		)
  
	@task
	def analyze_web_accessibility_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_web_accessibility_task'],
		)
  
	@task
	def analyze_web_best_practices_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_web_best_practices_task'],
		)
  
	@task
	def analyze_SEO_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_SEO_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
       		context=[self.analyze_web_performance_task(),self.analyze_web_accessibility_task(),self.analyze_web_best_practices_task(),self.analyze_SEO_task()],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the QaReview crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
