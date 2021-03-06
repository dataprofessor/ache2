import streamlit as st
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, matthews_corrcoef
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from PIL import Image

st.markdown('# 💊 AChEpred')
st.info('Prediction of Acetylcholinesterase inhibitors and non-inhibitors')
st.markdown('- [**Link to Paper**](https://peerj.com/articles/2322/)')

st.sidebar.header("Author's Name")
author_names = st.sidebar.text_input('Enter the author names')
st.write(author_names)

st.markdown('# Abstract')
st.info('Alzheimer’s disease (AD) is a chronic neurodegenerative disease which leads to the gradual loss of neuronal cells. Several hypotheses for AD exists (e.g., cholinergic, amyloid, tau hypotheses, etc.). As per the cholinergic hypothesis, the deficiency of choline is responsible for AD; therefore, the inhibition of AChE is a lucrative therapeutic strategy for the treatment of AD. Acetylcholinesterase (AChE) is an enzyme that catalyzes the breakdown of the neurotransmitter acetylcholine that is essential for cognition and memory. A large non-redundant data set of 2,570 compounds with reported IC50 values against AChE was obtained from ChEMBL and employed in quantitative structure-activity relationship (QSAR) study so as to gain insights on their origin of bioactivity. AChE inhibitors were described by a set of 12 fingerprint descriptors and predictive models were constructed from 100 different data splits using random forest. Generated models afforded R2, Q2CV and Q2Ext values in ranges of 0.66–0.93, 0.55–0.79 and 0.56–0.81 for the training set, 10-fold cross-validated set and external set, respectively. The best model built using the substructure count was selected according to the OECD guidelines and it afforded R2, Q2CV and Q2Ext values of 0.92 ± 0.01, 0.78 ± 0.06 and 0.78 ± 0.05, respectively. Furthermore, Y-scrambling was applied to evaluate the possibility of chance correlation of the predictive model. Subsequently, a thorough analysis of the substructure fingerprint count was conducted to provide informative insights on the inhibitory activity of AChE inhibitors. Moreover, Kennard–Stone sampling of the actives were applied to select 30 diverse compounds for further molecular docking studies in order to gain structural insights on the origin of AChE inhibition. Site-moiety mapping of compounds from the diversity set revealed three binding anchors encompassing both hydrogen bonding and van der Waals interaction. Molecular docking revealed that compounds 13, 5 and 28 exhibited the lowest binding energies of −12.2, −12.0 and −12.0 kcal/mol, respectively, against human AChE, which is modulated by hydrogen bonding, π–π stacking and hydrophobic interaction inside the binding pocket. These information may be used as guidelines for the design of novel and robust AChE inhibitors.')

st.markdown('# Introduction')

