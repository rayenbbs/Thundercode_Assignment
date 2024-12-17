from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.qa_review.tools.page_accessibility_tool import PageAccessibilityTool
from src.qa_review.tools.page_performance_tool import PagePerformanceTool
from src.qa_review.tools.page_best_practices_tool import PageBestPracticesTool
from src.qa_review.tools.page_seo_tool import PageSEOTool
from src.qa_review.tools.page_html_tool import PageHTMLTool
from src.qa_review.tools.page_http_header_tool import PageHTTPHeaderTool


@CrewBase
class QaReview():
	"""QaReview crew"""
 
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	#defining the agents
	@agent
	def pagePerformance_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['pagePerformance_analyzer'],
   			tools=[PagePerformanceTool()], #the tool used by the agent
			verbose=True
		)
  
	
	@agent
	def pageAccessibility_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['pageAccessibility_analyzer'],
   			tools=[PageAccessibilityTool()], #the tool used by the agent
			verbose=True
		)
	
	@agent
	def pageBestPractices_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['pageBestPractices_analyzer'],
   			tools=[PageBestPracticesTool()], #the tool used by the agent
			verbose=True
		)
  
	@agent
	def pageSEO_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['pageSEO_analyzer'],
   			tools=[PageSEOTool()], #the tool used by the agent
			verbose=True
		)
  
	@agent
	def html_content_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['html_content_analyzer'],
   			tools=[PageHTMLTool()], #the tool used by the agent
			verbose=True
		)
  
	@agent
	def web_security_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['web_security_specialist'],
   			tools=[PageHTTPHeaderTool()], #the tool used by the agent
			verbose=True
		)
	
	@agent
	def kpi_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['kpi_extractor'],
		)
  	
  
	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
		)
	#defining the tasks
	@task
	def analyze_web_performance_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_web_performance_task'],
      		async_execution=True, #async for parallel execution
			output_file='outputs/performance_report.md'
		)
  
	@task
	def analyze_web_accessibility_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_web_accessibility_task'],
      		async_execution=True, #async for parallel execution
        	output_file='outputs/accessibility_report.md'
		)
  
	@task
	def analyze_web_best_practices_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_web_best_practices_task'],
   			async_execution=True, #async for parallel execution
			output_file='outputs/best_practices_report.md'
		)
  
	@task
	def analyze_SEO_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_SEO_task'],
			async_execution=True, #async for parallel execution
			output_file='outputs/SEO_report.md'
  		)
  
	@task
	def analyze_html_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_html_task'],
			#async for parallel execution
			async_execution=True,
			output_file='outputs/html_report.md'
		)
  
	@task
	def analyze_http_security_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_http_security_task'],
			#async for parallel execution
			async_execution=True,
			output_file="outputs/security_report.md"
		)

 
	@task
	def generate_kpi_json_task(self) -> Task:
		return Task(
			config=self.tasks_config['generate_kpi_json_task'],
   			#added context so that the output of the other tasks is now accessible for this task.
       		context=[self.analyze_web_performance_task(),self.analyze_web_accessibility_task(),self.analyze_web_best_practices_task(),self.analyze_SEO_task(),self.analyze_html_task(),self.analyze_http_security_task()],
			#JSON file for KPIs
   			output_file='outputs/kpis.json'
		)
 
	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			#added context so that the output of the other tasks is now accessible for this task.
       		context=[self.analyze_web_performance_task(),self.analyze_web_accessibility_task(),self.analyze_web_best_practices_task(),self.analyze_SEO_task(),self.analyze_html_task(),self.analyze_http_security_task(),self.generate_kpi_json_task()],
			output_file='outputs/report.md'
		)
  
  
	#defining the crew
	@crew
	def crew(self) -> Crew:
		"""Creates the QaReview crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential, #Sequential because the process is simple and doesn't necessitate dynamic allocation of tasks
			verbose=True,
		)
