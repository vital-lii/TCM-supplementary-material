# Validation of Semi-Quantitative Scoring System for  Nanocarriers in Pulmonary Delivery

## 1. Background of the Scoring System

This semi-quantitative scoring system aims to provide an objective assessment framework for the pulmonary delivery potential of Traditional Chinese Medicine (TCM) nanocarriers. The system is constructed based on systematic analysis of the latest research advances in the field of nanodrug delivery to provide theoretical guidance for nanocarrier design if it went well.

### 1.1 Objectives and Significance

- Establish a universal scoring framework applicable to different types of nanocarrier systems
- Predict the pulmonary delivery efficiency of nanocarriers, reducing experimental resource consumption
- Promote comparability and standardization of results across different studies
- Assist in the rational design of more efficient TCM nano-delivery systems

### 1.2 System Scope

The scoring system covers key parameters affecting nanocarrier pulmonary delivery efficiency, divided into five categories:

- Physical properties (35%): Particle size, PDI, Zeta potential
- Carrier properties (26%): Carrier type, Surface modification
- Biological properties (25%): Toxicity/Biocompatibility, Stability
- Delivery properties (10%): Cellular uptake, Biodistribution
- Drug properties (4%): Encapsulation efficiency

## 2. Methodological Design

### 2.1 Literature Analysis Method

Python-based computational methods were used to systematically analyze PubMed articles:

1. Systematic collection and organization of article metadata (PMID, abstract, title, keywords, and publication year)
2. Application of natural language processing techniques to extract terminology related to nanocarriers
3. Quantitative calculation of relative weights for key parameters based on their frequency in article abstracts

### 2.2 Weight Determination Method

A two-tier weight distribution method was adopted:

1. **Category-level weights**: Assigned directly based on frequency in literature: physical properties (35%), carrier properties (26%), biological properties (25%), delivery properties (10%), and drug properties (4%)
2. **Within-category parameter weights**: Selected the most representative parameters within each category, considering both literature analysis results and expert experience for weight distribution

### 2.3 Scoring Standards Development

The scoring standards for each parameter were determined based on optimized ranges reported in scientific literature:

1. **Particle Size Scoring Standard**:

   - <50 nm: 5 points
   - 50-100 nm: 3 points
   - 100-200 nm: 2 points
   - > 200 nm: 0 points
     >
2. **PDI Scoring Standard**:

   - <0.1: 5 points
   - <0.2: 4 points
   - <0.3: 3 points
   - <0.4: 1 point
   - > 0.4: 0 points
     >
3. **Zeta Potential Scoring Standard**:

   - > 30 mV: 5 points
     >
   - > 20 mV: 4 points
     >
   - > 10 mV: 2 points
     >
   - <10 mV: 0 points
4. **Carrier Type Scoring**:

   - NLC/SLN/Liposome: 4 points
   - PLGA/Chitosan: 4 points
   - Composite carriers: 4 points
   - Inorganic carriers: 2 points
5. **Surface Modification Scoring**:

   - PEG: 5 points
   - Chitosan: 4 points
   - Cationic modification: 3 points
   - Antibody conjugation: 3 points
   - No modification: 1 point

## 3. Computational Implementation

### 3.1 Code Architecture

We developed the following Python modules to implement the scoring system:

- `semi_qua.py`: Core implementation of the semi-quantitative scoring system

  - `calculate_absolute_weights()`: Returns weights for each parameter
  - `calculate_score()`: Calculates the comprehensive score for nanocarriers
  - Parameter scoring functions: `size_score()`, `pdi_score()`, `zeta_score()`, etc.
- `validate_weights.py`: Validates the effectiveness of the scoring system

  - Extracts nanocarrier data from literature
  - Calculates correlation between scores and actual performance indicators (FPF, MMAD)
  - Visualizes results

### 3.2 Calculation Flow

```python
# Core calculation flow example
def calculate_score(particle_size, pdi, zeta_potential, carrier_type, surface_modification, ...):
    # Calculate scores for each parameter
    size_score_val = size_score(particle_size)
    pdi_score_val = pdi_score(pdi)
    zeta_score_val = zeta_score(zeta_potential)
    carrier_score_val = carrier_score(carrier_type)
    surface_score_val = surface_score(surface_modification)
  
    # Get weights
    weights = calculate_absolute_weights()
  
    # Calculate weighted total score
    total_score = (
        size_score_val * weights['particle_size'] +
        pdi_score_val * weights['pdi'] +
        zeta_score_val * weights['zeta_potential'] +
        carrier_score_val * weights['carrier_type'] +
        surface_score_val * weights['surface_modification'] +
        ...
    )
  
    return total_score
```

## 4. Validation Method

### 4.1 Validation Dataset

We collected detailed data for 7 nanoformulations from published literature:

- Covering various carrier types: liposomes, PLGA, NLC, and polymer systems
- Applied to different pulmonary disease states
- Including key physicochemical parameters and measured delivery efficiency indicators (FPF, MMAD)

### 4.2 Validation Steps

1. Extract physicochemical parameters of nanocarriers from literature
2. Calculate the score for each nanocarrier using the `calculate_score()` function from `semi_qua.py`
3. Extract experimentally determined FPF and MMAD values from respective publications
4. Assess correlation between scores and performance indicators using Spearman rank correlation analysis
5. Calculate p-values to evaluate the statistical significance of correlations

### 4.3 Validation Tools

- Python packages: pandas (data processing), scipy.stats (statistical analysis), matplotlib (visualization)
- Use the `validate_weights.py` script to automatically execute the entire validation process
- Support for reading nanocarrier information from CSV or Markdown format data files

## 5. Validation Results

### 5.1 Correlation Analysis

Validation results showed low correlation between the scoring system and actual performance indicators:

- FPF correlation: Spearman's ρ = 0.00, p-value = 1.0000
- MMAD correlation: Spearman's ρ = -0.29, p-value = 0.5345

### 5.2 Results Interpretation

1. **Complexity of Nano-Bio Interactions**: The performance of pulmonary nanocarriers likely emerges from complex, non-linear interactions between multiple parameters that cannot be adequately captured by a linear scoring system
2. **Material-Specific Determinants**: Different carrier materials (lipids, polymers, etc.) may have unique structure-function relationships in the pulmonary environment, preventing generalization across carrier types
3. **Pulmonary delivery system**: These 7 nanoparticles are applied across various pulmonary delivery systems and diffential in vitro pulmonary deposition experiment, which may have different performance metric. As shown in Figure 4, salbutamol-lip-asth, which was calculated low score but with adequate FPF and MMAD values.
4. **Multifactorial Performance Determinants**: Critical factors influencing in vivo performance may extend beyond the conventional physicochemical parameters typically characterized and reported in literature

### 5.3 Scientific Findings

These results align with broader challenges in nanomedicine translation, where promising preclinical results often fail to translate reliably to clinical settings. Our results empirically demonstrate why nanodrug development progresses more slowly than conventional pharmaceutical development—the complexity and heterogeneity of nanomaterials necessitate individualized approaches rather than universal frameworks.

## 6. Future Research Directions

Based on the findings from our validation study, we recommend that TCM nanocarrier research should develop in the following directions:

1. **Material-Specific Optimization Strategies** - Developing dedicated optimization guidelines for each major carrier type (lipid-based, polymer-based, etc.)
2. **Experimental Design Optimization** - Emphasizing rigorous experimental design with appropriate controls and standardized characterization methods
3. **Context-Specific Evaluation** - Creating evaluation methodologies tailored to specific therapeutic applications and administration routes
4. **Machine Learning Approaches** - Leveraging computational methods to identify non-linear relationships and complex patterns in nanocarrier performance data

## 7. Resources and Code

