correctness_dict = {"1398-1286, 1000-900": [1286, 1398, 900, 1000],
                    "1398-1286, 2750-2700": [1286, 1398, 2700, 2750]}

PVC_carbonyl_dict = {"1746-1510, 1000-900": [1510, 1746, 900, 1000],
                     "1746-1510, 1398-1286": [1510, 1746, 1286, 1398],
                     "1746-1510, 2750-2700": [1510, 1746, 2700, 2750],
                     "1850-1650, 1000-900": [1650, 1850, 900, 1000],
                     "1850-1650, 1398-1286": [1650, 1850, 1286, 1398],
                     "1850-1650, 2750-2700": [1650, 1850, 2700, 2750]
                     }


PVC_vinyl_dict = {"650-550, 1000-900": [550, 650, 900, 1000],
                  "650-550, 1398-1286": [550, 650, 1286, 1398],
                  "650-550, 2750-2700": [550, 650, 2700, 2750],
                  "1225-1200, 1000-900": [1200, 1225, 900, 1000],
                  "1225-1200, 1398-1286": [1200, 1225, 1286, 1398],
                  "1225-1200, 2750-2700": [1200, 1225, 2700, 2750]}

PP_carbonyl_dict = {"1850-1550, 1000-900": [1550, 1850, 900, 1000],
                    "1850-1550, 1398-1286": [1550, 1850, 1286, 1398],
                    "1850-1550, 2750-2700": [1550, 1850, 2700, 2750]}

plastic_dict = {"PP carbonyl": PP_carbonyl_dict,
                "PVC carbonyl": PVC_carbonyl_dict,
                "PVC vinyl": PVC_vinyl_dict,
                "Reference peaks": correctness_dict}
