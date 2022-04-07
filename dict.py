import math
test_integration_dict = {"sin": [0, math.pi, math.pi, 2 * math.pi],
                         "exp": [0, 1, 2, 3],
                         "FWHM": [-10, 0, 0, 10],
                         "manual_peaks_ref": [940, 980, 1290, 1340],
                         "manual_peaks_CI": [1525, 1700, 1290, 1340],
                         "manual_peaks_CI2": [1525, 1700, 940, 980]}



correctness_dict = {"correct_960": [1286, 1398, 940, 980],
                    "correct_960ny": [1286, 1398, 930, 990],
                    "correct_2721": [1286, 1398, 2700, 2750]}

PVC_carbonyl_dict = {"PVC_1620_960": [1510, 1746, 900, 1000],
                     "PVC_1620_1330": [1510, 1746, 1286, 1398],
                     "PVC_1620_2721": [1510, 1746, 2700, 2750],
                     "PVC_1718_960": [1650, 1850, 900, 1000],
                     "PVC_1718_1330": [1650, 1850, 1286, 1398],
                     "PVC_1718_2721": [1650, 1850, 2700, 2750]
                     }

PVC_vinyl_dict = {"PVC_600_960": [550, 650, 900, 1000],
                  "PVC_600_1330": [550, 650, 1286, 1398],
                  "PVC_600_2721": [550, 650, 2700, 2750],
                  "PVC_1205_960": [1200, 1225, 900, 1000],
                  "PVC_1205_1330": [1200, 1225, 1286, 1398],
                  "PVC_1205_2721": [1200, 1225, 2700, 2750]}

PP_carbonyl_dict = {"PP_1700_960": [1550, 1850, 900, 1000],
                    "PP_1700_1330": [1550, 1850, 1286, 1398],
                    "PP_1700_2721": [1550, 1850, 2700, 2750]}

plastic_dict = {"test": test_integration_dict,
                "correctness": correctness_dict,
                "PVC_carbonyl": PVC_carbonyl_dict,
                "PVC_vinyl": PVC_vinyl_dict,
                "PP_carbonyl": PP_carbonyl_dict}
