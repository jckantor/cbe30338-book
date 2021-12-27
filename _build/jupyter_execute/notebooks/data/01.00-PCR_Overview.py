#!/usr/bin/env python
# coding: utf-8

# # Case Study: Thermal Cycling for PCR

# ## Pre-reads
# 
# * [Notre Dame Center for Advanced Diagnostics and Therapeutics](https://advanceddiagnostics.nd.edu/assets/382241/coronavirus_test_faq.pdf)
# * [miniPCR Thermal Cycler]( https://www.youtube.com/watch?time_continue=1&v=ALNZJhUOSMs&feature=emb_logo)

# ## Coronavirus Diagnostics
# 
# 
# 
# COVID-19 is a respiratory tract infection by a specific species of coronavirus called SARS-CoV-2. Coronaviruses have a protein envelope characterized by club-shaped protrusions that give the impression of a corona when viewed with an electron microscope.
# 
# <p><a href="https://commons.wikimedia.org/wiki/File:Novel_Coronavirus_SARS-CoV-2.jpg#/media/File:Novel_Coronavirus_SARS-CoV-2.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Novel_Coronavirus_SARS-CoV-2.jpg/1200px-Novel_Coronavirus_SARS-CoV-2.jpg" alt="Electron micrograph of SARS-CoV-2 virions with visible coronae"></a><br>By NIAID - <a rel="nofollow" class="external free" href="https://www.flickr.com/photos/niaid/49534865371/">https://www.flickr.com/photos/niaid/49534865371/</a>, <a href="https://creativecommons.org/licenses/by/2.0" title="Creative Commons Attribution 2.0">CC BY 2.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=87484997">Link</a></p>
# 
# Coronaviruses have a relatively large genome comprised of a single strand of positive-sense RNA. A coronavirus test begins with a swab of throat or nose. The swab is rinsed with a buffer solution to capture the host DNA and RNA, and the RNA of any virus that may be present. RNA is isolated from the solution and converted to DNA using a reverse transcriptase enzyme.
# 
# The amount of DNA collected in this fashion is too small to analyze by conventional methods. So the first step in a diagnostic protocol is to amplify the amount of DNA using the polymerase chain reaction.

# ## Polymerase Chain Reaction (PCR)
# 
# The polymerase chain reaction (PCR) is a technique used in molecular biology to take amplify small samples of DNA into quantities large enough to be detected using conventional analytical methods. 
# 
# <a title="Enzoklop / CC BY-SA (https://creativecommons.org/licenses/by-sa/3.0)" href="https://commons.wikimedia.org/wiki/File:Polymerase_chain_reaction.svg"></a>
# 
# 
# <img width="1200" alt="Polymerase chain reaction" src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Polymerase_chain_reaction.svg/1200px-Polymerase_chain_reaction.svg.png">
# 
# The main part of PCR consists of three steps that are repeated 20 or more times:
# 
# 1. Denaturation at 94-96 $^\circ$C. At this step, DNA 'breaks apart', splitting from a double helix into single strands
# 2. Annealing at 68 $^\circ$C. Primers bond to the single-stranded DNA
# 3. Extension at ca. 72 $^\circ$C. Polymerase compliments the DNA, synthesizing strands that are of the target sequence
# 

# ## Examples of low-cost and open-source PCR thermal cyclers
# 
# * [miniPCR Thermal Cycler]( https://www.youtube.com/watch?time_continue=1&v=ALNZJhUOSMs&feature=emb_logo)
# * https://www.instructables.com/id/Arduino-PCR-thermal-cycler-for-under-85/
# 

# In[1]:


from IPython.display import YouTubeVideo
YouTubeVideo('ALNZJhUOSMs')


# In[ ]:




