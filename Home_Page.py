import streamlit as st  					#pip install streamlit
import requests								# pip install requests
from streamlit_lottie import st_lottie		# pip install streamlit-lotti

def load_lottieurl(url: str):
	'''
	Function to generate animations on the interface using streamlit_lottie
	Parameters :
	url 	url of the animation
	'''
	r = requests.get(url)

	if r.status_code != 200:
		return None

	return r.json()


# Setup for page configuration in local streamlit application
st.set_page_config(
	page_title = 'Fatigue Measurements',
	layout = 'wide'
	)



# Defining containers for headings, features, navigation
# Containers and columns are used to hold multiple GUI elements

# st.container 		define streamlit container
# st.columns		define streamlit column(s)		the passed list defines the proportional size of each column
header_cont = st.container()
header_text_col, header_animation_col = st.columns([1.5, 1])
features_cont = st.container()
navigation_cont = st.container()



# Working with the header container
with header_cont :

	# st.markdown		display string formatted as Markdown
	st.markdown("<h1 style = 'text-align : center; color : #023e8a;'> ELECTRIC MEASUREMENTS FOR FATIGUE TESTS </h1>", unsafe_allow_html=True)

	st.markdown("<h3 style = 'text-align : center; color : #0077b6;'> Windmill Turbine Blades Damage Detection. (WIMDaD)  </h3>", unsafe_allow_html = True)

	st.markdown("# ")



with header_text_col :

	st.markdown("<div style ='text-align: justify;'> The application, developed in collaboration between TH Köln and the Metabolon Institute, serves the purpose of measuring and analyzing the results obtained from a series of fatigue tests conducted as part of the WIMDaD project. In this project, four distinct probes undergo a cyclic load, experiencing a displacement of 20 mm in both directions. The primary objective of the measurement process is to determine the time required for each individual probe to reach its breaking point.</div>", unsafe_allow_html = True)



with header_animation_col :
	header_animation = load_lottieurl('https://assets1.lottiefiles.com/packages/lf20_qp1q7mct.json')

	# using imported function to generate animation
	st_lottie(
		header_animation, 
		quality = 'high',
		height = 160,
		width = 300 	
		)



with features_cont : 
	st.markdown("<h2 style = 'text-align : left; color : #0096c7;'> Features of the Application </h2>", unsafe_allow_html = True)

	st.markdown(""" 

		- **Real-Time Measurements :**
			- Provides information about the current flowing on each of the probes.
			- Records the amount of time that it takes for each probe to break.
			- Possibility to store the measurements into CSV files for further analysis.

		""")

	st.markdown("""

		- **Results :**
			- The Results from each tests are saved in a new dataframe and stored in a separate page.
			- A plot for each result can be displayed to visualize the current behavior prior the breaking point. 

		""")


	st.markdown("# ")



st.markdown("# ")