with st.expander('Click to expand'):
  st.markdown('''
  Neurodegenerative diseases is caused by the progressive loss of neural cells thereby leading to nervous system dysfunction (Beal, 1995; Kuca et al., 2016). In particular, Alzheimer’s disease (AD) is a debilitating illness that is expected to triple by the year 2050 (Brookmeyer et al., 2007). AD is characterized by gradual cognitive impairment, memory loss and decline in speech, behavioral abnormality and eventually death. The pathological changes in AD are mainly attributed to the dramatic loss of neurons in many areas of the central nervous system accompanied by a great reduction in the levels of neurotransmitters. Acetylcholine (ACh) is a neurotransmitter possessing important cognitive and muscular functions. Particularly, in the peripheral nervous system, ACh is found at the neuromuscular junction where it is involved in muscle contraction while in the central nervous system, it is involved in cognitive functions such as thought, learning and memory.

  Acetylcholinesterases (AChE) is an enzyme that catalyzes the breakdown of ACh to choline and acetic acid (Quinn, 1987). Thus, a promising therapeutic approach is to maintain the level of ACh by inhibiting the enzyme that is responsible for its breakdown. The structure of AChE is comprised of four main subsites consisting of anionic subsite, esteratic site, oxyanion hole and the acyl pocket (Bourne, Taylor & Marchot, 1995). The anionic site is involved in the binding of the positive quaternary amine of ACh (Ordentlich et al., 1993). The substrate interacts with the 14 aromatic residues that forms the active site. Of these 14 aromatic residues, Trp84 is important for the enzyme activity because when it is replaced by alanine, the activity of the enzyme decreased by 3,000-fold (Tougu, 2001). The esteratic site contains the catalytic triad consisting of Ser203, His447 and Glu334 (i.e., resembling that of chymotrypsin and other serine proteases) that hydrolyzes ACh to acetate and choline (Harel et al., 1993). The mechanism of the hydrolysis starts from the carboxyl ester leads to the formation of an acyl-enzyme and choline. Finally, the acyl-enzyme undergoes nucleophilic attack by water molecules thereby regenerating the enzyme (Tougu, 2001). The oxyanion hole consisting of Gly121, Gly122 and Ala204 contribute hydrogen bond donors to help stabilize the tetrahedral intermediate of ACh form during catalysis. The acyl pocket consisting of Phe295 and Phe297 are gatekeepers that limit the dimension of substrates that can enter the active site.

  AChE inhibitors form one of the most actively investigated classes of compounds having been labeled as a potential agent for the treatment of AD by inhibiting AChE from hydrolyzing ACh, thereby leading to increases in the level of ACh (Birks, 2006). Generally, AChE inhibitors can be classified into reversible and irreversible inhibitors. Reversible inhibitor bind to the enzyme at allosteric sites as to reduce the activity of the enzyme whether or not the enzyme has already bind the substrate or not. Tacrine is a reversible AChE inhibitor that was synthesized nearly five decades ago and in 1993 it has become the first drug to be marketed for the treatment of AD with approval from the US. Food and Drug Administration (Racchi et al., 2004). On the other hand, irreversible inhibitors such as metrifonate (Morris et al., 1998) bind to the target enzymes and dissociates very slowly from the enzyme via either covalent or non-covalent interactions (Kitz & Wilson, 1962).

  Quantitative structure–activity relationship (QSAR) is a paradigm that enables the prediction of biological activities for compounds of interest as a function of their descriptors through the use of statistical or machine learning methods (Nantasenamat et al., 2009). Aside from the ability to predict the activity, QSAR models have been instrumental in enabling understanding on the origin of these biological activities by means of interpreting the descriptors used in building such models.

  Historically, the first QSAR investigation of AChE inhibitors was reported by Mundy et al. (1978) almost 40 years ago in which the log(1/LD50 for a series of twelve substituted 0,0-dimethyl 0-(p-nitrophenyl) phosphorothioates and 0-analogs was predicted as a function of the octanol/water partition coefficient. Analysis of the literature of QSAR studies of AChE revealed that much of the early studies are classical QSAR models (i.e., Hansch and Free-Wilson approach) that are based on small congeneric compound set and primarily aimed at predicting AChE inhibition as to investigate the toxic effect of pesticides of various chemotypes belonging to either organophosphates (Mager, 1983; Aaviksaar, 1990) or carbamates (Su & Lien, 1980; Goldblum, Yoshimoto & Hansch, 1981; Walters & Hopfinger, 1986). Recent QSAR studies are based on the use of large and heterogeneous data sets comprising of structurally diverse chemotypes. This include the study from Yan & Wang (2012) where they predicted AChE inhibition for a large set of 404 compounds using multiple linear regression and support vector machine. Furthermore, Lee & Barron (2016) performed a 3D-QSAR investigation on a large set of 341 compounds comprising of organophosphates and carbamates. Moreover, Veselinović et al. (2015) compiled a set of 278 organophosphates for which they developed QSAR models for predicting AChE inhibition using SMILES-based descriptors.

  Research in this field had experienced two distinct transitions when viewed from biological and computational viewpoints. Biologically, early QSAR studies treat AChE as a biomarker of toxicity from pesticides while investigations from later years had shifted the focus by viewing AChE as a therapeutic target for the treatment of AD. In regards to the latter point, viewpoint on targeting AChE as a single target for treating AD is starting to be replaced by the multi-target concept in which the treatment for AD can be approached by a panel of key targets (Fang et al., 2015; Huang et al., 2011). Computationally, early studies are predominantly based on simple 2D-QSAR (Mundy et al., 1978; Su & Lien, 1980) while later years started to use more sophisticated approach for understanding AChE inhibition encompassing 3D-QSAR (Deb et al., 2012; Lee & Barron, 2016; Prado-Prado et al., 2012), molecular dynamics (Shen et al., 2002), molecular docking (Lu et al., 2011; Deb et al., 2012; Giacoppo et al., 2015), pharmacophore modeling (Lu et al., 2011; Gupta & Mohan, 2014) and statistical molecular design (Andersson et al., 2014; Prado-Prado, Escobar & Garcia-Mera, 2013).

  Herein, we propose the first large-scale QSAR investigation for predicting AChE inhibition, which to the best of our knowledge represents the largest collection of 2,570 non-redundant compounds. QSAR models were built using interpretable learning methods (e.g., random forest) and descriptors (i.e., molecular fingerprints) as to unravel the underlying AChE inhibitory activity, which was performed in accordance with guidelines of the Organisation for Economic Cooperation and Development (OECD). Molecular docking was also performed on a chemically diverse set of compounds selected from active AChE inhibitors. Together, the ligand and structure-based approach employed in this study is anticipated to be useful in the design and development of robust AChE inhibitors.

  ''')

# 1. Load dataset
st.markdown('## 1. Load dataset')
st.info('''
A dataset consisting of Acetylcholinesterase bioactivity data was compiled from the ChEMBL database.
Each compounds were labeled as inhibitors (pIC50 ≥ 6) or non-inhibitors (pIC50 ≤ 5) on the basis of their bioactivity data values.
''')

dataset_url = 'https://raw.githubusercontent.com/dataprofessor/data/master/acetylcholinesterase_07_bioactivity_data_2class_pIC50_pubchem_fp.csv'
dataset = pd.read_csv(dataset_url)

with st.expander('See: Dataset'):
  st.write(dataset)

  
# 2. Data pre-processing
st.markdown('## 2. Data pre-processing')
          
# Prepare class label column
st.markdown('#### Prepare class label column')
bioactivity_threshold = []
for i in dataset.pIC50:
  if float(i) <= 5:
    bioactivity_threshold.append("inactive")
  elif float(i) >= 6:
    bioactivity_threshold.append("active")
  else:
    bioactivity_threshold.append("intermediate")
    
# Add class label column to the dataset DataFrame
bioactivity_class = pd.Series(bioactivity_threshold, name='class')
df = pd.concat([dataset, bioactivity_class], axis=1)

with st.expander('See: Dataset (with class label column)'):
  st.write(df)

# Select X and Y variables
st.markdown('#### Select X and Y variables')

X = df.drop(['pIC50', 'class'], axis=1)

def target_encode(val):
  target_mapper = {'inactive':0, 'active':1}
  return target_mapper[val]

Y = df['class'].apply(target_encode)

with st.expander('See: X variables'):
  st.write(X)

with st.expander('See: Y variable'):
  st.write(Y)

# Remove low variance features
st.markdown('#### Remove low variance features')

def remove_low_variance(input_data, threshold=0.1):
    selection = VarianceThreshold(threshold)
    selection.fit(input_data)
    return input_data[input_data.columns[selection.get_support(indices=True)]]

X = remove_low_variance(X, threshold=0.1)

with st.expander('See: X variables (low variance features removed)'):
  st.write(X)