The complete validation process, data, and code can be accessed through the following resources:

- Data files: `data/input/list.md` or `data/input/nanocarriers.csv`
- Core implementation of scoring system: `code/semi_qua.py`
- Validation script: `code/validate_weights.py`

## 8. Conclusion

The main finding of this study is that nanocarrier performance emerges from complex material-drug-biological interactions that fundamentally depend on experimental validation and are difficult to accurately predict using a universal semi-quantitative scoring system. This finding represents a valuable contribution to the understanding of nanomedicine development challenges, emphasizing the necessity of developing specific optimization strategies for different carrier types.

## 9. References(in nanocarriers.csv)

Y2PYZTMF[^zhangInhalationTreatmentPrimary2018]
6W44S2Z2[^honmaneLungDeliveryNanoliposomal2019]
EAAKZTDL[^jiaPulmonaryDeliveryMagnololloaded2024]
BY2SBCWB[^wangDevelopmentCharacterizationInhaled2024]
CE2CN553[^said-elbahrNebulizableColloidalNanoparticles2016]
TFT3V9US[^galdoporporaInhalableMannosylatedRifampicin2022]

[^zhangInhalationTreatmentPrimary2018]: Zhang, T., Chen, Y., Ge, Y., Hu, Y., Li, M., & Jin, Y. (2018). Inhalation treatment of primary lung cancer using liposomal curcumin dry powder inhalers. Acta Pharmaceutica Sinica B, 8(3), 440–448. https://doi.org/10.1016/j.apsb.2018.03.004
    
[^honmaneLungDeliveryNanoliposomal2019]: Honmane, S., Hajare, A., More, H., Osmani, R. A. M., & Salunkhe, S. (2019). Lung delivery of nanoliposomal salbutamol sulfate dry powder inhalation for facilitated asthma therapy. Journal of Liposome Research, 29(4), 332–342. https://doi.org/10.1080/08982104.2018.1531022
    
[^jiaPulmonaryDeliveryMagnololloaded2024]: Jia, B., He, J., Zhang, Y., Dang, W., Xing, B., Yang, M., Xie, H., Li, J., & Liu, Z. (2024). Pulmonary delivery of magnolol-loaded nanostructured lipid carriers for COPD treatment. International Journal of Pharmaceutics, 662, 124495. https://doi.org/10.1016/j.ijpharm.2024.124495
    
[^wangDevelopmentCharacterizationInhaled2024]: Wang, X., Gadhave, D., Chauhan, G., & Gupta, V. (2024). Development and characterization of inhaled nintedanib-loaded PLGA nanoparticles using scalable high-pressure homogenization technique. Journal of Drug Delivery Science and Technology, 91, 105233. https://doi.org/10.1016/j.jddst.2023.105233
    
[^said-elbahrNebulizableColloidalNanoparticles2016]: Said-Elbahr, R., Nasr, M., Alhnan, M. A., Taha, I., & Sammour, O. (2016). Nebulizable colloidal nanoparticles co-encapsulating a COX-2 inhibitor and a herbal compound for treatment of lung cancer. European Journal of Pharmaceutics and Biopharmaceutics, 103, 1–12. https://doi.org/10.1016/j.ejpb.2016.03.025
    
[^galdoporporaInhalableMannosylatedRifampicin2022]: Galdopórpora, J. M., Martinena, C., Bernabeu, E., Riedel, J., Palmas, L., Castangia, I., Manca, M. L., Garcés, M., Lázaro-Martinez, J., Salgueiro, M. J., Evelson, P., Tateosian, N. L., Chiappetta, D. A., & Moretton, M. A. (2022). Inhalable Mannosylated Rifampicin–Curcumin Co-Loaded Nanomicelles with Enhanced In Vitro Antimicrobial Efficacy for an Optimized Pulmonary Tuberculosis Therapy. Pharmaceutics, 14(5), Article 5. https://doi.org/10.3390/pharmaceutics14050959
