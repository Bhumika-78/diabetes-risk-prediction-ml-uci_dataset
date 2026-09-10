# Duplicate Record Analysis & Profile Consistency

| Metric                    | Value  | Interpretation                                                                              |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------- |
| Total Records             | 520    | Original dataset record count                                                               |
| Unique Profiles           | 251    | Distinct clinical patient feature vectors                                                   |
| Duplicate Records         | 269    | Repeated identical patient vectors                                                          |
| Duplicate Rate (%)        | 51.73% | Over half of dataset consists of repeated survey entries                                    |
| Conflicting Class Labels  | 0      | Identical symptom vectors having different labels (0 indicates 100% deterministic labeling) |
| Label Integrity Score (%) | 100.0% | Perfect consistency across all repeated measurements                                        |
